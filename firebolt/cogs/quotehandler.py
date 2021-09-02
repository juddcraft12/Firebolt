import json
import random
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import discord
import firebolt.tools.embed as dmbd
import os
import fortune
import re
class quotehandler(commands.Cog):
    """Quote commands"""

    def __init__(self, bot):
        """ Initialize Quote Commands"""

        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message):
      if message.channel.id == 864343350916546560:
         lines=open('quotes.txt',"a")
         mess=str(message.content)
         attachment=0
         if message.attachments:
          attachment=message.attachments[0].url
         else:
          if len(str(attachment))>1:
            mess=attachment
            lines.write(str(mess)+"\n")
          else:
           mess=mess.replace('!','')
           ping=re.split("\<\@(.+?)\>",str(mess))
           print(ping)
           for i in ping:
              def containsNumber(value):
               for character in i:
                if character.isdigit():
                 return True
                else:
                 return False
                 break
              if containsNumber(i) and len(i)==18:
                user = await self.bot.fetch_user(i)
                split_string = str(user).split("#", 1)
                user = split_string[0]
                index = ping.index(str(i))
                ping[index]="@"+str(user)
                print(ping)
              else:
                print("No") 
           save=''.join(ping)
           lines.write(str(save)+"\n")
def setup(bot):
    """ Setup Quotes Module"""
    bot.add_cog(quotehandler(bot))
