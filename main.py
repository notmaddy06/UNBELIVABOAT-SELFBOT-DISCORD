import logging
from asyncio import sleep
from discord import Client, Message, TextChannel
from discord.ext import tasks

logging.basicConfig(level=logging.INFO)

guild_ids = [
    1209956399073992745
]  # Only servers where the commands will work in (safety feature).

specific_user_id = 'GUILD ID'  # Replace with the specific user's ID

@tasks.loop(minutes=15)  # Example interval for the commands, adjust as needed
async def auto_commands(channel: TextChannel):
    try:
        await channel.send('$work')  # Send the work command
        await sleep(4)  # Wait for 4 seconds
        await channel.send('$collect')  # Send the collect command
        await sleep(4)  # Wait for 4 seconds
        await channel.send('$dep all')  # Send the deposit command
        await sleep(3)  # Wait for 3 seconds before the next $dep all command
    except Exception as e:
        logging.error(f"Error in auto_commands: {e}")

client = Client()  # Define client session

@client.event
async def on_ready():
    logging.info(f"We have logged in as {client.user}")  # Let the user know that it's running

@client.event
async def on_message(message: Message):
    try:
        if message.guild and message.guild.id in guild_ids and message.author.id == client.user.id:
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
        if message.channel.id == 'CHANNELID' and client.user in message.mentions:
            if message.author.id == 'USERID':  # Check if the specific user mentioned the bot
                await sleep(3)  # Wait for 3 seconds before sending the deposit command
                await message.channel.send('$dep all')  # Send the deposit command when mentioned by the specific user
    except Exception as e:
        logging.error(f"Error in on_message: {e}")

@client.event
async def on_disconnect():
    logging.warning("Bot disconnected. Attempting to reconnect...")

@client.event
async def on_resumed():
    logging.info("Bot reconnected successfully.")

client.run("TOKEN")
