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
import core


config = json.load(open('credentials.json'))
logging.getLogger("discord").setLevel(logging.WARNING)
logging.debug("Removed Discord.py logs")

bot = commands.Bot(command_prefix='$', description='A bot to control the OBS Studio')

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await core.setup()
    
                        
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
    
@bot.command()
async def list(ctx):
    ok, scenes = await core.scene_list()
    
    if not ok:
        ctx.send('Ocorreu um erro ao obter a lista de cenas, talvez o obs esteja desconectado ou não está configurado corretamente')
        return
    
    for scene in scenes:
        await ctx.send(scene)
    

@bot.command()
async def cam(ctx, *, cam_name: str):
    
    ok = await core.set_scene(cam_name)

    if not ok:
        await ctx.send('Falha ao mudar de camera, talvez o obs esteja desconectado ou não está configurado corretamente')

    if ok:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=cam_name))


bot.run(config['discord_token'])