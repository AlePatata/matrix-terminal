import asyncio
import getpass
from datetime import datetime

from nio import AsyncClient, RoomMessageText

matrix_server = "https://fjara.cl"
usr = "alepatata"
room_id = "!JcyXcqJpFionRkCrPM:fjara.cl"

client = AsyncClient(matrix_server, usr)
priv_rooms = []
start_time = None


async def mandar_msg(msg):
    await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content={"msgtype": "m.text", "body": msg},
    )


def listens_for_logs(room, event):
    if event.server_timestamp < start_time:
        return
    id = room.room_id
    if id != room_id:
        return
    message_text = event.body
    for line in message_text.strip().splitlines():
        print(line)
    print("responder? ")


async def listener():
    client.add_event_callback(listens_for_logs, RoomMessageText)
    await client.sync_forever(timeout=30000)


async def main():
    psw = getpass.getpass("pass: ")
    res = await client.login(psw)
    print(res)

    global start_time
    start_time = datetime.now().timestamp() * 1000

    listener_task = asyncio.create_task(listener())

    while True:
        message = await asyncio.to_thread(input, "responder? ")
        if message == ":q":
            break

        await mandar_msg(message)

    listener_task.cancel()
    await client.logout()
    await client.close()


asyncio.run(main())
