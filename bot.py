#please get your own discord token and channel id. Thx :)

import discord
from dotenv import load_dotenv
import json
import os
from discord.ext import commands,tasks


load_dotenv()

# Load bot token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL =os.getenv('CHANNEL_ID')
print("channel",CHANNEL)

# Initialize client with intents
intents = discord.Intents.default()
intents.members = True  # Enable the members intent to access member information

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')
    await process_json('data.json')


#@tasks.loop(seconds=0.5)  # Run every 0 seconds
async def process_json(file):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        
        name = data['error_info'][0]['name']
        language = data['error_info'][0]['file_format']
        error_script = data['error_info'][0]['error_type']
        
        channel = bot.get_channel(int(CHANNEL))
        if channel is None:
            print(f"Channel with ID {CHANNEL} not found")
            return

        # Find the role based on the language
        guild = channel.guild
        role = discord.utils.get(guild.roles, name=language)
        if role is None:
            print(f"Role '{language}' not found")
            
            return

        # Mention members with the specified role
        members = role.members
        if not members:
            await channel.send(f"{language}を使える人がいないのでロールを新しく付与してください")
            return

        for member in members:
            await channel.send(f"{member.mention}, {name}さんが助けを求めています！エラーコード: {error_script}")

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


bot.run(TOKEN)


