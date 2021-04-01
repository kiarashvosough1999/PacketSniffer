# PacketSniffer

PacketSniffer is a python application which you can use it to
control over your network statistics.

## Run On Terminal

Use 'python3' command to execute program.
```bash
python3 path_to/main.py
```

## Arguments that you can pass

- **Address** : the IP (v4 or v6) that you wish to sniff on. you can pass ip address or host name plus its domain.
- **Thread number** : number of threads (*_there is also a limit that we prompt before you enter your inputs_*) that the program can use to complete its tasks.
- **waiting time** : time (in second) that program wait to get response back from the server for each port.
- **sniffing modes** : port range for specific set of port that can be sniffed.
- **start** : start value of port interval that program will check(**optional**).
- **end** : end value of port interval that program will check(**optional**).
- **ip Vesrion** : ipV6 and ipV4 are supported(**default is set on ipV4**).

> you can skip optional inputs it by just pressing enter.
>
> you can skip port interval input by pressing enter so that program check evety port on that mode.

## Sniffing Modes
1. All Ports (0-65535)
2. Reserved Port (including a varity of popular port from host around the world)
3. application layer services (TELNET, FTP, SSH, HTTP, HTTP_TLS, SMTP, SMTP_TLS, POP, IMAP, POP_TLS, IMAP_TLS)

## Passing Arguments Examples


```bash
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


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)