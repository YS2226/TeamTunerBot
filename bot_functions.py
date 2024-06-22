import discord
import json

class DiscordBot:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = int(channel_id)
        self.client = discord.Client(intents=discord.Intents.default())

        @self.client.event
        async def on_ready():
            print(f'We have logged in as {self.client.user}')

        @self.client.event
        async def on_message(message):
            if message.channel.id == self.channel_id:
                await self.handle_message(message)

    async def handle_message(self, message):
        # Example message handler
        if message.content.startswith('!json'):
            try:
                with open('data.json', 'r') as file:
                    data = json.load(file)
                    await message.channel.send(json.dumps(data, indent=4))
            except Exception as e:
                await message.channel.send(f'Error: {e}')

    def run(self):
        self.client.run(self.token)
