def get_subscriptions_to_topic_arn(sns_connection, topic_arn):
    response = sns_connection.get_all_subscriptions_by_topic(topic_arn)
    return response['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['Subscriptions']


def get_confirmed_subscriptions_to_topic_arn(sns_connection, topic_arn):
    subscriptions = get_subscriptions_to_topic_arn(sns_connection, topic_arn)
    return [s for s in subscriptions if s['SubscriptionArn'] != 'PendingConfirmation']


def get_subscriptions_to_topic(sns_connection, topic):
    response = sns_connection.get_all_subscriptions()
    all_subscriptions = response['ListSubscriptionsResponse']['ListSubscriptionsResult']['Subscriptions']

    return [s for s in all_subscriptions if s['TopicArn'].endswith(topic)]


def get_confirmed_subscriptions_to_topic(sns_connection, topic):
    subscriptions = get_subscriptions_to_topic(sns_connection, topic)
    return [s for s in subscriptions if s['SubscriptionArn'] != 'PendingConfirmation']


def get_all_topic_arns(sns_connection):
    response = sns_connection.get_all_topics()
    return [t['TopicArn'] for t in response['ListTopicsResponse']['ListTopicsResult']['Topics']]


def get_topic_arns(sns_connection, topics):
    all_topic_arns = get_all_topic_arns(sns_connection)
    return [t for t in all_topic_arns if topic_name_from_topic_arn(t) in topics]


def get_all_topics(sns_connection):
    all_topic_arns = get_all_topic_arns(sns_connection)
    return [topic_name_from_topic_arn(t) for t in all_topic_arns]


def topic_name_from_topic_arn(arn):
    return arn[arn.rfind(':')+1:]


def get_topics(sns_connection, topics):
    all_topics = get_all_topics(sns_connection)
    return [t for t in all_topics if t in topics]


def format_message(msg_format, *args):
    args_length = 0
    for arg in args:
        args_length += len(str(arg))

    msg_format_length = len(msg_format) - msg_format.count('%s') * 2

    amt_to_trim_from_each_arg = ((args_length + msg_format_length) - 140) / len(args)
    if amt_to_trim_from_each_arg > 0:
        format_params = [arg[:-amt_to_trim_from_each_arg] for arg in args]
    else:
        format_params = args

    return msg_format % tuple(format_params)
