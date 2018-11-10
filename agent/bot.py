import requests as request
from telethon import TelegramClient, events, sync
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from config.main import api_id, api_hash

client = TelegramClient('session_name', api_id, api_hash)
client.start()
try:
  result = client.send_message('@gex_bot', 'start')
  print(result)
except Exception as exception:
  print(exception)

