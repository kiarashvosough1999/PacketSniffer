# PacketSniffer

PacketSniffer is a python application which you can use it to
control over your network statistics.

## Run On Terminal

Use ' python3' command to execute program.

## Arguments that you can pass

- address : the IP (v4 or v6) that you wish to sniff on.
- thread_num : number of threads that the program can use to complete its tasks.
- waiting_time : time (in second) that program wait to get response back from the server.
- sniffing modes: port rang or specific set of port that can be sniffed.
- start : start value of port interval that program will check.
- end : end value of port interval that program will check.
- ip Vesrion: ipV6 and ipV4 are supported.

## Sniffing Modes

1.All Ports (0-65535)
2.Reserved Port (including a varity of popular port from host around the world)
3.application layer services (TELNET, FTP, SSH, HTTP, HTTP_TLS, SMTP, SMTP_TLS, POP, IMAP, POP_TLS, IMAP_TLS)

## Passing Arguments

Method 1: pass in python argv.
```bash
python3 address thread_num waiting_time sniffingMode start(optional in some cases) end(optional in some cases) ipVesrion(default is 4)
```
Method 2: pass nothing as argv and the program will prompt and ask you for your inputs.
```bash
python3 [path_to_main.py]
```
## Examples
this will check google.com host with 4 thread and 1 second as timeout for checking each port between 50 and 1000 with ipV4.
```bash
python3 google.com 4 1 1 50 1000 4
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)