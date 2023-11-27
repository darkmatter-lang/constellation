# Constellation

A WebSocket server for the [Darkmatter Website](https://darkmatter.anthonyw.me/) stars wallpaper.


## Protocol

All data is represented as JSON messages over WebSockets.

### Flow

1. Client connects.
2. Client sends `hello` request.
3. Server sends `hello` response.
4. Client sends periodic `ping` messages to avoid being automatically disconnected.
5. Client sends periodic `stars` requests.
6. Server sends `stars` response.

### Packet Table of Contents

- [HELLO]
- [SYSTEM_MESSAGE]
- [PING]
- [STAR_LIST]
- [STAR_CREATED]
- [STAR_DESTROYED]
- [STAR_UPDATE]
- [STAR_UPDATE_PUSH]
- [MESSAGE] *(unused)*







### HELLO
[HELLO]: #packet-hello

Client Request:
```json
{
	"msg": "hello",
	"cid": "c1255c00101b204e87edcecc225cf548", // unique random request-id
	"payload": {
		"version": {
			"major": 0,
			"minor": 1,
			"patch": 0
		},
		"user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
		"client_info": {
			// additional browser information
		}
	}
}
```

Server Response (Success):
```json
{
	"msg": "hello",
	"cid": "c1255c00101b204e87edcecc225cf548", // same request-id as sent by the client
	"payload": {
		"version": {
			"major": 0,
			"minor": 1,
			"patch": 0
		},
		"cors": "*",
		"name": "Constellation",
		"version_check": "ok",
		"valid": true,
		"star": {
			"id": "your unique hashed id",
			"gid": "your hashed group id",
			"color": 0, // color encoded as int
			"position": [0, 0]
		}
	}
}
```

Server Response (Version Error):
```json
{
	"msg": "hello",
	"cid": "c1255c00101b204e87edcecc225cf548",
	"payload": {
		"version": {
			"major": 0,
			"minor": 1,
			"patch": 0
		},
		"cors": "*",
		"name": "Constellation",
		"version_check": "fail",
		"valid": false
	}
}
```






### SYSTEM_MESSAGE
[SYSTEM_MESSAGE]: #packet-system_message

Only the server may send this message.

Currently in our JavaScript client implementation this will invoke a JS alert().

Client Request:
```json
{
	"msg": "system_message",
	"cid": null,
	"payload": {
		"message": "This is a system message!"
	}
}
```








### PING
[PING]: #packet-ping

Client Request:
```json
{
	"msg": "ping",
	"cid": "1ef6dc2eecb6dfdb54593e382e36384a",
	"payload": null
}
```

Server Response:
```json
{
	"msg": "ping",
	"cid": "1ef6dc2eecb6dfdb54593e382e36384a",
	"payload": null
}
```








### STAR_LIST
[STAR_LIST]: #packet-star_list

Client Request:
```json
{
	"msg": "star_list",
	"cid": "24b2dfd86be9ea9bed4b3bb9cd68d0ae",
	"payload": null
}
```

Server Response:
```json
{
	"msg": "star_list",
	"cid": "24b2dfd86be9ea9bed4b3bb9cd68d0ae",
	"payload": {
		"stars": [
			{
				"id": "11c2cdb0b2577accccc364a343f5ac7b",
				"gid": "044908991e186e5c467c307caf73b6ec",
				"color": 81389, // color encoded as int
				"position": [12.3456, -12.3456]
			},
			{
				"id": "75a22b574083dd7ae8c36fec1d996a77",
				"gid": "044908991e186e5c467c307caf73b6ec",
				"color": 34831, // color encoded as int
				"position": [7.8901, -7.8901]
			}
		]
	}
}
```




### STAR_CREATED
[STAR_CREATED]: #packet-star_created

Only the server may send this message.

A new star joined.

Server Response:
```json
{
	"msg": "star_update",
	"cid": null,
	"payload": {
		"star": {
			"id": "id hash",
			"gid": "group hash",
			"color": 34831, // color encoded as int
			"position": [7.8901, -7.8901]
		}
	}
}
```







### STAR_DESTROYED
[STAR_DESTROYED]: #packet-star_destroyed

Only the server may send this message.

A star left.

Server Response:
```json
{
	"msg": "star_destroyed",
	"cid": null,
	"payload": {
		"star": {
			"id": "id hash"
		}
	}
}
```










### STAR_UPDATE
[STAR_UPDATE]: #packet-star_update

Only the server may send this message.

Periodic server updates on stars that have updated their position.

Server Response:
```json
{
	"msg": "star_update",
	"cid": null,
	"payload": {
		"stars": [ // list of stars that have updated their position
			{
				"id": "id hash",
				"gid": "group hash",
				"color": 34831, // color encoded as int
				"position": [7.8901, -7.8901]
			}
		]
	}
}
```







### STAR_UPDATE_PUSH
[STAR_UPDATE_PUSH]: #packet-star_update-push

Updates other clients on our current position.

Client Request:
```json
{
	"msg": "star_update_push",
	"cid": "9c15b43937d13edd31ac9fbdab9b2a66",
	"payload": {
		"mouse_position": [0, 0]
	}
}
```

Server Response:
```json
{
	"msg": "star_update_push",
	"cid": "9c15b43937d13edd31ac9fbdab9b2a66",
	"payload": {
		"status": "ok",
		"success": true
	}
}
```








#### MESSAGE
[MESSAGE]: #packet-message

Messages can be sent on channels `1-256`, channel `0` is reserved for system commands send to and from the server.

```json
{
	"msg": "message",
	"cid": "1d68a4188e521d17d251c0f910ec5152",
	"payload": {
		"channel": 0,
		"message": ""
	}
}
```

### Message types

| Name             | Valid Channels | Data Type | Description                                        |
|------------------|----------------|-----------|----------------------------------------------------|
||














## Build

Ensure you *first* deploy [Darkmatter's Site](https://github.com/darkmatter-lang/darkmatter-site) before deploying this project.

### Build Docker image

```sh
./docker-build.sh
```

### Development Setup

Run the container:

```bash
docker run --rm \
	-it \
	--net darkmatter \
	--name darkmatter-constellation \
	-h darkmatter-constellation \
	-v "$(pwd):/mnt:ro" \
	darkmatter-constellation
```

### Production Deploy

```bash
docker run -d \
	--net darkmatter \
	--name darkmatter-constellation \
	-h darkmatter-constellation \
	-v "$(pwd)/:/mnt" \
	darkmatter-constellation
```


### Environment variables

| Name                  | Default Value   | Description                                               |
|-----------------------|-----------------|-----------------------------------------------------------|
| SERVER_NAME           | "Constellation" | The web-socket server name.                               |
| SYSTEM_MESSAGE        |                 | A system message announcement.                            |
| IDLE_TIMEOUT_INTERVAL | 10000           | Millis before a client is disconnected for idling.        |
| STAR_UPDATE_INTERVAL  | 1000            | Millis for periodic position updates.                     |
| BANNED_IPS            |                 | A comma-separated list of IP addresses to ignore.         |



















