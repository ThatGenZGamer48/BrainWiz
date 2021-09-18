import discord
from discord.ext import commands
import json
import random

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add command!
    @commands.command(description="Adds two numbers.")
    async def add(self, ctx, num1, num2):
        total = int(num1) + int(num2)
        await ctx.message.delete()
        await ctx.send(f"When you add {num1} and {num2}, you get {str(total)}")

    # Multiply command!
    @commands.command(description="Multiplies two numbers.", aliases=['mult', 'mul', 'm'])
    async def multiply(self, ctx, num1, num2):
        total = int(num1) * int(num2)
        await ctx.message.delete()
        await ctx.send(f"When you multiply {num1} and {num2}, you get {str(total)}")

    # Divide command!
    @commands.command(description="Divides two numbers.", aliases=['div', 'd'])
    async def divide(self, ctx, num1, num2):
        total = int(num1) / int(num2)
        await ctx.message.delete()
        await ctx.send(f"When you divide {num1} and {num2}, you get {str(total)}")

    # Subtract command!
    @commands.command(description="Subtracts two numbers.", aliases=['sub', 's'])
    async def subtract(self, ctx, num1, num2):
        total = int(num1) - int(num2)
        await ctx.message.delete()
        await ctx.send(f"When you subtract {num1} and {num2}, you get {str(total)}")
    
    # Generates a random number for ya.
    @commands.command(description="Gives the user a random number")
    async def randomnumber(self, ctx):
      await ctx.message.delete()
      await ctx.send(f'Here is a random number between 1 and 100: {random.randint(0, 100)}')

    # Exponent command!
    @commands.command(description="Adds two numbers.", aliases=['exponents', 'exp', 'exponen', ''])
    async def exponent(self, ctx, num1, num2):
        total = int(num1) ** int(num2)
        await ctx.message.delete()
        await ctx.send(f"When you add {num1} and {num2}, you get {str(total)}")

def setup(bot):
    bot.add_cog(Math(bot))
