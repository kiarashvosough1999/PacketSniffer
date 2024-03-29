import socket

from DataModels.HOPUserInputsModel import HOPUserInputsModel
from TraceRoute.TraceRouter import TraceRouter
from Utilities.StartManagers.AppStartManager import AppStartManager
from Utilities.Threading.PrintThread import PrintThread

if __name__ == '__main__':
    PrintThread.shared().start_print_thread()
    AppStartManager(None).start()