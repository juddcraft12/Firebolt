import discord
import psutil
import time
import typing


import firebolt


class Moderation(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.command(aliases=['?'])
    async def help(self, ctx, *cog):
        if not cog:
            embed = discord.Embed(description="📖 Help", color=0xEEB551,
                                  icon_url="https://cdn.discordapp.com/avatars/612634758744113182"
                                           "/7fe078b5ea6b43000dfb7964e3e4d21d.png?size=512")
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/840230433178124299/abb04ca910c2c38ea44c7381ce1e3df6.png?size=1024")
            cogs_desc = ""
            for x in self.bot.cogs:
              
                cogs_desc += f'**{x}** - {self.bot.cogs[x].__doc__}\n'
            embed.add_field(name='Modules', value=cogs_desc[0:len(cogs_desc) - 1])
            embed.set_footer(text=f"Antimatter made this with zero sleep and zero will to live | Code licensed under the MIT License")
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(emoji='✅')
        else:
            if len(cog) > 1:
                await ctx.send(embed=firebolt.messages.toomanyarguments())
                await ctx.message.add_reaction(emoji='🛑')
            else:
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            embed = discord.Embed(color=0xEEB551)
                            cog_info = ''
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    cog_info += f"**{c.name}** - {c.help}\n"
                            embed.add_field(name=f"{cog[0]} Module", value=cog_info)
                            await ctx.send(embed=embed)
                            await ctx.message.add_reaction(emoji='✅')
                            found = True
                if not found:
                    for x in self.bot.cogs:
                        for c in self.bot.get_cog(x).get_commands():
                            if c.name.lower() == cog[0].lower():
                                embed = discord.Embed(title=f"Command: {c.name.lower().capitalize()}",
                                                      description=f"**Description:** {c.help}\n**Syntax:** {c.qualified_name} {c.signature}",
                                                      color=0xEEB551)
                                embed.set_author(name=f"Firebolt.py {firebolt.version()}",
                                                 icon_url="https://cdn.discordapp.com/embed/avatars/2.png")
                                await ctx.message.add_reaction(emoji='✅')
                                found = True
                    if not found:
                        embed = firebolt.messages.notfound("Module")
                        await ctx.message.add_reaction(emoji='🛑')
                    await ctx.send(embed=embed)
                else:
                    await ctx.message.add_reaction(emoji='✅')


    @discord.ext.commands.command(aliases=['about'])
    async def info(self, ctx):
        embed = discord.Embed(title="Developers: Me, Myself, I, Antimatter", description="Multi-purpose Discord Bot",
                              color=0xEEB551)
        embed.set_author(name=f"Firebolt.py {firebolt.version()}",
                         icon_url="https://cdn.discordapp.com/embed/avatars/2.png")
        embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/2.png")
        embed.add_field(name="Bot User:", value=self.bot.user)
        embed.add_field(name="Guilds:", value=len(self.bot.guilds))
        embed.add_field(name="Members:", value=len(set(self.bot.get_all_members())))
        embed.add_field(name="O.S.:", value=str(firebolt.platform()))
        embed.add_field(name="Storage Type:", value=firebolt.config.storage_type())
        embed.add_field(name="Prefix:", value="b.")
        embed.add_field(name="Links",
                        value="[Support Discord](https://discord.gg/QmRFNwp8)",
                        inline=False)
        embed.set_footer(text=f"{firebolt.copyright()} | Code licensed under MIT License")
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(emoji='✅')


    @discord.ext.commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)} ms')
        await ctx.message.add_reaction(emoji='✅')


    @discord.ext.commands.command(aliases=['purge', 'clear', 'cls'])
    @discord.ext.commands.has_permissions(manage_messages=True)
    async def prune(self, ctx, amount=0):
        if amount == 0:
            await ctx.send("Please specify the number of messages you want to delete!")
            await ctx.message.add_reaction(emoji='❌')
        elif amount <= 0:  # lower then 0
            await ctx.send("The number must be bigger than 0!")
            await ctx.message.add_reaction(emoji='❌')
        else:
            await ctx.message.add_reaction(emoji='✅')
            await ctx.channel.purge(limit=amount + 1)


    @discord.ext.commands.command()
    @discord.ext.commands.has_permissions(kick_members=True)  # check user permission
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'{member} has been kicked!')
            await ctx.message.add_reaction(emoji='✅')
        except Exception as failkick:
            await ctx.send("Failed to kick: " + str(failkick))
            await ctx.message.add_reaction(emoji='❌')


    @discord.ext.commands.command()
    @discord.ext.commands.has_permissions(ban_members=True)  # check user permission
    async def ban(self, ctx, member: discord.User, *, reason=None):  # Banning a member who is not in the server is also possible
        try:
            if isinstance(member, discord.Member):
                await member.ban(reason=reason)
            else:
                await ctx.guild.ban(member, reason=reason)
                
            await ctx.send(f'{member.name} has been banned!')
            await ctx.message.add_reaction(emoji='✅')
        except Exception as e:
            await ctx.send("Failed to ban: " + str(e))
            await ctx.message.add_reaction(emoji='❌')
    
    @discord.ext.commands.command()
    @discord.ext.commands.has_permissions(ban_members=True)  # check user permission
    async def unban(self, ctx, member: discord.User, *, reason=None):
        try:
            await ctx.guild.unban(member, reason=reason)                
            await ctx.send(f'{member.name} has been unbanned!')
            await ctx.message.add_reaction(emoji='✅')
        except Exception as e:
            await ctx.send("Failed to unban: " + str(e))
            await ctx.message.add_reaction(emoji='❌')

    @discord.ext.commands.command() # Work In Progress
    async def admin(self, ctx):
        await ctx.send(embed=firebolt.messages.WIP())


    @discord.ext.commands.command()
    @discord.ext.commands.has_permissions(administrator=True)
    async def debug(self, ctx):
        embed = discord.Embed(title="Developers: Me, Myself, I, Antimatter", description="Debug info:",
                              color=0xEEB551)
        embed.set_author(name=f"Firebolt.py {firebolt.version()}",
                         icon_url="https://cdn.discordapp.com/embed/avatars/2.png")
        embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/2.png")
        embed.add_field(name="Bot User:", value=self.bot.user, inline=True)
        embed.add_field(name="Memory",
                        value=str(round(psutil.virtual_memory()[1] / 1024 / 1024 / 1024)) + "GB / " + str(round(
                            psutil.virtual_memory()[0] / 1024 / 1024 / 1024)) + "GB", inline=True)
        embed.add_field(name="O.S.:", value=str(firebolt.platform()), inline=True)
        embed.add_field(name="Storage Type:", value=firebolt.config.storage_type(), inline=True)
        embed.add_field(name="Prefix:", value=", ".join(firebolt.config.bot_prefix()), inline=True)
        embed.add_field(name="Links",
                        value="[Support Discord](https://discord.gg/QmRFNwp8)",
                        inline=False)
        embed.set_footer(text=f"{firebolt.copyright()} | Code licensed under the MIT License")
        # embed.set_image(url="https://user-images.githubusercontent.com/43201383/72987537-89830a80-3e25-11ea-95ef-ecfa0afcff7e.png")
        await ctx.message.author.send(embed=embed)
        await ctx.message.add_reaction(emoji='✅')
 

def setup(bot):
    bot.add_cog(Moderation(bot))
