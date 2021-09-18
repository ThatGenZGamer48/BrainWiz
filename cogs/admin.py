import discord
from discord.ext import commands
from time import sleep
import asyncio
import random

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban", description="Bans a specified person.")
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
      if reason != None:
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} for **{reason}**!")
      else:
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}!')

    @commands.command(description="Kicks a specified person.")
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
      if reason != None:
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention} for **{reason}**!")
      else:
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention}!")

    @commands.command(description="Unbans a specified person.", colour=discord.Colour.purple())
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def unban(self, ctx, *, member):
        bannedUsers = await ctx.guild.bans
        name, discriminator = member.split

        for ban in bannedUsers:
            user = ban.user

            if (user.name, user.discriminator) == (name, discriminator):
                await ctx.guild.unban(user)
              
                await ctx.send(f'Unbanned {member.mention}!')
                return

    @commands.command(description="Clears specified amount of messages", aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def clear(self, ctx, amount=5):
      await ctx.channel.purge(limit=amount)
      clearMsg = f"<a:blacktick:799587961313296384> Cleared {amount} messages"
      embed = discord.Embed(title="Clear", description=clearMsg, colour=discord.Colour.blue())
      message = await ctx.send(embed=embed)
      sleep(5)
      await message.delete()

    @commands.command(description="Creates a channel", aliases=['create_text_channel', 'create_text'])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ocreate_text_channel(self, ctx, channelName):
      await ctx.guild.create_text_channel(channelName)
      await ctx.message.delete()
      await ctx.send(f"{channelName} channel has been created!")
      
    @commands.command(description="Creates a category", aliases=['create_category', 'create_cat'])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ocreate_category(self, ctx, categoryName):
      await ctx.guild.create_category(categoryName)
      await ctx.message.delete()
      await ctx.send(f"{categoryName} category has been made")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, mute_time, member: discord.Member=None, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')
        if not member:
            await ctx.send("Mention a member to mute!")
            return
        
        if not mutedRole:
          mutedRole = await guild.create_role(name='Muted')
          for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=False, read_messages=False)

        seconds = 0
        if mute_time.lower().endswith("d"):
            seconds += int(mute_time[:-1]) * 60 * 60 * 24
        if mute_time.lower().endswith("h"):
            seconds += int(mute_time[:-1]) * 60 * 60
        elif mute_time.lower().endswith("m"):
            seconds += int(mute_time[:-1]) * 60
        elif mute_time.lower().endswith("s"):
            seconds += int(mute_time[:-1])

        current_roles = member.roles

        await member.add_roles(mutedRole)
        await member.edit(roles=[mutedRole])
        await ctx.send(f"Muted {member.mention} for {mute_time}!")
        await member.send(f'You were muted for {mute_time} in the server {guild.name} for reason "{reason}"')

        await asyncio.sleep(seconds)
        await member.remove_roles(mutedRole)
        await member.edit(roles=current_roles)
        await member.send(f'You were unmuted {member.mention}, time period has expired!')
        await ctx.send(f"{member.mention} was unmuted because his time period expired!")

    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await ctx.send(f"Unmuted {member.mention}")
        await member.send(f"You were unmuted in the server {ctx.guild.name}")

        @commands.command(name='delete_channel', description='Deletes a specified channel', aliases=['dc'])
        @commands.has_permissions(manage_channels=True, aliases=['remove_text_channel', 'delete_text_channel'])
        async def _delete_text_channel(self, ctx, channel: discord.TextChannel = None, *, reason=None):
          if channel == None:
            channel = ctx.channel
          await channel.delete(reason=reason)
          await ctx.send(f'Deleted channel `{channel}` for reason `{reason}`')


    @commands.command(name='add_role', description='Adds a specified role to a specified member')
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def add_role(self, ctx, role: discord.Role, member: discord.Member = None):
      if member == None:
        member = ctx.author
      await member.add_roles(role)
      await ctx.send(f'Added {role.mention} role to {member.mention}')

    @commands.command(name='remove_role', description='Removes a specified role from a specified member')
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def remove_role(self, ctx, role: discord.Role, member: discord.Member = None):
      if member == None:
        member = ctx.author
      await member.remove_roles(role)
      await ctx.send(f'Removed {role.mention} role from {member.mention}')
    
    @commands.command(name='create_role', aliases=['cr'])
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def create_role(self, ctx, name):
        await ctx.guild.create_role(name=name)
        await ctx.send(f'Created role \'{name}\'!')

    @commands.command(description='Warns a specified member.')
    async def warn(ctx, member: discord.Member):
      await ctx.send(f'Ok! I warned {member}')
    @commands.command(description="Server deafens a member.")
    @commands.has_permissions(manage_channels=True)
    async def set_deafen(self, ctx, member: discord.Member):
      await member.edit(deafen=True)
      await ctx.send(f"I have deafened {member}.")
    @commands.command(description="Undeafens a member.")
    @commands.has_permissions(manage_channels=True)
    async def remove_deafen(self, ctx, member: discord.Member):
      await member.edit(deafen=False)
      await ctx.send(f"I have undeafened {member}")

    @commands.command(name='lock', aliases=['lockdown', 'shutdown'])
    async def lock(self, ctx, channel: discord.TextChannel = None):
      if channel == None:
        channel = ctx.channel
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f'{ctx.channel} has been locked!')
      else:
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f'{channel} has been locked!')

    @commands.command(name='unlock', aliases=['remove-lock, removelock, unlockdown'])
    async def unlock(self, ctx, channel: discord.TextChannel = None):
      if channel == None:
        channel = ctx.channel
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f'{ctx.channel} has been unlocked!')
      else:
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f'{channel} has been unlocked!')

    @commands.command(name='randomNumbers')
    async def random_numbers(self, ctx, noOfNumbers):
      if noOfNumbers == None:
        await ctx.send(f"{str(random.randint(0, 99)) * 5}")
      else:
        await ctx.send(f"{str(random.randint(0, 99)) * noOfNumbers}")

def setup(bot):
    bot.add_cog(Admin(bot))
