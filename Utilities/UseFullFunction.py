from Utilities.MyExceptions import MyExeption, ExeptionAction


def safe_cast(val, to_type, error_message):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return MyExeption(message='{} is not {}'.format(error_message, to_type),
                          action=ExeptionAction.casting_error)