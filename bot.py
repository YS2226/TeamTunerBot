#please get your own discord token and channel id. Thx :)

import discord
from dotenv import load_dotenv
import json
import os
from discord.ext import commands,tasks
import websockets
import asyncio


load_dotenv()

# Load bot token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
WS_URL = 'ws://localhost:8080'
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
print("channel",CHANNEL_ID)


# Initialize client with intents
intents = discord.Intents.default()
intents.members = True  # Enable the members intent to access member information

bot = commands.Bot(command_prefix='!', intents=intents)

async def websocket_handler():
    try:
        async with websockets.connect(WS_URL) as websocket:
            print('Connected to WebSocket server')
            while True:
                message = await websocket.recv()
                print(type(message))
                if message == "1":
                    print(f"解決したと出るメッセージ: {message}")
                    if channel:
                        await channel.send(f"上の問題は解決されました!")
                else:
                    parsed_message = json.loads(message)
                    if isinstance(parsed_message, dict) and 'source' in parsed_message:
                        if parsed_message['source'] == 'vscode':
                            print(f"Received from WebSocket server: {parsed_message['language']}")
                            channel = bot.get_channel(int(CHANNEL_ID))
                            if channel:
                                solvedName = parsed_message['memberName']
                                await process_json(parsed_message['memberName'], parsed_message['language'], parsed_message['message'])

                # if not isinstance(message, str):
                #     parsed_message = json.loads(message)
                #     if isinstance(parsed_message, dict) and 'source' in parsed_message:
                #         if parsed_message['source'] == 'vscode':
                #             print(f"Received from WebSocket server: {parsed_message['language']}")
                #             channel = bot.get_channel(int(CHANNEL_ID))
                #             if channel:
                #                 await process_json(parsed_message['memberName'], parsed_message['language'], parsed_message['message'])
                # else :
                #     print(f"解決したと出るメッセージ: {message}")
                #     print(f"解決したと出るメッセージ: {message}")
                #     if message == '解決した':
                #         if channel:
                #             await channel.send(f"解決しました")
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed, retrying in 5 seconds...")
        await asyncio.sleep(5)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')
    #await process_json('data.json')
    bot.loop.create_task(websocket_handler())


#@tasks.loop(seconds=0.5)  # Run every 0 seconds
async def process_json(name, language, error_script):
    try:
        channel = bot.get_channel(int(CHANNEL_ID))
        if channel is None:
            print(f"Channel with ID {CHANNEL_ID} not found")
            return

        # Find the role based on the language
        guild = channel.guild
        role = discord.utils.get(guild.roles, name=language)
        if role is None:
            print(f"Role '{language}' not found")
            await channel.send(f"{language}を使える人がいないのでロールを新しく付与してください")

            return

        # Mention members with the specified role
        members = role.members
        if not members:
            await channel.send(f"{language}を使える人がいないのでロールを新しく付与してください")
            return
        await channel.send(" ".join(user.mention for user in members) + f" \n {name}さんが助けを求めています！\n エラーコード: {error_script}")

    except FileNotFoundError:
        print("data.json file not found")
    except json.JSONDecodeError:
        print("Invalid JSON in data.json")
    except KeyError as e:
        print(f"Key not found in JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await channel.send(f'{user.mention} がお助けします')
    async with websockets.connect(WS_URL) as websocket:
        await websocket.send(json.dumps({'source': 'discord', 'message': f'{user.display_name} がお助けします'}))
        print(f'{user.display_name} がお助けします')

bot.run(TOKEN)


