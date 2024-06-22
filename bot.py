import discord
from dotenv import load_dotenv
import json
import os
import sys

load_dotenv()

# Load bot token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize client with intents
intents = discord.Intents.default()
intents.members = True  # Enable the members intent to access member information
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
    # Check if arguments are provided for sending a message
    if len(sys.argv) > 2:
        CHANNEL_ID = int(sys.argv[1])
        MESSAGE = sys.argv[2]
        await send_message(CHANNEL_ID, MESSAGE)

# Load JSON data
with open('data.json', 'r') as file:
    data = json.load(file)
    role_name = data['ppl1']

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await channel.send(f'{user.mention} がお助けします')

async def send_message(channel_id, message):
    channel = client.get_channel(channel_id)
    if channel:
        await channel.send(message)
        #TODO ここにVsCodeから情報を受け取ったときの処理を追加
    else:
        print(f"Error: Channel with ID {channel_id} not found")
        await client.close()

client.run(TOKEN)
