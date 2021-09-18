import discord
from discord.ext import commands
import json
import random 
import requests



class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", description="Gets the bot's latency")
    async def ping(self, ctx):
      latency = round(self.bot.latency * 1000)
      await ctx.send(f"Pong! `{latency}ms`") 
    
    @commands.command(name="pfp", aliases=["avatar", "av"])
    async def pfp(self, ctx, member: discord.Member = None):
      if member == None:
        member=ctx.author
        em=discord.Embed(
          title=f"{member.name}'s Avatar",
          color=discord.Color.blue()
        )
        em.set_image(url=member.avatar_url)
        await ctx.send(embed=em)
      else:
        em=discord.Embed(
          title=f"{member.name}'s Avatar",
          color=discord.Color.blue()
        )
        em.set_image(url=member.avatar_url)
        await ctx.send(embed=em)

    @commands.command(aliases=['si'], description="Gives the server's info")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=str(ctx.guild.name) + "'s Server Information",
                              description=str(ctx.guild.description), colour=discord.Color.blue())

        embed.set_thumbnail(url=str(ctx.guild.icon_url))
        embed.add_field(name="OWNER", value=str(ctx.guild.owner), inline=False)
        embed.add_field(name="SERVER ID", value=str(ctx.guild.id), inline=False)
        embed.add_field(name="REGION", value=str(ctx.guild.region), inline=False)
        embed.add_field(name="MEMBER COUNT", value=str(ctx.guild.member_count), inline=True)
        await ctx.send(embed=embed)

    @commands.command(description="Gets the user's info", aliases=['ui'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
      if member == None:
        member = ctx.author
        embed = discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {member}.", colour=discord.Colour.blue())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="NAME", value=member.mention, inline=False)
        embed.add_field(name="NICKNAME", value=member.nick, inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="STATUS", value="Online", inline=False)
        embed.add_field(name="TOP ROLE", value=member.top_role.mention, inline=False)
        await ctx.send(embed=embed)
      else:
        embed = discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {member}.", colour=discord.Colour.blue())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="NAME", value=member.mention, inline=False)
        embed.add_field(name="NICKNAME", value=member.nick, inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="STATUS", value="Online", inline=False)
        embed.add_field(name="TOP ROLE", value=member.top_role.mention, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='userperms', description='Gets the permisisons of an user!')
    async def userperms(self, ctx, user: discord.Member = None):
        perms_array = user.permissions_in(ctx.channel)
        await ctx.send(perms_array)

def setup(bot):
    bot.add_cog(Info(bot))