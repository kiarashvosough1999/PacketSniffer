from DataModels.Constant import Constant
from Utilities.Exception.MyExceptions import MyException, ExceptionAction


def safe_cast(val, to_type, error_message):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return MyException(message='{} is not {}'.format(error_message, to_type),
                           error_type=MyException.casting_error,
                           action=ExceptionAction.exit_0)


def convert_int_to_bytes(integer):
    return integer.to_bytes((integer.bit_length() + 7) // 8, Constant.big_byte_order)
