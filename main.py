import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!')

#Input your bot Token here.
token = "TokenTokenToken"

#Input the Discord ID's of the users you want to be able to use the !add and !delete commands.
userIDS = [ID1, ID2, ID3, ...]

if not (os.path.isfile('response.txt')):
    f= open("response.txt","w+")
    f.close()

@bot.event
async def on_ready():
    print("Ready!")


@bot.event
async def on_message(message):
   
    with open("response.txt","r") as f:
        filedata = f.read()
    try:
        filedata = filedata.split("!$!")
    except Exception as e:
        print(e)
    
    msgList = []
    respList = []
    for i in filedata:
        if i !="":
            msgList.append(i.split("~")[0].lower())
            respList.append(i.split("~")[1])
    if message.content.lower() in msgList:
        response = respList[msgList.index(message.content.lower())]
        await message.channel.send(response)
   
    await bot.process_commands(message)
    
@bot.command()
async def add(ctx,*,arg):
    if ctx.author.id in userIDS:
        with open("response.txt","r") as f:
            filedata = f.read()
        try:
            filedata = filedata.split("!$!")
        except Exception as e:
            print(e)
        _message = arg.split("~")[0]
        rsp =arg.split("~")[1]
        print(f"New pair add request -> {_message} : {rsp}")
        msgList = []
        for i in filedata:
            if i !="":
                msgList.append(i.split("~")[0].lower())
        if _message.lower() in msgList:
            embed=discord.Embed(title="Couldn't Add", description=f"Message **\'{arg}\'** already exists!", color=0xff0000)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Message Pair Added!", description=f"Response message have been added!", color=0x00ff00)
            embed.add_field(name="Message", value=_message, inline=True)
            embed.add_field(name="Response", value=rsp, inline=True)
            await ctx.send(embed=embed)
            filedata.append(_message+"~"+rsp)
            with open("response.txt","w") as f:
                f.write("!$!".join(filedata))
    
    

   
@bot.command()
async def delete(ctx,*,arg):
    if ctx.author.id in userIDS:
        with open("response.txt","r") as f:
            filedata = f.read()
        try:
            filedata = filedata.split("!$!")
        except Exception as e:
            print(e)
        msgList = []
        respList = []
        for i in filedata:
            if i !="":
                msgList.append(i.split("~")[0].lower())
                respList.append(i.split("~")[1].lower())
        if arg.lower() in msgList:
            indx = msgList.index(arg.lower())+1
            filedata.pop(indx)
            embed=discord.Embed(title="Message Pair Deleted!", description=f"Message for pair have been deleted!", color=0x00ff00)
            embed.add_field(name="Message", value=arg, inline=True)
            embed.add_field(name="Response", value=respList[msgList.index(arg.lower())], inline=True)
            await ctx.send(embed=embed)
            
        else:
            embed=discord.Embed(title="Couldn't Find", description=f"Message **\'{arg}\'** does not exists!", color=0xff0000)
            await ctx.send(embed=embed)
        
        with open("response.txt","w") as f:
            f.write("!$!".join(filedata))

bot.run(token)
