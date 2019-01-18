import network.net_utils as utils
from enum import Enum

class MessageType(Enum):
    CONNECT=1
    INFO = 2
    DATA = 3

    UNKNOWN = 255

def form_data_message(data):
    msg = bytes([MessageType.DATA.value]) + utils.int_to_bytes(len(data))
    msg += bytes(data,'utf-8')
    # TODO: pickle the data object
    return msg

def form_connect_message(name):
    msg = bytes([MessageType.CONNECT.value]) + utils.int_to_bytes(len(name))
    msg += bytes(name,'utf-8')
    # TODO: pickle the data object
    return msg

def get_message_data(msg):
    """
    Parameters
    ------------
    msg: bytes
        the input message
    """
    #TODO: use pickle
    return msg[3:].decode('utf-8')

def get_message_length(msg):
    """
    Parameters
    ------------
    msg: bytes
        the input message
    """
    msg_len = utils.bytes_to_int(msg[1:3])
    return msg_len

def get_message_type(msg):
    """
    Parameters
    ------------
    msg: bytes
        the input message
    """
    msg_type = msg[0]
    if msg_type == 1:
        return MessageType.CONNECT
    elif msg_type == 2:
        return MessageType.INFO
    elif msg_type == 3:
        return MessageType.DATA

    else:
        return MessageType.UNKNOWN
