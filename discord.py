import discord
import mcstatus
import boto3
import os
import conf.config as cf

from mcstatus import MinecraftServer
from discord import app_commands

import paramiko
import time
import asyncio

TOKEN = cf.token

MINECRAFT_SERVER_DOMAIN = cf.domain
MINECRAFT_SERVER_PORT = cf.port

AWS_ACCESS_KEY = cf.aws_access_key
AWS_SECRET_ACCESS_KEY = cf.aws_secret_key
AWS_REGION_NAME = cf.region_name
AWS_INSTANCE_ID = cf.instance_id

EC2_KEY_PAIR_FILE = cf.key_pair_file  # EC2インスタンスのキーペアファイル（.pemファイル）
EC2_USERNAME = cf.username  # EC2インスタンスに接続するためのユーザー名
MINECRAFT_DOCKER_IMAGE = cf.minecraft_docker_image  # MinecraftサーバーのDockerイメージ
MINECRAFT_CONTAINER_NAME = cf.minecraft_container_name  # MinecraftサーバーのDockerコンテナ名

# Botのインスタンスを作成(初期化)
intents = discord.Intents.default() #botが土の種類のイベントに反応するか
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client) #スラッシュコマンド用

#ec2クライアント設定
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

@client.event
async def on_ready():
    print('ログインしました')
    
    new_activity = f"テスト"
    await client.change_presence(activity=discord.Game(new_activity))
    
    #スラッシュコマンドの同期
    await tree.sync() 
    
#/コマンド @テスト
#name:打つコマンド名 description:discordで見える説明
@tree.command(name = "test", description="テストって言うテスト")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("ちんちん")
    
#サーバー起動&起動したか確認
@tree.command(name = "start", description="サーバーを起動する")
async def test(interaction: discord.Interaction):
    try:
        response = ec2_client.start_instances(InstanceIds=[AWS_INSTANCE_ID])
        await interaction.response.send_message("起動開始")
        statuses = response.get('InstanceStatuses', [])
        
        if not statuses:
            status_message = "寝てる"
            await client.change_presence(status=discord.Status.dnd, activity=discord.CustomActivity(name="Zzz..."))
        else:
            status_message = "起きてる"
            await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="オンライン"))
        await interaction.response.send_message(status_message)
        
    except Exception as e:
        await interaction.response.send_message("なんもわからん")
        await client.change_presence(status=discord.Status.dnd, activity=discord.CustomActivity(name="Zzz..."))

    
client.run(TOKEN)