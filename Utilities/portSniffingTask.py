from enum import Enum


class portSniffingTask(Enum):
    all_port = 0
    reserved_port = 1
    application_port = 2
    error = -1

    @staticmethod
    def get_type(from_string):
        if from_string == '1':
            return portSniffingTask.all_port
        elif from_string == '2':
            return portSniffingTask.reserved_port
        elif from_string == '3':
            return portSniffingTask.application_port
        return portSniffingTask.error
