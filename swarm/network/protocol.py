import utils
from enum import Enum

class MessageType(Enum):
    CONNECT=1
    INFO = 2
    DATA = 3

    UNKNOWN = 255

def get_message_type(msg):
    """
    Parameters
    ------------
    msg: bytes
        the input message
    """
    msg_type = msg_bytes[0]
    if msg_type == 1:
        return MessageType.CONNECT
    elif msg_type == 2:
        return MessageType.INFO
    elif msg_type == 3:
        return MessageType.DATA

    else:
        return MessageType.UNKNOWN
