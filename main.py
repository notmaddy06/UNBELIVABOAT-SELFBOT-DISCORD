from asyncio import sleep
from discord import Client, Message, TextChannel
from discord.ext import tasks

guild_ids = [
    1209956399073992745
]  # Only servers where the commands will work in (safety feature).

specific_user_id = 123456789012345678  # Replace with the specific user's ID

@tasks.loop(minutes=15)  # Example interval for the commands, adjust as needed
async def auto_commands(channel: TextChannel):
    await channel.send('$work')  # Send the work command
    await sleep(4)  # Wait for 4 seconds
    await channel.send('$collect')  # Send the collect command
    await sleep(4)  # Wait for 4 seconds
    await channel.send('$dep all')  # Send the deposit command

client = Client()  # Define client session

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")  # Let the user know that it's running

@client.event
async def on_message(message: Message):
    if message.guild.id in guild_ids and message.author.id == client.user.id:
        if message.content == "!start":  # Start commands
            await message.delete()  # Delete command message
            if auto_commands.is_running():  # Checks if commands are already running
                auto_commands.restart(message.channel)  # Restarts commands if already running
            else:
                auto_commands.start(message.channel)  # Starts commands if not running
        elif message.content == "!stop":  # Stop commands
            await message.delete()  # Delete command message
            auto_commands.stop()  # Stop commands

    # Check if the bot is mentioned in the specific channel by the specific user
    if message.channel.id == 1210689910533660802 and client.user in message.mentions:
        if message.author.id == 778526555856961540: # Check if the specific user mentioned the bot
            await message.channel.send('$dep all')  # Send the deposit command when mentioned by the specific user

client.run("TOKEN")
