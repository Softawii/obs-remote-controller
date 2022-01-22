# Discord
import discord
from discord.ext import commands, tasks
import json
import logging
import sys

# My content
import core.core as core
import utils.utils as utils
from utils.pages import PageSystem

config = json.load(open('credentials.json'))
logging.getLogger("discord").setLevel(logging.WARNING)
logging.debug("Removed Discord.py logs")

bot = commands.Bot(command_prefix='$', description='A bot to control the OBS Studio')
scenes = (False, [])
current_page = []
last_page_size = 0

page_system = PageSystem(['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣'], '◀️','▶️')
PAGE_CONTAINS_EMOJI = lambda x, reactions: len(list(filter(lambda y: x == y.emoji, reactions)))


@tasks.loop(seconds = config['update_time'])
async def update_scene_list():
    global scenes, current_page, last_page_size
    
    _scenes = await core.scene_list()
    
    if not utils.equals(_scenes[1], scenes[1]):
        print('update_scene_list: updated list = ' + str(_scenes[0]) + ' ' + str(_scenes[1]))
    
    scenes = (_scenes[0], _scenes[1])
    if scenes[0]:
        current_page = page_system.get_current_page_items(scenes[1])
    else:
        current_page = []
    
    channel = get_channel()
    if channel != False:
        
        # Update in the message
        try: 
            message = await channel.fetch_message(config["msg-id"])
            if scenes[0]:
                await message.edit(content="", embed=scene_list_embed(current_page))
            else:
                await message.edit(content="O programa está indisponível, tente novamente mais tarde!", embed=None)
        except discord.NotFound: 
            # TODO: Creating another one
            return
        
        # Adding reactions 
        current_page_items = len(current_page)
        
        if current_page_items == last_page_size:
            return
        
        last_page_size = current_page_items
        
        await message.clear_reaction(page_system.next_emoji)
        await message.add_reaction(page_system.back_emoji)
        for i in range(len(page_system.emoji_list)):
            if i >= current_page_items and PAGE_CONTAINS_EMOJI(page_system.emoji_list[i], message.reactions):
                await message.clear_reaction(page_system.emoji_list[i])
            elif i < current_page_items and not PAGE_CONTAINS_EMOJI(page_system.emoji_list[i], message.reactions):
                await message.add_reaction(page_system.emoji_list[i])    
        await message.add_reaction(page_system.next_emoji)

def get_channel():
    guild = list(filter(lambda x: x.id == config['guild-id'], bot.guilds))
    
    if len(guild) >= 1:
        guild = guild[0]
    else:
        return False

    channel = list(filter(lambda x: x.id == config['channel-id'], guild.text_channels))
    
    if len(channel) >= 1:
        channel = channel[0]
    else:
        return False

    return channel


@bot.event
async def on_ready():
    """
        Initializing core configuration (socket connection) and loops
    """
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    
    try:
        await core.setup()
    except:
        print("Runtime Error: Maybe the OBS is off or the credentials are wrong")
        sys.exit(1)
    
    print("Getting current scene")
    ok, current = await core.get_current_scene()
    
    if ok:
        print("Presence Update: " + current)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=current))
    
    # Loop to update the scene list, every 'update_time' seconds
    update_scene_list.start()
    print("Loop Started")
    
    
@bot.event
async def on_raw_reaction_add(payload):
    global scenes, current_page, current_page_items, PAGE_SETTINGS
    
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji="📩")
    user = payload.member
    
    emoji = payload.emoji
    
    if payload.guild_id == config["guild-id"] and payload.channel_id == config["channel-id"] and message.id == config["msg-id"]:
        
        if bot.user.id != user.id:
            await message.remove_reaction(emoji, user)

            if emoji.name in page_system.emoji_list[:page_system.get_current_page_items_number()]:
                index = page_system.emoji_list.index(emoji.name)
                await cam(bot.get_channel(payload.channel_id), current_page[index])
            
            if emoji.name == page_system.next_emoji:
                page_system.increase_page()
                current_page = page_system.get_current_page_items(scenes[1])
                await update_scene_list()
            elif emoji.name == page_system.back_emoji:
                page_system.decrease_page()
                current_page = page_system.get_current_page_items(scenes[1])
                await update_scene_list()
            
                      
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
       
@bot.command()
async def setup(ctx):
    guild = ctx.message.guild
    channel = await guild.create_text_channel(config["channel-name"])
          
    global scenes, current_page
    
    ok = scenes[0]
    lst = scenes[1]
    
    if not ok:
        msg = await channel.send('Ocorreu um erro ao obter a lista de cenas, talvez o obs esteja desconectado ou não está configurado corretamente')
    else:
        msg = await channel.send(embed=scene_list_embed(current_page))

    config["guild-id"]   = guild.id
    config["channel-id"] = channel.id
    config["msg-id"]     = msg.id
    
    with open('credentials.json', 'w') as outfile:
        json.dump(config, outfile, indent=4)


async def cam(channel, cam_name: str):

    ok = await core.set_scene(cam_name)

    if not ok:
        await channel.send('Falha ao mudar de camera, talvez o obs esteja desconectado ou não está configurado corretamente', delete_after=10)

    if ok:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=cam_name))


def scene_list_embed(lst):
    strLst = ""
    for i in range(len(lst)):
        strLst += f"**{i + 1}**. {lst[i]}\n"
        
    embedmsg = utils.createEmbed(title="Lista de Cenas", description=strLst, color=0x00ff00, fields=[], img="")
    
    return embedmsg

bot.run(config['discord_token'])