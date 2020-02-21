* compile
```
gcc -o server server.c  
gcc -o client client.c
```

* server
```
$ ./server
Listening...
New client(4) connecting...
Received from client(4): test

Received from client(4): hello

Received from client(4): 
Client(4) closing...
```

* client
```
$ ./client
Type a sentence to send to server:
You typed: test
Received from server: test


Type a sentence to send to server:
You typed: hello
Received from server: hello
```
