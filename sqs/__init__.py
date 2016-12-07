import time
from aws.s3 import bulk_delete_keys
from boto.sqs.message import RawMessage


def wait_for_message(queue, timeout_seconds=0):
    timeout_time = time.time() + timeout_seconds

    while time.time() < timeout_time if timeout_seconds else True:
        message = get_single_message(queue)
        if message:
            return message
    return None


def get_single_message(queue, wait=None, visibility_timeout=None, attributes=None):
    # if wait=None, this will wait up to the specified timeout on the SQS Queue (probably 20 seconds)
    messages = queue.get_messages(1,
                                  wait_time_seconds=wait,
                                  visibility_timeout=visibility_timeout,
                                  attributes=attributes)
    return messages[0] if len(messages) > 0 else None


def oldest_message_timestamp(queue):
    msg = get_single_message(queue, visibility_timeout=0, wait=0, attributes='SentTimestamp')
    timestamp = int(msg.attributes['SentTimestamp'])/1000.0 if msg else None
    return timestamp


def messages_are_available(queue):
    return queue.read(visibility_timeout=0) is not None


def is_empty(queue):
    attr = queue.get_attributes()
    total_messages = int(attr['ApproximateNumberOfMessages']) + \
                     int(attr['ApproximateNumberOfMessagesDelayed']) + \
                     int(attr['ApproximateNumberOfMessagesNotVisible'])

    if total_messages == 0:
        # Double check by attempting to read.
        message = queue.read(visibility_timeout=0)
        if message is None:
            return True
    return False


def persist_to_s3(sqs, prefix, bucket):
    queues = sqs.get_all_queues(prefix)

    # Save the queues with the oldest messages first
    queue_ages = sorted([(queue, int(get_queue_age(queue))) for queue in queues], key=lambda t: t[1], reverse=True)

    for queue, age in queue_ages:
        queue.set_message_class(RawMessage)
        queue.save_to_s3(bucket)


def restore_from_s3(sqs, bucket, queue_creator=None):
    queue_ids = [p.name for p in bucket.list('', '/')]
    for queue_id in queue_ids:
        prefixes = bucket.list(queue_id, '/')
        for prefix in prefixes:
            queue_name = prefix.name[len(queue_id):-1]
            if queue_creator is None:
                queue = sqs.create_queue(queue_name)
            else:
                queue = queue_creator(queue_name)
            queue.set_message_class(RawMessage)
            queue.load_from_s3(bucket, prefix.name[:-1])
            bulk_delete_keys(bucket, prefix.name)


def move_messages(from_queue, to_queue, predicate=lambda m: True, progress_callback=None):
    """
    :param from_queue: Queue to move messages from
    :param to_queue: Queue to move messages to
    :param predicate: Message is moved if this predicate evaluates to True. Params: message body
    :param progress_callback: Callback method. Params: total_messages, moved_messages
    :return: total_messages, moved_messages
    """
    orig_from_queue_message_class = from_queue.message_class
    orig_to_queue_message_class = from_queue.message_class

    total_messages = 0
    moved_messages = 0

    try:
        from_queue.set_message_class(RawMessage)
        to_queue.set_message_class(RawMessage)

        visibility_timeout = 60

        messages = from_queue.get_messages(10, visibility_timeout=visibility_timeout)
        while messages:
            message_batch = []
            for message in messages:
                total_messages += 1
                body = message.get_body()
                if predicate(body):
                    message_batch.append((total_messages, body, 0))

            from_queue.delete_message_batch(messages)
            if len(message_batch) > 0:
                to_queue.write_batch(message_batch)
                moved_messages += len(message_batch)

            if progress_callback:
                progress_callback(total_messages, moved_messages)

            messages = from_queue.get_messages(10, visibility_timeout=visibility_timeout)
    finally:
        from_queue.set_message_class(orig_from_queue_message_class)
        to_queue.set_message_class(orig_to_queue_message_class)

    return total_messages, moved_messages


def cycle_queue(sqs, queue, egress_predicate=lambda m: True, ingress_predicate=lambda m: True, progress_callback=None):
    """
    SQS queues have a max retention period. This method cycles through all of the
    messages in the queue so that they can be retained in the queue longer.

    If this is interrupted for any reason, restarting it will begin where it left off.

    Warning: The original order of messages in the queue may not be preserved.
    """
    temp_queue = sqs.create_queue(queue.name + "-cycling")
    temp_queue.set_attribute('MessageRetentionPeriod', 1209600)  # 14 days

    total_msgs, _ = move_messages(queue, temp_queue, predicate=egress_predicate, progress_callback=progress_callback)
    _, moved_msgs = move_messages(temp_queue, queue, predicate=ingress_predicate,
                                  progress_callback=lambda t, m: progress_callback(t+total_msgs, _+m))

    temp_queue.delete()

    return total_msgs, moved_msgs


def count_messages(sqs, prefix):
    total_messages = 0
    for queue in sqs.get_all_queues(prefix):
        total_messages += queue.count()
    return total_messages


def get_queue_age(queue):
    messages = queue.get_messages(wait_time_seconds=0, visibility_timeout=0, attributes=['SentTimestamp'])
    message = messages[0] if messages else None
    if message is None:
        return 0

    return time.time() - int(message.attributes['SentTimestamp'])/1000.0
