import discord
from mcstatus import MinecraftServer
import os
import conf.config as cf

TOKEN = cf.token

MINECRAFT_SERVER_DOMAIN = cf.domain
MINECRAFT_SERVER_PORT = cf.port

# Botのインスタンスを作成
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!status'):
        try:
            # Minecraftサーバのステータスを取得
            server = MinecraftServer.lookup(f"{MINECRAFT_SERVER_DOMAIN}:{MINECRAFT_SERVER_PORT}")
            status = server.status()
            
            # メッセージを作成
            response = (
                f"サーバはオンラインです！\n"
                f"プレイヤー数: {status.players.online}/{status.players.max}\n"
                f"ラグ: {status.latency}ms"
            )
        except Exception as e:
            response = f"サーバに接続できませんでした。エラー: {e}"

        await message.channel.send(response)

client.run(TOKEN)