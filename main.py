import discord
from discord.ext import commands
import random 
import json
from configtemplate import PREFIX, DEVELOPER_ID, DEVELOPER_NAME
import os
import asyncio
import datetime
# import keep_alive

# keep_alive.keep_alive()

token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.reactions = True
intents.messages = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(PREFIX),
    intents=intents,
    description="A bot made for simple utilities",
    case_insensitive=True
)

bot.remove_command("help")
    
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.listening, name=f"{PREFIX}help")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print(f"{bot.user} is ready!")

@bot.event
async def on_command_error(ctx, error):
    ignored = (commands.UserInputError)
    if isinstance(error, ignored):
        print('COMMANDIGNOREDERROR: WRONG USER INPUT')

    if isinstance(error, commands.CommandOnCooldown):
        print('COMMANDCOOLDOWNERROR: COMMAND USED BEFORE COOLDOWN ENDED')
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f'You must wait {int(s)} seconds before using this command once more! Please wait...')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f'You must wait {int(m)} minutes and {int(s)} seconds before using this command once more! Please wait...')
        else:
            await ctx.send(f'You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds before using this command once more! Please wait...')

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey! You don't have enough permissions to use this command.")
        raise error

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Hey! The command is missing an important argument!")
        raise error

# Commands for cogs, loadcog and unloadcog.

@bot.command(name="loadcog", description="Loads all the cogs")
@commands.cooldown(1, 30, commands.BucketType.user)
@commands.has_permissions()
async def loadcog(ctx, cog):
    bot.load_extension(f"cogs.{cog}")
    
    await ctx.send(f"Loaded cog {cog}.")
    member = ctx.author.name
    print(f'{member} just used the loadcog command!')

@bot.command(name="unloadcog", description="Unloads all the cogs")
@commands.cooldown(1, 30, commands.BucketType.user)
async def unloadcog(ctx, cog):
    bot.unload_extension(f"cogs.{cog}")
    await ctx.send(f"Unloaded cog {cog}.")
    member = ctx.author.name
    print(f'{member} just used the unloadcog command!')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command()
async def help(ctx, arg="Not specified"):
    if arg == "Not specified":
        categoryEmbed = discord.Embed(title='Help!', description='Get help by using -help <category>. The categories are below', color=discord.Color.blue())
        categoryEmbed.add_field(name='Admin', value='`-help admin`')
        categoryEmbed.add_field(name='Fun', value='`-help fun`')
        categoryEmbed.add_field(name='Math', value='`-help math`')
        categoryEmbed.add_field(name='Info', value='`-help info`')
        categoryEmbed.add_field(name='Bot', value='`-help bot`')
        # categoryEmbed.add_field(name='Economy', value='`-help economy`')
        await ctx.send(embed=categoryEmbed)
    elif arg.lower() == 'admin':
        adminEmbed = discord.Embed(title='Admin', description='`ban`, `unban`, `kick`, `purge`, `mute`, `unmute`, `create_text_channel`, `create_category`, `lock`, `unlock`', color=discord.Color.blue())
        await ctx.send(embed=adminEmbed)
    elif arg.lower() == 'fun':
        funEmbed = discord.Embed(title='Fun', description='`8ball`, `fakemute`, `webhook`, `dice`, `coin`, `gen_nitro`, `epicgamerrate`, `pograte`', color=discord.Color.blue())
        await ctx.send(embed=funEmbed)
    elif arg.lower() == 'info':
        infoEmbed = discord.Embed(title='Info', description='`ping`, `userinfo`, `serverinfo`, `servercount`, `stats`, `pfp`, `invite`', color=discord.Color.blue())
        await ctx.send(embed=infoEmbed)
    elif arg.lower() == 'math':
        mathEmbed = discord.Embed(title='Math', description='`add`, `subtract`, `multiply`, `divide`, `exponent`', color=discord.Color.blue())
        await ctx.send(embed=mathEmbed)
    elif arg.lower() == 'bot':
        botEmbed = discord.Embed(title='Bot', description='`invite`, `supportserver`, `report`, `suggest`, `credits`, `stats`, `guilds`', color=discord.Color.blue())
        await ctx.send(embed=botEmbed)
    else:
        await ctx.send("Invalid cog specified! Please pick a category from one of these:\n`Admin`\n`Fun`\n`Info`\n`Math`\n`Bot`")

@bot.command()
@commands.has_permissions(administrator=True)
async def gstart(ctx, mins: int, *, prize: str):
  embed = discord.Embed(title=prize, color=discord.Color.blue())
  end = datetime.datetime.utcnow() + datetime.timedelta(seconds = round(mins*60))
  embed.add_field(name='Ends at', value=f'{end} UTC')
  embed.set_footer(text=f'Ends: {mins} minutes')
  giveaway = await ctx.send(embed=embed)
  await giveaway.add_reaction('🎉')
  await asyncio.sleep(mins*60)
  giveawayEndMsg = await ctx.channel.fetch_message(giveaway.id) 
  users = await giveawayEndMsg.reactions[0].users().flatten()
  users.pop(users.index(bot.user))
  winner = random.choice(users)
  await ctx.send(f'Congratulations! {winner.mention} won the giveaway for {prize}!')

def convert(time):
  pos = ['s', 'm', 'h', 'd']
  time_dict = {'s': 1, 'm': 60, 'h': 3600, 'd': 3600*24}
  unit = time[1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2
  return val * time_dict[unit]

@bot.command(aliases=['rl'])
@commands.is_owner()
async def reload(ctx, cog):
  async with ctx.channel.typing():
    if ctx.author.id == 780414447894134794:
      if cog == 'all':
        message = await ctx.send('Starting reload...')
        for filename in os.listdir('./cogs'):
          if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')
            await message.edit(content=f'Unloaded {filename}')
            bot.load_extension(f'cogs.{filename[:-3]}')
            await message.edit(content=f'Loaded {filename}')
        await message.edit(content='Reloaded all cogs!')
      else:
        message = await ctx.send('Starting reload...')
        await asyncio.sleep(2)
        bot.unload_extension(f'cogs.{cog}')
        await message.edit(content=f'Unloading cog `{cog}`')
        bot.load_extension(f'cogs.{cog}')
        await asyncio.sleep(2)
        await message.edit(content=f'Reloading cog `{cog}`')
        await asyncio.sleep(2)
        await message.edit(content=f'Reloaded cog `{cog}`')
    else:
      await ctx.send('Hey you aren\'t allowed to use this command!')

'''@bot.command(aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f'{ctx.author.name} Balance',color = discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance',value=bank_amt)
    await ctx.send(embed= em)

@bot.command()
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(101)

    embed = discord.Embed(title = "Beg", description = f"{ctx.author.mention} Got {earnings} coins!!", color = discord.Color.gold())
    await ctx.send(embed=embed)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)


@bot.command(aliases=['wd'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,'bank')
    embed = discord.Embed(title = "Withdraw", description = f'{ctx.author.mention} You withdrew {amount} coins', color = discord.Color.gold())
    await ctx.send(embed=embed)


@bot.command(aliases=['dp'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,'bank')
    embed = discord.Embed(title = "Deposit", description = f'{ctx.author.mention} You deposited {amount} coins', color = discord.Color.gold())
    await ctx.send(embed=embed)


@bot.command(aliases=['sm', 'give'])
async def send(ctx,member : discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount,'bank')
    await update_bank(member,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')


@bot.command(aliases=['rb'])
async def rob(ctx,member : discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)


    if bal[0]<100:
        await ctx.send('It is useless to rob him :(')
        return

    earning = random.randrange(0,bal[0])

    await update_bank(ctx.author,earning)
    await update_bank(member,-1*earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')


@bot.command()
async def slots(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice(['X','O','Q'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author,2*amount)
        await ctx.send(f'You won :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f'You lose :( {ctx.author.mention}')


@bot.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)



@bot.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@bot.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]
    

@bot.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.7* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]


@bot.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = bot.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return True


async def get_bank_data():
    with open('mainbank.json','r') as f:
        users = json.load(f)

    return users


async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal'''



bot.run(str(token))
