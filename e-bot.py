import os
import time
from datetime import datetime, timedelta
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = int(os.getenv('DISCORD_CHANNEL'))
client = discord.Client()
lastThree = []
    
# on bot startup
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

# check e channel
@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    elif message.channel.id == CHANNEL:

        # terminal response
        print('POST:', message.author, message.content, len(message.content))

        # check that message is 
        if len(str(message.content)) != 1:
            time.sleep(0.5)
            print("!!! message is not correct!")
            await message.delete()
            await message.author.edit(timed_out_until=(datetime.now() + timedelta(minutes=10)),
            reason='For breaking the rules of the sacred e channel.')

        # check that the message is "correct":
        elif ord(message.content) != ord('e'):
            time.sleep(0.5)
            print("!!! message is not correct!")
            await message.delete()
            await message.author.edit(timed_out_until=(datetime.now() + timedelta(minutes=10)),
            reason='For breaking the rules of the sacred e channel.')

        # no spamming e rule:
        elif str(message.author) in lastThree:
            time.sleep(0.5)
            print('!!! message was spammed!')
            await message.delete()
            await message.author.edit(timed_out_until=(datetime.now() + timedelta(minutes=10)),
            reason='For posting messages too quickly in the sacred e channel.')

        # message not a reference
        elif message.reference is not None:
            time.sleep(0.5)
            print('!!! message has a reference!')
            await message.delete()
            await message.author.edit(timed_out_until=(datetime.now() + timedelta(minutes=10)),
            reason='For breaking the rules of the sacred e channel.')

        # a good post happened
        else:
            if len(lastThree) >= 2:
                lastThree.append(str(message.author))
                lastThree.pop(0)
            else:
                lastThree.append(str(message.author))

        print('last three good posters ->', lastThree)
        print('-------------------------')



@client.event
async def on_message_edit(message_before, message_after):
    if message_after.author == client.user or message_before.author == client.user:
        return
    elif message_after.channel.id == CHANNEL:

        # terminal response
        print('EDIT:', message_after.author, message_after.channel.id, message_after.content)

        # check that the message is "correct"
        if len(message_after.content) != 1 or ord(message_after.content) != ord('e'):
            time.sleep(1)
            print('!!! message was edited!')
            await message_after.delete()
            await message_after.author.edit(timed_out_until=(datetime.now() + timedelta(minutes=10)),
            reason='For trying to edit a previous message in the sacred e channel.')

        # check if reference was added through edit
        elif message_after.reference is not None:
            time.sleep(1)
            print('!!! message has a reference!')
            await message_after.delete()
            await message_after.author.edit(timed_out_until=(datetime.now() + timedelta(minutes=10)),
            reason='For breaking the rules of the sacred e channel.')
    
client.run(TOKEN)