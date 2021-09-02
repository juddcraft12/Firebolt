import discord

import firebolt


def newembed(c=0xEEB551):
    em = discord.Embed(colour=c)
    em.set_footer(text="Made by Antimatter",
                  icon_url="https://cdn.discordapp.com/embed/avatars/2.png")

    return em
