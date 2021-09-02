import json
import random
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import discord
import firebolt.tools.embed as dmbd
import os
import fortune
import discord.utils
import re
class Quotes(commands.Cog):
    """Quote commands"""

    def __init__(self, bot):
        """ Initialize Quote Commands"""

        self.bot = bot

    @commands.command(aliases=['uncanny_quotes','quotes'])
    async def quote(self,ctx):
      """ Quotes from the Exemplify SMP"""
      lines = open('quotes.txt').read().splitlines()
      myline =random.choice(lines)
      imgurl="https://cdn.discordapp.com/"
      if imgurl in myline:
       em = dmbd.newembed()
       em.set_image(url=myline)
       await ctx.send(embed=em)       
      else:
       await ctx.send(myline)

#    @commands.command()
#    async def keyword(self,ctx):
#      lines=open('quotes.txt',"a")
#      channel = discord.utils.get(ctx.guild.channels, id=864343350916546560) 
#      messages = await channel.history(limit=100000000000000).flatten()
#      for msg in messages:
#        mess=str(msg.content)
#        attachment=0
#        if msg.attachments:
#        attachment=msg.attachments[0].url
#        else:
#         if len(str(attachment))>1:
#           mess=attachment
#           lines.write(str(mess)+"\n")
#         else:
#          mess=mess.replace('!','')
#          ping=re.split("\<\@(.+?)\>",str(mess))
#          print(ping)
#          for i in ping:
#             def containsNumber(value):
#              for character in i:
#               if character.isdigit():
#                return True
#               else:
#                return False
#                break
#             if containsNumber(i) and len(i)==18:
#               user = await self.bot.fetch_user(i)
#               split_string = str(user).split("#", 1)
#               user = split_string[0]
#               index = ping.index(str(i))
#               ping[index]="@"+str(user)
#               print(ping)
#             else:
#               print("No") 
#          save=''.join(ping)
#          lines.write(str(save)+"\n")

def setup(bot):
    """ Setup Quotes Module"""
    bot.add_cog(Quotes(bot))
