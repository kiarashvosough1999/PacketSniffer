# PacketSniffer

PacketSniffer is a python application which you can use it to
control over your network statistics.

## Run On Terminal

Use ' python3' command to execute program.

## Arguments that you can pass

- address : the IP (v4 or v6) that you wish to sniff on.
- thread_num : number of threads that the program can use to complete its tasks.
- waiting_time : time (in second) that program wait to get response back from the server.
- sniffing mode: port rang or specific set of port that can be sniffed.
- start : start value of port interval that program will check.
- end : end value of port interval that program will check.

## Passing Arguments

Method 1: pass in python argv.
```bash
python3 address thread_num waiting_time start end
```
Method 2: pass nothing as argv and the program will prompt and ask you for your inputs.
```bash
python3 [path_to_main.py]
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)