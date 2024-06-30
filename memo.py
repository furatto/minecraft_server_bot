#/コマンドで実装する

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!status'):
        try:
            response = ec2_client.describe_instance_status(InstanceIds=[AWS_INSTANCE_ID])
            statuses = response.get('InstanceStatuses', [])

            if not statuses:
                status_message = "サーバーは停止しています。"
            else:
                instance_state = statuses[0].get('InstanceState', {}).get('Name', 'unknown')
                status_message = f"サーバーの状態: {instance_state}"

            await message.channel.send(status_message)
        
        except Exception as e:
            await message.channel.send(f"サーバーの状態を取得できませんでした: {str(e)}")

        await message.channel.send(response)

    if message.content.startswith("!open"):
        