# bot.py
# The SimpleDatabaseBot.py
# This python script hosts a discord bot which can b used to access your
# firebase database and pull/push data to/from it. I built this bot off the
# model of my SimpleElections discord bot.

#Set up instructions:
# 1. Create a Firebase Project
# 2. Set up a RealtimeDatabase
# 3. Create an application on Firebase and copy the config data over:
# 4. Download a service account json file from Firebase
# 5. Link the service account in your config data
# 6. Create discord bot on your developers account
# 7. Copy the discord bot's token
# 8. Enable Intents on your discord bot
# 9. Import pyrebase.py, and discord.py via PIP.
# 10. Run the bot and run pullData and pushData commands


import os
import random
from discord.ext import commands
import discord
import csv
import pyrebase
import os
import string


config = {
    "apiKey":"",
    "authDomain":"[data].firebaseapp.com",
    "databaseURL":"https://[database].firebaseio.com/",
    "storageBucket":"[databasename].appspot.com",
    "projectId": "",
     "serviceAccount": os.getcwd()+r"/path/filename.json",
    }
email = 'email'
password='password'


firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
user = auth.sign_in_with_email_and_password(email, password)
user = auth.refresh(user['refreshToken'])

# Get a reference to the database service
db = firebase.database()
dbMain = db.get()
ALL_DATA = dbMain.val()
#print(ALL_DATA)


command_prefix1='!'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=command_prefix1,intents=intents)


#runs when bot starts
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    #print(bot.guilds)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=command_prefix1+"help"))
 
#runs when bot is added to a discord server
@bot.event
async def on_guild_join(guild):
    db.child('servers').child(guild.name+str(guild.id)).child('Data').set({'None':'None'})     

#runs when the bot detects that a message has been sent
@bot.event
async def on_message(message):
    if message.guild is None and message.author != bot.user:
        print(message)
    elif message.content == command_prefix1+"help":
        embed = discord.Embed(title="Commands:", description="List of commands accessible") #,color=Hex code
        embed.add_field(name="{0}commandName".format(command_prefix1), value="Command Description")
        embed.add_field(name="{0}commandName".format(command_prefix1), value="Command Description")
        embed.add_field(name="{0}commandName".format(command_prefix1), value="Command Description")
        await message.channel.send(embed=embed)
        embed2 = discord.Embed(title="Commands Page 2:",description="List of commands accessible")
        embed2.add_field(name="{0}comandName *field*".format(command_prefix1),value="Description")
        embed2.add_field(name="{0}comandName *field*".format(command_prefix1),value="Description")
        embed2.add_field(name="{0}comandName *field*".format(command_prefix1),value="Description")
        await message.channel.send(embed=embed2)
    else:
        await bot.process_commands(message)

#push data to the database
@bot.command()
async def pushData(ctx,*,data):
    if(ctx.author.guild_permissions.administrator):
        server = ctx.guild.name+str(ctx.guild.id)
        db.child('servers').child(server).set({"myData":data})
       
        await ctx.send("Data uploaded")
    else:
        await ctx.send('Insuffient permissions')

#pull data from the database
@bot.command()
async def pullData(ctx):
        server = ctx.guild.name+str(ctx.guild.id)
        data= db.child('servers').child(server).child('myData').get().val()
        await ctx.send("Data pulled:"+data)


#get the number of servers the bot has been added to, as registed by your databse
@bot.command(pass_context = True)
async def ServerCount(ctx):
    await ctx.send("Bot is in: "+str(len(db.child('servers').get().val()))+" servers")

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
#alternatively you can run
#bot.run("PASTE TOKEN HERE")
