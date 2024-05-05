# How to set up

Requires `python` with `pip` and `node` with `npm`.

## Server

Change directory to `./server`

```console
cd ./server
```

Create virtual environment and install dependencies

```console
python -m venv .venv && pip install -r requirements.txt
```

Compile Protocol Buffer files using attached script

```console
chmod u+x gen_proto.sh && ./gen_proto.sh
```

Start the server

```console
python server.py
```

## Client

Change directory to `./client`

```console
cd ./client
```

Install dependencies
```console
npm install
```

Start the client
```console
node client.js
```

