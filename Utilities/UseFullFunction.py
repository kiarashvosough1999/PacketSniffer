from Utilities.MyExceptions import MyException, ExceptionAction


def safe_cast(val, to_type, error_message):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return MyException(message='{} is not {}'.format(error_message, to_type),
                           action=ExceptionAction.casting_error)
