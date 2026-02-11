import json
import asyncio
from datetime import datetime
from nio import AsyncClient, RoomMessageText
import getpass

matrixServer = "https://fjara.cl"
usr = "alepatata"
room_id = "!JcyXcqJpFionRkCrPM:fjara.cl"

client = AsyncClient(matrixServer, usr)
privRooms = []
startTime = None


async def mandar_msg(msg):
    await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body":msg 
        }
    )


def listensForLogs(room, event):
    if event.server_timestamp < startTime:
        return
    id = room.room_id
    if id != room_id:
        return
    messageText = event.body
    for line in messageText.strip().splitlines():
        print(line)
    print("responder? ")


async def listenerFunction():
    client.add_event_callback(listensForLogs, RoomMessageText)
    await client.sync_forever(timeout=30000)

async def main():
    psw = getpass.getpass("pass: ")
    res = await client.login(psw)
    print(res)

    global startTime
    startTime = datetime.now().timestamp() * 1000

    listener_task = asyncio.create_task(listenerFunction())

    while True:
        message = await asyncio.to_thread(input, "responder? ")    
        if message == ":q":
            break
        
        await mandar_msg(message)

            
    listener_task.cancel()
    await client.logout()
    await client.close()


asyncio.run(main())

