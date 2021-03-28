from DataModels.PortScanningModel import PortScanningModel
from Utilities.customRange import customRange
from portSniffer import portSniffer
import sys

port_data_model = None
# PortScanningModel(socket.gethostbyname('142.250.179.206'), 2, customRange(70, 450),1)

if __name__ == '__main__':

    print('enter your input in the folowing format')

    while True:
        print('Address: ')
        address = input()
        print('Thread Number: ')
        thread_num = input()
        print('Port Scanning Waiting Time: ')
        waiting_time = input()
        print('Port Start Interval: ')
        start = input()
        print('Port End Interval: ')
        end = input()

        if int(thread_num) and float(waiting_time) and int(start) and int(end):
            port_data_model = PortScanningModel(address=address,
                                                thread_number=int(thread_num),
                                                portRange=customRange(int(start), int(end)),
                                                waitingTime=float(waiting_time))
            if port_data_model.valid_ip_type():
                break
            else:
                print('IP address is not valid')
                print('enter your inputs again')
                continue
        else:
            print('there was a mistake in input data')
            print('enter your inputs again')
            continue

    try:
        x = portSniffer(port_data_model=port_data_model)
        x.start()
    except KeyboardInterrupt:
        print('\tInterrupted')
        sys.exit(0)
