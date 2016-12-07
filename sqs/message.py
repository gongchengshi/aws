from boto.sqs.message import Message, RawMessage
import pickle


class PickleMessage(Message):
    """ Simple class to dump/load data into Pythons
        pickle format upon reading or writing the
        message body.

        Must use set_body and get_body methods to
        access the data appropriately

        XXX: Because Message is not of an object
        type, the user of super() is not allowed.
        Filed bug report:

        http://code.google.com/p/boto/issues/detail?id=311
    """

    def set_body(self, body):
        new_body = pickle.dumps(body)
        Message.set_body(self, new_body)
    
    def get_body(self):
        new_body = Message.get_body(self)
        return pickle.loads(new_body)


def build_message_shell(queue, receipt_handle):
    msg = RawMessage(queue=queue)
    msg.receipt_handle = receipt_handle
    return msg
