import discord
from discord.ext import commands
from time import sleep 
from datetime import datetime
from configtemplate import DEVELOPER_NAME, PYTHON_VERSION, DISCORD_VERSION, BOT_VERSION

class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Suggest your command.", aliases=['suggestion'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def suggest(self, ctx, suggestion=str):
      embed = discord.Embed(title=f"Suggestion by {ctx.author}", description=suggestion, colour=discord.Colour.blue())
      dt = datetime.now()
      dt2 = dt.strftime('%H:%M.%S %p')
      embed.set_footer(text=f'{dt2} | {ctx.author}')
      await ctx.message.delete()
      await self.bot.get_user(764848425253994516).send(embed=embed)
      await ctx.author.send(f"Your suggestion has been sent to the developers.")

    @commands.command(description="Post reports to the devs.", aliases=['reports'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def report(self, ctx, report):
      embed = discord.Embed(title=f"Report by {ctx.author}", description=report, colour=discord.Colour.blue())
      dt = datetime.now()
      dt2 = dt.strftime('%H:%M.%S %p')
      embed.set_footer(text=f'{dt2} | {ctx.author}')
      await ctx.message.delete()
      await self.bot.get_user(764848425253994516).send(embed=embed)
      await ctx.author.send(f"Your report has been sent to the developers.")

    @commands.command(description="Gives the link to bot's support server.", aliases=['support', 'ss', 'sserver', 'supports'])
    async def supportserver(self, ctx):
      embed=discord.Embed(
        title='Here is the link for my support server!',
        description="[Support Server](<https://discord.gg/JBS3s4n>)",
        colour=discord.Colour.blue()
      )
      await ctx.send(embed=embed)

    @commands.command(description='Gets the bots credits.', aliases=['crd', 'credit'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def credits(self, ctx):
      embed = discord.Embed(title='Credits', colour=discord.Colour.blue())
      embed.add_field(name='Developer', value='That GenZ Gamer#7595')
      embed.add_field(name='Co-Developer', value='f4477#1560')
      embed.set_footer(text='And all my IRL and Online friends for supporting me!')
      await ctx.send(embed=embed)

    @commands.command(description="Invites the bot to your server.", aliases=['inv', 'i'])
    async def invite(self, ctx):
        embed = discord.Embed(
          title="Invite my bot using this link!", 
          description="[Invite Bot Link](<https://discord.com/api/oauth2/authorize?client_id=799247206829654036&permissions=8&scope=bot>)", 
          colour=discord.Colour.blue())
        await ctx.message.delete()
        await ctx.send(embed=embed)
      
    @commands.command(description="Pings the user 5 times", aliases=['raidme', 'rme', 'pme'])
    async def raid(self, ctx, member: discord.Member = None):
      if member == None:
        member = ctx.author
      await ctx.message.delete()
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)
      await ctx.send(f"{member.mention}") ; sleep(0.5)

    @commands.command(description="Shows the bot's stats", aliases=['info', 'botinfo'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stats(self, ctx):
      guilds = len(self.bot.guilds)
      cmds = len(self.bot.commands)
      ping = f"{round(self.bot.latency * 1000)}ms"
      embed = discord.Embed(title="Bot Stats")
      embed.add_field(name="BOT", value=self.bot.user, inline=False)
      embed.add_field(name="PYTHON", value=PYTHON_VERSION, inline=False)
      embed.add_field(name="DISCORD.PY", value=DISCORD_VERSION, inline=False)
      embed.add_field(name="BOT", value=BOT_VERSION, inline=False)
      embed.add_field(name="GUILDS", value=guilds, inline=False)
      embed.add_field(name="DEVELOPER", value=DEVELOPER_NAME, inline=False)
      embed.add_field(name="COMMANDS", value=cmds, inline=False)
      embed.add_field(name="CURRENT PING", value=ping, inline=False)
      await ctx.send(embed=embed)

    @commands.command(description="Shows how many servers, the bot is in.", aliases=['servercount'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def guilds(self, ctx):
      guilds_to_go = 100 - len(self.bot.guilds)
      guilds_now = len(self.bot.guilds)
      await ctx.send(f"The bot is currently in {guilds_now} guilds and the bot has {guilds_to_go} guilds to go.")

def setup(bot):
    bot.add_cog(Bot(bot))
