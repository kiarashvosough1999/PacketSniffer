# PacketSniffer

PacketSniffer is a python application which you can use it to
control over your network statistics.

## Run On Terminal

Use 'python3' command to execute program.
```bash
python3 path_to/main.py
python3 path_to/main.py [-h] [-wt WAITTIME] [-tc THREADCOUNT] [-ip IPVER] [-sp STARTPORT] [-ep ENDPORT] address mode
```

## Arguments That You Can Pass

- **Address** : the IP (v4 or v6) that you wish to sniff on. you can pass ip address or host name plus its domain.
- **Thread number** : number of threads (*_there is also a limit that we prompt before you enter your inputs_*) that the program can use to complete its tasks.
- **waiting time** : time (in second) that program wait to get response back from the server for each port.
- **sniffing modes** : port range for specific set of port that can be sniffed.
- **start** : start value of port interval that program will check(**optional**).
- **end** : end value of port interval that program will check(**optional**).
- **ip Vesrion** : ipV6 and ipV4 are supported(**default is set on ipV4**).

> *_you can skip optional inputs it by just pressing enter._*
>
> *_you can skip port interval input by pressing enter so that program check evety port on that mode._*
>
> *_if you pass argument directly in front of main.py make sure you provide address and sniffing mode which are required, other parameters are optional and have default value._*

## Sniffing Modes
1. All Ports (0-65535)
2. Reserved Port (including a varity of popular port from host around the world)
3. application layer services (TELNET, FTP, SSH, HTTP, HTTP_TLS, SMTP, SMTP_TLS, POP, IMAP, POP_TLS, IMAP_TLS)

## Passing Arguments Examples

###Method 1

You just need to execute main.py.

```bash
python3 path_to/main.py

You can run 10000 threads concurently, do not try to hit the limit unless there is no guarantee to work properly.
Address: 
>> www.google.com
Thread Number:
>> 5000
Port Scanning Waiting Time:
>> 1 
ip Address version: 4.ipV4 6.ipV6 (default is ipV4, to ignore just press enter)
>> 4
Choose your sniffing mode: 1.App Ports  2.Reserved Port  3.application layer services
>> 3
Port Start Interval: 
>> 200
Port End Interval: 
>> 1000
```

###Method 2

You can execute main.py and provide arguments in front of it, first two arguments are required, but the rest of them are optional.

- **Thread number** : default is set to 10.
- **waiting time** : default is set to 2.
- **start, end** : default is set to None which means program will check all ports.
- **ip Vesrion** : default is set to ipV4.

```bash
python3 path_to/main.py google.com 3 -wt 2 -tc 20 -ip 4 -sp 1 -ep 0
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)