import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


load_dotenv()

# 必要なintentsを有効にする
intents = discord.Intents.default()
intents.members = True  # メンバー関連のイベントを取得するために必要

# ボットのプレフィックスを設定し、intentsを渡す
bot = commands.Bot(command_prefix='', intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # ボットが自分自身のメッセージに反応しないようにする
    if message.author == bot.user:
        return

    # 特定のメッセージに反応する例
    if message.content.startswith('hello'):
        await message.channel.send(f'Hello, {message.author.mention}!')

    # コマンドも処理するためにこれを追加
    await bot.process_commands(message)

@bot.command()
async def greet(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command()
async def mention_role(ctx, role: discord.Role):
    members = role.members
    if not members:
        await ctx.send(f"No members with the role {role.name}.")
        return

    for member in members:
        await ctx.send(f"{member.mention}, you have been mentioned!")

bot.run(TOKEN)






