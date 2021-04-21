from DataModels.PingInputsModel import PingInputsModel
from Ping.Ping import ping
from Utilities.AppStartManager import AppStartManager
from Utilities.Threading.PrintThread import PrintThread


if __name__ == '__main__':
    PrintThread.shared().start_print_thread()
    p = ping(PingInputsModel(['google.com','python.org','bing.com'],2000,55))
    p.start()
    # AppStartManager().start()
