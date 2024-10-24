import websocket
import json
import time
from .const import PING_INTERVAL, CLIENT_UID

def open_websocket(access_token, connection_id):
    ws_url = f"wss://bliss.iot.findernet.com/_sync?id={connection_id}"
    server_payload = None

    def on_message(ws, message):
        nonlocal server_payload
        messages = message.split("\x1e")
        for msg in messages:
            if msg.strip():
                process_message(ws, msg.strip())

    def process_message(ws, msg):
        nonlocal server_payload
        try:
            msg_json = json.loads(msg)
            if 'serverPayload' in msg_json.get('arguments', [{}])[0]:
                server_payload = msg_json['arguments'][0]['serverPayload']
                print("Extracted serverPayload:")
                print(server_payload)
                ws.close()
            else:
                print("No serverPayload found in the message.")
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")

    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")

    def on_open(ws):
        print("WebSocket connection opened")
        send_initial_messages(ws)

    def send_initial_messages(ws):
        protocol_message = {"protocol": "json", "version": 1}
        ws.send(json.dumps(protocol_message) + "\x1e")

        init_request_message = {
            "type": 1,
            "target": "InitRequest",
            "arguments": [{
                "clientId": CLIENT_UID,
                "stamp": None,
                "clientPlatform": "Android/7.1.1",
                "clientModel": "OnePlus/ONEPLUS A5000",
                "clientBuild": "166"
            }]
        }
        ws.send(json.dumps(init_request_message) + "\x1e")

        time.sleep(2)

        sync_request_message = {
            "type": 1,
            "target": "SyncRequest",
            "arguments": [{
                "clientId": CLIENT_UID,
                "clientOperationId": "00000000-0000-0000-0000-000000000000",
                "clientSyncVersion": 0,
                "serverSyncVersion": 0,
                "stamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + ".000Z",
                "status": "ACTIVE"
            }]
        }
        ws.send(json.dumps(sync_request_message) + "\x1e")

    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header={"Authorization": f"Bearer {access_token}"})
    ws.on_open = on_open
    ws.run_forever(ping_interval=PING_INTERVAL)

    return server_payload