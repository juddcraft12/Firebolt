import discord

import teapot


def newembed(c=0x428DFF):
    em = discord.Embed(colour=c)
    em.set_footer(text=teapot.copyright(),
                  icon_url="https://cdn.discordapp.com/embed/avatars/2.png")

    return em
