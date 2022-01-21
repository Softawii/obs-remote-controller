# Discord
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
import random
import copy
from typing import Union
import json
import os
import logging
import sys

# My content
import core.core as core
import utils

config = json.load(open('credentials.json'))
logging.getLogger("discord").setLevel(logging.WARNING)
logging.debug("Removed Discord.py logs")

bot = commands.Bot(command_prefix='$', description='A bot to control the OBS Studio')
scenes = (False, [])


@tasks.loop(seconds = config['update_time'])
async def update_scene_list():
    global scenes
    
    _scenes = await core.scene_list()
    
    if not utils.equals(_scenes[1], scenes[1]):
        print('update_scene_list: updated list = ' + str(_scenes[0]) + ' ' + str(_scenes[1]))
    
    scenes = (_scenes[0], _scenes[1])


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
    
                          
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
    
@bot.command()
async def list(ctx):
    
    global scenes
    
    ok = scenes[0]
    lst = scenes[1]
    
    if not ok:
        ctx.send('Ocorreu um erro ao obter a lista de cenas, talvez o obs esteja desconectado ou não está configurado corretamente')
        return
    
    strLst = ""
    for i in range(len(lst)):
        strLst += f"**{i + 1}**. {lst[i]}\n"
        
    embedmsg = utils.createEmbed(title="Lista de Cenas", description=strLst, color=0x00ff00, fields=[], img="")
    callback = await ctx.send(embed=embedmsg)
    
    print("Callback ID: " + str(callback.id))
     
        
@bot.command()
async def cam(ctx, *, cam_name: str):
    
    ok = await core.set_scene(cam_name)

    if not ok:
        await ctx.send('Falha ao mudar de camera, talvez o obs esteja desconectado ou não está configurado corretamente')

    if ok:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=cam_name))


bot.run(config['discord_token'])