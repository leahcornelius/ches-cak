import discord
import csv
import time
import random
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
from create_chatbot_instance import new_ches_cak
# from ttb import ttb
# from stt import read
import requests
import json
import sys
import os
from color import color
from datetime import datetime
from format_out import format_out
from format_out import games
from bot_conf import TOKEN, mention
statuses = [discord.Status.offline, discord.Status.online, discord.Status.idle, discord.Status.do_not_disturb]
# Create a new chat bot named ches cak
chatbot = new_ches_cak()
client = discord.Client()
recent_res_to = []
recent_res_to_max_size = 500


def accept_invite(INVITE_LINK):
    url = 'https://discordapp.com/api/v6/invite/'+INVITE_LINK+'?with_counts=true'
    print(url)
    headers = {"content-type": "application/json", "Authorization": TOKEN}

    r = requests.post(url, headers=headers)


def de(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii').replace(mention, "")


@client.event
async def on_ready():
    print(color.GREEN, 'Logged in as {0.user}'.format(client), color.END)


def remove_mute(user):
    for user_list in mutes:
        if user_list == user:
            mutes.remove(user)


@client.event
async def on_message(message):
    if is_mute(message.author.name):
        if message.content.strip() != "speak to me " + mention:
            print("Message from user who has muted us: ", message.author.name,
                  " and not a unmute message (msg: ", message.content, ")")
            return
        else:
            remove_mute(message.author.name)
            message.author.send(
                "Ok im now responding to your messages again. To undo this say stop messaging me @ches cak")
            return
    if message.author.bot:
        return
    if message.author == client.user:
        return
    if message.content.strip() == "stop messaging me " + mention:
        mutes.append(message.author.name)
        message.author.send(
            "Ok im no longer responding to your messages. To undo this say: speak to me @ches cak")
        return
    if message.content.startswith('https://discord.gg'):
        print(message.content.split('.gg/'))
        accept_invite(message.content.split('.gg/')[1])
        message.author.message("i joined your server! Thaks for sharing!")
        return
    if message.content.startswith('https://discord.com'):
        print(message.content.split('.com/'))
        accept_invite(message.content.split('.com/')[1])
        message.author.message("i joined your server! Thanks for sharing!!")
        return
    if client.user not in message.mentions:
        if len(message.mentions) != 0:
            return
    if de(message.content).strip() == '':
        return
    if not message.guild is None:
        print('New message from guild: ', message.guild.name, ', in channel: ',
              message.channel.name, ', from user: ', message.author.name)
    else:
        print('New DM from user: ', message.author.name)
    response = chatbot.get_response(message.content)
    a = color.GREEN if response.confidence > 0.4 else color.RED
    now = datetime.now()
    print(now.strftime("%H:%M:%S"), ':', color.BOLD, 'Incoming message: ', color.END, color.YELLOW, message.content, color.END, ' (sent at ', message.created_at.strftime("%H:%M:%S"), ')',
          color.BOLD, 'Our response: ', color.END, color.PURPLE, response.text, color.END)
    print(color.BLUE, 'Confidence: ', response.confidence, a,
          'Would say: ', response.confidence > 0.4, color.END)
    if response.confidence < 0.4:
        return
    if len(response.text) > 1:
        res = response.text
        async with message.channel.typing():
            time.sleep(random.randrange(1, 5))
            await message.channel.send(format_out(res, message))
            if len(recent_res_to) >= recent_res_to_max_size:
                recent_res_to.pop(0)
            recent_res_to.append(de(message.content).strip())


@client.event
async def on_message_edit(before, after):
    if de(before.content).strip() not in recent_res_to:
        response = chatbot.get_response(after.content)
        if not after.guild is None:
            print('Edited message from guild: ', after.guild.name, ', in channel: ',
                after.channel.name, ', from user: ', after.author.name)
        else:
            print('Edited DM from user: ', after.author.name)
        a = color.GREEN if response.confidence > 0.4 else color.RED
        print(color.BOLD, 'Before: ', color.END, color.YELLOW, before.content, color.END,
              color.BOLD, 'After: ', color.END, color.YELLOW, after.content, color.END,
            color.BOLD, 'Our response (to edit): ', color.END, color.PURPLE, response.text, color.END)
        print(color.BLUE, 'Confidence: ', response.confidence, a,
            'Would say: ', response.confidence > 0.4, color.END)
        if response.confidence < 0.4:
            return
        elif len(response.text) > 1:
            res = response.text
            async with after.channel.typing():
                time.sleep(random.randrange(2, 10))
                await after.channel.send(format_out(res, after))
                if len(recent_res_to) > recent_res_to_max_size:
                    recent_res_to.pop()
                recent_res_to.append(de(after.content).strip())


@client.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.channels, name="general")
    if channel == None:
        channel = discord.utils.get(
            guild.channels, name="introductions")
        if channel == None:
            channel = discord.utils.get(
                guild.channels, name="offtopic")
    if channel != None:
        greet_strings = ['Hello', 'hi everyone', 'hey guys',
                         'is anyone online? :D', 'hello everyone!!']
        await channel.send(random.choice(greet_strings))
        bot_msg = [
            'i am an ai that learns by engaging in conversations (i am a bot) if you do not like that feel free to kick me. Other wise it would be great if you would talk with me',
            'i am a bot that learns by talking - wanna help out? talk with me and DM me or message me invites of servers which i will join.'
        ]
        await channel.say(random.choice(bot_msg))


def handle_mute(user):
    if user in mutes:
        return
    else:
        mutes.append(user)


def is_mute(user):
    if user in mutes:
        return True
    else:
        return False


@client.event
async def on_guild_remove(guild):
    print(color.RED, color.BOLD, 'I have been removed from ',
          guild.name, color.END, color.END)
    with open('bans.csv', mode='w') as ban_file:
        ban_writer = csv.writer(ban_file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        now = datetime.now()
        ban_writer.writerow(
            [now.strftime("%Y-%m-%d %H:%M:%S"), guild.name.strip()])

print('Loading cache from drive')
bans = [[]]
with open('bans.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',',
                         quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in readCSV:

        print(color.RED, 'FOUND BAN AT:',
              row[0], ', from server: ', row[1], color.END)
        bans.append([row[0], row[1]])

print("Loaded bans (count: ", len(bans), "). Moving onto mute logs")
mutes = []
with open('mutes.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',',
                         quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in readCSV:
        if row[0] != None:
           print(color.RED, 'User : ', row[0], ' has muted us', color.END)
           bans.append(row[0])
print("Loaded all ", len(mutes), " user's names who have muted us")
print("Connecting to discord...")
client.run(TOKEN, bot=False)
print("connected")
game = discord.Game(random.choice(games))
client.change_presence(status=random.choice(statuses), activity=game)
while True:
  mytime=time.localtime()
  if mytime.tm_hour < 6 or mytime.tm_hour > 18:
      time.sleep(60)
  else:
      time.sleep(60*60*random.randrange(0.1, 3))
      game=discord.Game(random.choice(games))
      client.change_presence(status=random.choice(statuses), activity=game)
