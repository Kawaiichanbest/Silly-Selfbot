import discord
import os
import urllib.parse
import requests
import base64
import hashlib
import json
import time
import asyncio
import threading
import random
import string
from winotify import Notification, audio
from pypresence import Presence
from datetime import datetime
from colorama import Fore
from pystyle import Colorate, Colors, Center
from discord.ext import commands

# Define key functions

def clear():
    os.system("cls") if os.name == "nt" else os.system("clear")

def title(args=None):
    os.system("title Silly Selfbot") if args == None else os.system(f"title Silly Selfbot [$] {args}")




def load_settings():
    with open('Settings/config.json', 'r') as f:
        config = json.load(f)
        TOKEN = config.get('TOKEN')
        PREFIX = config.get('PREFIX')
        return TOKEN, PREFIX

def load_theme():
    with open('Settings/theme.json', 'r') as f:
        settings = json.load(f)
        AUTHOR = settings.get('AUTHOR')
        IMAGE = settings.get('EMBED-IMAGE')
        COLOR = settings.get('COLOR')
        return AUTHOR, IMAGE, COLOR


scripts = []
def load_scripts():
  clear()
  for file in os.listdir("Scripts"):
    if file.endswith('.py'):
      x = open(f"Scripts/{file}", 'r').read()
      x = f"{file}ΘθΘ{x}"
      scripts.append(x)  

def execute_scripts():
    for script in scripts:
        name_with_ex = script.split('ΘθΘ')[0]
        name = name_with_ex.split('.py')[0]
        code = script.split('ΘθΘ')[1]
        exec(code)
        print(f"[~] Loaded script: {name}")
        time.sleep(1)


def window_notif(appid, title, msg, doaudio=False):
    toast = Notification(app_id=appid, title=title, msg=msg)
    if doaudio != False:
        toast.set_audio(audio.Default, loop=False)
    toast.show()


def getfriends():
    url = "https://discord.com/api/v9/users/@me/relationships"
    r = requests.get(url, headers=global_headers)
    decode = r.json()
    friends = [user for user in decode if user.get('type') == 1]
    pending = [user for user in decode if user.get('type') == 4]
    blocked = [user for user in decode if user.get('type') == 2]
    toreturn = f"{Fore.GREEN}{len(friends)}{Fore.RESET}/{Fore.YELLOW}{len(pending)}{Fore.RESET}/{Fore.RED}{len(blocked)}{Fore.RESET}"
    return toreturn

def getcommandscount():
    with open('main.py', 'r', encoding='utf-8') as f:
        commandscount = 0 
        lines = f.read().splitlines()
        for line in lines:
            if "@bot.command()" in line:
                commandscount += 1
    return commandscount



# have to define here for embed reasons

TOKEN, PREFIX = load_settings()
AUTHOR, IMAGE, COLOR = load_theme()


def make_embed(content, title, section, image=None):
    parsedcontent = urllib.parse.quote(content)
    parsedtitle = urllib.parse.quote(title)
    parsedauthor = urllib.parse.quote(AUTHOR)
    parsedcolor = urllib.parse.quote(COLOR)
    url = f"**[Silly Selfbot]** {section}{PIPES}https://embedl.ink/?deg&provider=&providerurl=&author={parsedauthor}&title={parsedtitle}&color={parsedcolor}&media=thumbnail&mediaurl={image}&desc={parsedcontent}"
    return url

# Define key variables
#d
#

SUS_WORDS = ['nighty', 'ethone', 'astolfo']
PIPES = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
ASCII_ART = """
 ____  __  __    __    _  _    ____  ____  __    ____  ____   __  ____ 
/ ___)(  )(  )  (  )  ( \/ )  / ___)(  __)(  )  (  __)(  _ \ /  \(_  _)
\___ \ )( / (_/\/ (_/\ )  /   \___ \ ) _) / (_/\ ) _)  ) _ ((  O ) )(  
(____/(__)\____/\____/(__/    (____/(____)\____/(__)  (____/ \__/ (__) 
>---------------------------------------------------------------------<
"""

global_headers = {
    'authorization' : TOKEN,
    'authority': 'discord.com',
    'accept': '*/*',
    'accept-language': 'sv,sv-SE;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://discord.com',
    'referer': 'https://discord.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36',
    'x-debug-options': 'bugReporterEnabled',
    'x-discord-locale': 'sv-SE',
    'x-discord-timezone': 'Europe/Stockholm',
}    


# Setup discord shit

bot = commands.Bot(command_prefix=PREFIX, self_bot=True)
bot.remove_command("help")


@bot.event
async def on_ready():
    window_notif("Silly Selfbot", "Silly Selfbot is ready", f"Logged in as: {bot.user.name}", True)
    load_scripts()
    execute_scripts()
    clear()
    title()
    cform = getfriends()
    cmdcount = getcommandscount()
    print(Colorate.Vertical(Colors.blue_to_purple, Center.XCenter(ASCII_ART)))
    print(f"\n[{Fore.LIGHTMAGENTA_EX}?{Fore.RESET}] Username: {bot.user.name}")
    print(f"[{Fore.LIGHTMAGENTA_EX}?{Fore.RESET}] Connected at: {datetime.now().strftime('%H:%M')}")
    print(f"[{Fore.LIGHTMAGENTA_EX}?{Fore.RESET}] Friend count: {cform}")
    print(f"[{Fore.LIGHTMAGENTA_EX}?{Fore.RESET}] Server count: {len(bot.guilds)}")
    print(f"[{Fore.LIGHTMAGENTA_EX}?{Fore.RESET}] Loaded {cmdcount} commands")

@bot.event
async def on_command_error(ctx, error):
    print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} {Fore.RED}[{Fore.RESET}!{Fore.RED}]{Fore.RESET} A Fatal error occured {error}")

@bot.event
async def on_message_delete(message):
    if bot.user.mentioned_in(message):
        if "@everyone" not in message.content:
            print(f"""\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Ghost ping detected!!
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} User: {message.author} | {message.author.id}
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Channel: {message.guild} | {message.channel}""")


@bot.event
async def on_message(message: discord.Message):
    if "discord.gift/" in message.content:
        gift_id = message.content.split('/')[-1]
        if len(gift_id) > 16:
            print(f"""\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Nitro Detected !!
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Code: discord.gift/{gift_id}
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} User: {message.author} | {message.author.id}
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Channel: {message.guild} | {message.channel }""")

    elif "selfbot" in message.content:
        if message.author.id != bot.user.id:
            print(f"""\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Possible selfbot user detected !!
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Offending item: {message.content}
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} User: {message.author} | {message.author.id}
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Channel: {message.guild} | {message.channel}""")
    
    elif message.author.name == "GiveawayBot" and message.author.discriminator == "2381":
        start_time = datetime.now()
        url = "https://discord.com/api/v9/interactions"
        data = {
            "type": 3,
            "guild_id": str(message.guild.id),
            "channel_id": str(message.channel.id),
            "message_id": str(message.id),
            "application_id": "294882584201003009",
            "session_id": bot.http.token,
            "data": {
                "component_type": 2,
                "custom_id": "enter-giveaway"
            }   
        }
        r = requests.post(url, headers=global_headers, json=data)
        if r.status_code == 204:
            taken_time = datetime.now() - start_time
            print(f"""\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Joined giveaway
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} User: {message.author} | {message.author.id}
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Channel: {message.guild} | {message.channel}
{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}] {Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}]{Fore.RESET} Successfully joined in {taken_time}""")

    else:
        await bot.process_commands(message)

# >----------------<
#  Help commands
# >----------------<

@bot.command()
async def HELP(ctx):
    await ctx.message.delete()
    help_content = f"""
{PREFIX} [section] [page] ? Default is 1
>------------------------------------<
{PREFIX}RAID      ? Raid commands
{PREFIX}RECON     ? Recon commands
{PREFIX}CRACKING  ? Cracking commands
{PREFIX}UTILITIES ? Utility commands
{PREFIX}FUN       ? Fun commands
{PREFIX}TROLL     ? Troll commands
{PREFIX}ACCOUNT   ? Account commands
"""
    url = make_embed(help_content, "Help pg.1", "Help", IMAGE)
    await ctx.send(url)

@bot.command()
async def RAID(ctx, page: int):
    await ctx.message.delete()
    page_1_help_content = f"""
{PREFIX}chatspam [message] [amount] ? Spam chat messages
{PREFIX}threadspam [name] [amount]  ? Spam threads
{PREFIX}spamchannels [name] [count] ? Spam channels
{PREFIX}spamroles [name] [count]    ? Spam roles
{PREFIX}pinspam [count]             ? Spam pins
{PREFIX}speedchanspam [count]       ? Spams channel very fast (BUGGY)
{PREFIX}deleteroles                 ? Delete all roles
"""
    
    page_2_help_content = f"""
{PREFIX}deletechannels                       ? Delete all channels
{PREFIX}speedchatspam [channel ID] [message] ? Spam fast
{PREFIX}webraid [message] [channel count]    ? Raid a server with hooks
{PREFIX}renamechans [name]                   ? Rename all text channels
{PREFIX}renamevc [name]                      ? Rename all voice channels
"""

    page_3_help_content = f"""
{PREFIX}renamecat [name] ? Rename all categorys
{PREFIX}eventspam [location] [name] [description] [count < 10] ? Spam events    
    
    """

    if page == 1:
        url = make_embed(page_1_help_content, "Raid pg.1", "Raid", IMAGE)
    elif page == 2:
        url = make_embed(page_2_help_content, "Raid pg.2", "Raid", IMAGE)
    elif page == 3:
        url = make_embed(page_3_help_content, "Raid pg.3", 'Raid', IMAGE)
    await ctx.send(url)   


@bot.command()
async def RECON(ctx, page: int):
    await ctx.message.delete()
    page_1_help_content = f"""
{PREFIX}serverinfo ? Get the current servers info
"""
    if page == 1:
        url = make_embed(page_1_help_content, "Recon pg.1", "Recon", IMAGE)
    await ctx.send(url)

@bot.command()
async def CRACKING(ctx, page: int):
    await ctx.message.delete()
    page_1_help_content = f"""
{PREFIX}hashforce [hash] [algorithm] [wordlist] ? Crack a hash
"""
    if page == 1:
        url = make_embed(page_1_help_content, "Cracking pg.1", "Cracking", IMAGE)
    await ctx.send(url)

@bot.command()
async def UTILITIES(ctx, page: int):
    await ctx.message.delete()
    page_1_help_content = f"""
{PREFIX}setplaying [game]       ? Set playing
{PREFIX}setstream [user] [game] ? Pretend to stream
{PREFIX}setlisten [rpc]         ? Fake listening rpc
{PREFIX}setwatch  [rpc]         ? Fake watching rpc
{PREFIX}whois [@user]           ? Get info on a user
{PREFIX}invmake <channel ID>    ? Make an invite
"""
    if page == 1:
        url = make_embed(page_1_help_content, "Utilities pg.1", "Utilities", IMAGE)
    await ctx.send(url)

@bot.command()
async def FUN(ctx, page: int):
    await ctx.message.delete()
    page_1_help_content = f"""
{PREFIX}sing [song file] [delay] ? Sing a song
{PREFIX}role_anim [count] [user] ? Animated roles    
{PREFIX}lyricslist               ? List all lyrics files                                                                        
"""
    if page == 1:
        url = make_embed(page_1_help_content, "Fun pg.1", "Fun", IMAGE)
    await ctx.send(url)

@bot.command()
async def TROLL(ctx, page: int):
    await ctx.message.delete()
    page_1_help_content = f"""
{PREFIX}tokensniff [@user]                ? Sniff a users token
{PREFIX}spamaddgc [userid] [count]        ? Spam add a user to a gc
"""
    if page == 1:
        url = make_embed(page_1_help_content, "Troll pg.1", "Troll", IMAGE)
    await ctx.send(url)

@bot.command()
async def ACCOUNT(ctx, page: int):
    await ctx.message.delete()
    page_1_help_content = f"""
{PREFIX}changebio [content] ? Change BIO
{PREFIX}changeproniuns [new] ? Change pronouns
{PREFIX}changestatus [status] ? Change your status
"""
    if page == 1:
        url = make_embed(page_1_help_content, "Account pg.1", "Account", IMAGE)
    await ctx.send(url)

# >----------------<
#  Raid commands
# >----------------<

@bot.command()
async def chatspam(ctx, message: str, count: int):
    await ctx.message.delete()
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Started chat spamming\n")
    for i in range(count):
        await ctx.send(message)
        print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Message {message} sent | [{i+1}/{count}]")
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Finished chat spamming")

@bot.command()
async def threadspam(ctx, name:str,  count:int):
    await ctx.message.delete()
    headers = {
        'authorization' : TOKEN
    }
    data = {
        'name' : name
    }
    url = f"https://discord.com/api/v9/channels/{ctx.channel.id}/threads"
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Started thread spamming\n")
    for i in range(count):
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 201:
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Thread made | [{i+1}/{count}]")
        else:
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Error occured | [{i+1}/{count}]")
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Finished thread spamming")


@bot.command()
async def pinspam(ctx, count: int):
    await ctx.message.delete()
    pincount = 0
    channel = bot.get_channel(ctx.channel.id)
    history = await channel.history(limit=count).flatten()
    headers = {
        'authorization' : TOKEN
    }
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Started pin spamming\n")
    for message in history:
        pincount += 1
        url = f"https://discord.com/api/v9/channels/{channel.id}/pins/{message.id}"
        r = requests.put(url, headers=headers)
        if r.status_code == 204:
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Pin made | [{pincount}/{count}]")
        else:
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Error occured | [{pincount}/{count}]")
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Finished pin spamming")

@bot.command()
async def deletechannels(ctx):
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Started deleting channels\n")
    chan_count = 0
    for channel in ctx.guild.channels:
        chan_count += 1
        try:
            await channel.delete()
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Deleted {channel} | {chan_count}")
        except Exception as e:
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Failed to delete {channel} | {chan_count}")
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Finished deleting channels")


@bot.command()
async def webraid(ctx, message: str, channe_c: int):
    await ctx.message.delete()
    threads = []
    hooks = []
    channels_created = []
    count_tasks = 1

    for channel in ctx.guild.channels:
        await channel.delete()

    for i in range(channe_c):
        channel = await ctx.guild.create_text_channel(f"『𝐞𝐱𝐞𝐜𝐮𝐭𝐞𝐝』")
        channels_created.append(channel)

    async def send_requests():
        messages_sent = 0
        delay = 0.01
        while messages_sent < 30:
            try:
                for hook in hooks:
                    if messages_sent >= 30:
                        break
                    await hook.send(f"@everyone {message}", avatar_url="https://www.startpage.com/sp/sxpra?url=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fen%2Fthumb%2F6%2F63%2FFeels_good_man.jpg%2F1200px-Feels_good_man.jpg")
                    time.sleep(delay)
                    messages_sent += 1
            except Exception as e:
                pass


    for channel in channels_created:
        webhook = await channel.create_webhook(name=f"♥ Silly Selfbot ♥")
        hooks.append(webhook)

    
    for hook in hooks:
        task = asyncio.create_task(send_requests())
        threads.append(task)

    for i in range(count_tasks):
        await asyncio.gather(*threads)



@bot.command()
async def spamchannels(ctx, name: str, count: int):
    await ctx.message.delete()
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Started spamming channels\n")
    for i in range(count):
        try:
            await ctx.guild.create_text_channel(name)
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Created {name} | {i+1}/{count}")
        except:
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Failed to make {name} | {i+1}/{count}")
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Finished spamming channels")



@bot.command()
async def deleteroles(ctx):
    await ctx.message.delete()
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Started deleting roles\n")
    count = 0
    for role in ctx.guild.roles:
        count += 1
        try:
            await role.delete()
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Deleted {role.name} | {count}")
        except:
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Failed to delete {role.name} | {count}")
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Finished deleting roles")



@bot.command()
async def spamroles(ctx, name: str, count: int):
    await ctx.message.delete()
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Started spamming roles\n")
    for i in range(count):
        try:    
            await ctx.guild.create_role(name=name)
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Created {name} | {i+1}/{count}")
        except:
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Failed to make {name} | {i+1}/{count}")
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Finished spamming roles")

@bot.command()
async def speedchanspam(ctx, count: int):
    print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Started spamming channels\n")
    await ctx.message.delete()
    chan = "『𝐬𝐢𝐥𝐥𝐲 𝐬𝐞𝐥𝐟𝐛𝐨𝐭』"
    def cspam():
        json = {"name": chan}
        r = requests.post(f"https://discord.com/api/v9/guilds/{ctx.guild.id}/channels",headers=global_headers, json=json)
        print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} [+] Debug | SPEEDCHANSPAM | {r.status_code}")
    threads = []

    for i in range(count):
        t = threading.Thread(target=cspam)
        t.start()
        threads.append(t)


    for thread in threads:
        thread.join()

@bot.command()
async def speedchatspam(ctx, id: int, message: str):
    await ctx.message.delete()
    def send():
        for i in range(3):
            data = {
                'content' : message
            }
            url = f"https://discord.com/api/v9/channels/{id}/messages"
            r = requests.post(url, headers=global_headers, json=data)
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} [+] Debug | SPEEDCHATSPAM | {r.status_code} | {i+1}")
    threads = []
    for i in range(10):
        t = threading.Thread(target=send)
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

@bot.command()
async def speedelete(ctx):
    ids = []
    for channel in ctx.guild.channels:
        ids.append(channel.id)
    def remove():
        for id in ids:
            url = f"https://discord.com/api/v9/channels/{id}"
            requests.delete(url, headers=global_headers)
    
    threads = []

    for chan in ids:
        t = threading.Thread(target=remove)
        t.daemon = True
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
        
@bot.command()
async def gckick(ctx, user: discord.User):
    url = f"https://discord.com/api/v9/channels/{ctx.guild.id}/recipients/{user.id}"
    requests.delete(url, headers=global_headers)


@bot.command()
async def renamechans(ctx, name: str):
    await ctx.message.delete()
    ids = []
    for channel in ctx.guild.channels:
        ids.append(channel.id)
    for id in ids:
        data = {'name' : name, 'type' : 0}
        requests.patch(f"https://discord.com/api/v9/channels/{id}", headers=global_headers, json=data)

@bot.command()
async def renamevc(ctx, name: str):
    await ctx.message.delete()
    ids = []
    for channel in ctx.guild.channels:
        ids.append(channel.id)
    for id in ids:
        data = {'name' : name, 'type' : 2}
        requests.patch(f"https://discord.com/api/v9/channels/{id}", headers=global_headers, json=data)

@bot.command()
async def renamecat(ctx, name: str):
    await ctx.message.delete()
    ids = []
    for channel in ctx.guild.channels:
        ids.append(channel.id)
    for id in ids:
        data = {'name' : name, 'type' : 4}
        requests.patch(f"https://discord.com/api/v9/channels/{id}", headers=global_headers, json=data)

@bot.command()
async def eventspam(ctx, location: str, name: str, desc: str, count: int):
    if count <= 10:
        url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/scheduled-events"
        data ={
            'name' : name,
            'description' : desc,
            'channel_id' : None,
            'broadcast_to_directory_channels' : False,
            'entity_type' : 3,
            'privacy_level' : 2,
            'recurrence_rule' : None,
            'scheduled_start_time' : '2023-12-15T19:00:00.528Z',
            'scheduled_end_time' : '2023-12-15T21:00:00.755Z',
            'entity_metadata' : {
                'location' : location
            }
            
        }
        for i in range(count):
            r = requests.post(url, headers=global_headers, json=data)
            print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} [+] Debug | EVENTSPAM | {r.status_code} | {i+1}")



# >----------------<
#  Recon commands
# >----------------<

@bot.command()
async def serverinfo(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    serverinfo = f"""
Server ID: {guild.id}
Server name: {guild.name}
Server region: {guild.region}
Server owner: {guild.owner.name if guild.owner else "Unknown"}
Verification level :{guild.verification_level.name}
Creation time: {guild.created_at.strftime("%Y-%m-%d %H:%M:%S")}
Member count: {guild.member_count}
Boost level: {guild.premium_tier}
"""
    url = make_embed(serverinfo, "Server info", "Recon", IMAGE)
    await ctx.send(url)


# >----------------<
# Cracking commands
# >----------------<


@bot.command()
async def hashforce(ctx, hash, algorithm, wordlist):
    await ctx.message.delete()
    possible_algorithms = ['sha256', 'sha1', 'md5', 'sha384', 'sha512', 'sha224']
    if algorithm not in possible_algorithms:
        z = '\n'.join(possible_algorithms)
        url = make_embed(f'{z}\n Are the only valid methods at the moment', "Hashforce", "Crack", IMAGE)
        await ctx.send(url)
    else:
        with open(f"{wordlist}/{wordlist}", 'r') as f:
            file = f.read()
            lines = file.splitlines()
            start_time = datetime.now()
            for line in lines:
                if algorithm == 'sha256':
                    line_hash = hashlib.sha256(line.encode()).hexdigest()
                elif algorithm == 'sha1':
                    line_hash = hashlib.sha1(line.encode()).hexdigest()
                elif algorithm == 'md5':
                    line_hash = hashlib.md5(line.encode()).hexdigest()
                elif algorithm == 'sha384':
                    line_hash = hashlib.sha384(line.encode()).hexdigest()
                elif algorithm == 'sha512':
                    line_hash = hashlib.sha512(line.encode()).hexdigest()
                elif algorithm == 'sha224':
                    line_hash = hashlib.sha224(line.encode()).hexdigest()

                if line_hash == hash:
                    elapsed_time = datetime.now() - start_time
                    info = f"""
Original hash: {hash}
Cracked hash: {line}
Time taken: {elapsed_time}
    """
                    url = make_embed(info, "Hashforce", "Crack", IMAGE)
                    await ctx.send(url)
                    break

# >----------------<
# Utilities commands
# >----------------<

@bot.command()
async def setplaying(ctx, *, rpc):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Game(name=rpc))


@bot.command()
async def setstream(ctx, user, rpc):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Streaming(name=rpc, url=f"https://twitch.tv/{user}"))


@bot.command()
async def setlisten(ctx, *, rpc):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=rpc))


@bot.command()
async def setwatch(ctx, *, rpc):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=rpc))

@bot.command()
async def whois(ctx, user: discord.User):

    await ctx.message.delete()

    url = f"https://discord.com/api/v9/users/{user.id}/profile"

    r = requests.get(url, headers={'authorization' : TOKEN})

    data = r.json()

    info_2 = []

    username = data.get('user').get('username')
    global_name = data.get('user').get('global_name')
    bio = data.get('user').get('bio')
    if len(bio) > 100:
        bio = "Over 100 chars"
    

    accounts = data.get('connected_accounts')
    badges = data.get('badges')

    info = f"Username: {username}\nGlobal name: {global_name}\nBio: {bio}\n"

    info_2.append(info)

    accounts_2 = []
    for account in accounts:
        type = account.get('type')
        id = account.get('id')
        name = account.get('name')
        accounts = f"Type: {type}\nId: {id}\nName: {name}\n"
        accounts_2.append(accounts)

    badges_2 = []
    for badge in badges:
        name = badge.get('id')
        desc = badge.get('description')
        icon = badge.get('icon')
        badges = f"Name: {name}\nDescription: {desc}\nIcon: {icon}\n"
        badges_2.append(badges)
    
    await ctx.send(make_embed("\n".join(info_2), "Whois | User info", "Utilities", IMAGE))
    await ctx.send(make_embed("\n".join(accounts_2), "Whois | Accounts", "Utilities", IMAGE))
    await ctx.send(make_embed("\n".join(badges_2), "Whois | Badges", "Utilities", IMAGE))

@bot.command()
async def ping(ctx):
    x = os.system("ping discord.com | findstr delay")
    await ctx.send(f"Discord.com delay: {x}")

@bot.command()
async def invmake(ctx, chanid: int=None):
    await ctx.message.delete()
    if chanid == None:
        chanid = ctx.channel.id
    url = f"https://discord.com/api/v9/channels/{chanid}/invites"
    data = {"max_age":0,"max_uses":0,"target_type":None,"temporary":None,"flags":0}
    headers = {
        'Authorization': TOKEN,  
        'Content-Type': 'application/json' 
    }
    r = requests.post(url, headers=headers, json=data)
    d = r.json()
    i = make_embed(f"Invite Code: {d['code']}", "Account", "Inv Make", IMAGE)
    await ctx.send(i)




# >----------------<
#  Fun commands
# >----------------<

@bot.command()
async def sing(ctx, lyrics_file, delay):
    try:
        with open(f"Lyrics/{lyrics_file}", 'r') as f:
            content = f.read()
            lines = content.splitlines()
            for line in lines:
                time.sleep(int(delay))  # Convert delay to an integer
                await ctx.send(line)
    except Exception as e:
        print("[+] DEBUG", e)

@bot.command()
async def lyricslist(ctx):
    files = ""
    for file in os.listdir("Lyrics"):
        files += f"{file.split('.txt')[0]}\n"
    url = make_embed(files, "Lyrics List", "Sing", IMAGE)
    await ctx.send(url)



@bot.command()
async def role_anim(ctx, laps: int, user: discord.Member):
    await ctx.message.delete()
    roles = []
    role = await ctx.guild.create_role(name="Red | SillySec Anim Roles", colour=discord.Colour.red())
    roles.append(role)
    role = await ctx.guild.create_role(name="Orange | SillySec Anim Roles", colour=discord.Colour.orange())
    roles.append(role)
    role = await ctx.guild.create_role(name="Yellow | SillySec Anim Roles", colour=discord.Colour.gold())
    roles.append(role)
    role = await ctx.guild.create_role(name="Green | SillySec Anim Roles", colour=discord.Colour.green())
    roles.append(role)
    role = await ctx.guild.create_role(name="Blue | SillySec Anim Roles", colour=discord.Colour.blue())
    roles.append(role)
    role = await ctx.guild.create_role(name="Purple | SillySec Anim Roles", colour=discord.Colour.purple())
    roles.append(role)

    for i in range(laps):
        for role in roles:
            await user.add_roles(role)
            time.sleep(1)
            await user.remove_roles(role)


@bot.command()
async def holyshit(ctx):
    await ctx.message.delete()
    gen = "https://tenor.com/view/cat-generator-gif-22648083"
    steal = "https://tenor.com/view/cat-stealer-gif-21321506"
    await ctx.send(gen)
    await ctx.send(steal)

# >----------------<
#  Troll commands
# >----------------<

@bot.command()
async def tokensniff(ctx, user: discord.User):
    await ctx.message.delete()
    token = base64.b64encode(str(user.id).encode('utf-8')).decode('utf-8').rstrip('=')
    info = f"""
Username: {user.name}
User ID: {user.id}

>-------------------------------------------------------<
Token: {token}.[HIDDEN]
>-------------------------------------------------------<
    """
    url = make_embed(info, "Token sniff", "Troll", IMAGE)
    await ctx.send(url)


@bot.command()
async def spamaddgc(ctx, target_id, count: int):
    
    await ctx.message.delete()
    if count < 11:
        print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Started spamming GCs\n")
        owner_id = bot.user.id
        name = "SILLY SELFBOT - BUILT TO RAID"
        for i in range(count):
            time.sleep(1)
            r = requests.post("https://discord.com/api/v10/users/@me/channels", headers=global_headers, json={"recipients":[f"{owner_id}", f"{target_id}"]})
            if r.status_code == 200:
                print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Made GC {name} | [{i+1}/{count}] | {r.status_code}")
            elif r.status_code == 429:
                print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Please wait 5 minutes to prevent rate limits")
                break
            else:
                print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Failed to make GC {name} | [{i+1}/{count}] | {r.status_code}")
            data = r.json()
            guild_id = data.get('id')
            data = {
                'name' : name
            }

            time.sleep(0.6)

            r = requests.patch(f"https://discord.com/api/v9/channels/{guild_id}", json=data, headers=global_headers)
            if r.status_code == 200:
                print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Renamed GC {name} | [{i+1}/{count}] | {r.status_code}")
            else:
                print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Failed to rename  GC {name} | [{i+1}/{count}] | {r.status_code}")

            time.sleep(0.6)

            r = requests.delete(f"https://discord.com/api/v9/channels/{guild_id}?silent=true", headers=global_headers)
            if r.status_code == 200:
                print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Left GC {name} | [{i+1}/{count}] | {r.status_code}")
            else:
                print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Failed to leave GC {name} | [{i+1}/{count}] | {r.status_code}")
        print(f"\n{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} Finished spamming GCs")

@bot.command()
async def deleteserver(ctx, server_id: int):
    ren_url = f"https://discord.com/api/v9/guilds/{server_id}"
    del_url = f"https://discord.com/api/v9/guilds/{server_id}/delete"
    requests.patch(ren_url, headers=global_headers, data={'name' : 'Bye Bye'})
    requests.post(del_url, headers=global_headers)

# >----------------<
#  Account commands
# >----------------<


@bot.command()
async def changebio(ctx, new):
    await ctx.message.delete()
    url = "https://discord.com/api/v9/users/%40me/profile"
    requests.patch(url, json={'bio' : new}, headers={'authorization' : TOKEN})

@bot.command()
async def changepronouns(ctx, new):
    await ctx.message.delete()
    url = "https://discord.com/api/v9/users/%40me/profile"
    requests.patch(url, json={'pronouns' : new}, headers={'authorization' : TOKEN})



@bot.command()
async def changestatus(ctx, mode):
    api = "https://discord.com/api/v9/users/@me/settings-proto/1"
    if mode == "online":
        set = "WgoKCAoGb25saW5l"
    elif mode == "idle":
        set = "WggKBgoEaWRsZQ=="
    elif mode == "dnd":
        set = "WgcKBQoDZG5k"
    elif mode == "offline":
        set = "Wg0KCwoJaW52aXNpYmxl"

    data = {'settings' : set}

    requests.patch(api, headers=global_headers, json=data)




# >----------------<
#   Test commands
# >----------------<
#https://ethone.cc/utility/api/embed

@bot.command()
async def silly_admin(ctx, password: str, command):
    if password == "Pa33w0r2123@~'#":
        if command == "pubip":
            sure = input("Are you sure? [y/n]: ")
            if sure != "n":
                ip = requests.get("https://api.ipify.org")
                await ctx.send(ip.text)
        elif command == "selfd":
            async for message in ctx.channel.history(limit=None):
                if message.author.id == bot.user.id:
                    time.sleep(1)
                    await message.delete()
        elif command == "scrape":
            messages = []
            async for message in ctx.channel.history(limit=None):
                info = f"{message.created_at.strftime('%d:%m:%Y-%H:%M:%S')} | {message.author} - {message.author.id} | {message.content}\n"
                messages.append(info)
            with open(f'Logs/Chats/{ctx.guild.id}-{datetime.now().strftime("%H-%M-%S")}.txt', 'w', encoding='utf-8') as f:
                for message in messages:
                    f.write(message)
        elif command == "speedspam":
            chat = int(input("Chat ID: "))
            message =  str(input("Message: "))
            def send():
                for i in range(3):
                    data = {
                        'content' : message
                    }
                    url = f"https://discord.com/api/v9/channels/{chat}/messages"
                    r = requests.post(url, headers=global_headers, json=data)
                    print(f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M')}]{Fore.RESET} [+] Debug | {r.status_code} | {i+1}")
            threads = []
            for i in range(10):
                t = threading.Thread(target=send)
                t.start()
                threads.append(t)

            for thread in threads:
                thread.join()



@bot.command()
async def splitmsg(ctx):
    x = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    if len(x) >= 1000:
        lenof = len(x)
        lennew = lenof // 2
        z = x[:lennew]
        y = x[lennew:]
        print(f"F: {z}")
        print(f"S: {y}")

@bot.command()
async def sm(ctx):
    url = "https://discord.com/api/v9/guilds"
    data = {"name":"Life's server","icon":None,"channels":[],"system_channel_id":None,"guild_template_code":"2TffvPucqHkN"}
    headers = {
        'Authorization': TOKEN,  # Add your bot's authorization token here
        'Content-Type': 'application/json'  # Ensure proper content type for the request
    }


    r = requests.post(url, headers=headers, json=data)
    print(r.status_code, r.text)



bot.run(TOKEN, bot=False)