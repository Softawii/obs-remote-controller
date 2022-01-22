import discord


def equals(l1, l2):    
    result = all(map(lambda x, y: x == y, l1, l2))
    return result and len(l1) == len(l2)


def createEmbed(title="", description="", color=0x00ff00, fields=[], img=""):
    embed = discord.Embed(title=title, description=description, color=color)
    
    if img != "":
        embed.set_image(url=img)

    for field in fields:
        embed.add_field(name=field[0], value=field[1], inline=field[2])

    return embed
