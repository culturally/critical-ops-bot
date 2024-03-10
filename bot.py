import discord
import asyncio
import requests
from discord.ext.commands import Bot
from discord.ext import commands
import datetime
import time
import json
import re

PREFIX = ("-") #Prefix feel free to choose your own
intents = discord.Intents.all()
intents.members = True
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
bot = commands.Bot(case_insensitive=True,intents=intents, command_prefix=PREFIX,help_command = help_command)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your house"))
    print("on!")
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument.")

@bot.command(aliases=['u'])
async def username(ctx, *what):
    """ Info Lookup about player by Username""" #Command description
    if not what:  # Check if any arguments were provided
        await ctx.send("Please provide a username.")
        return

    user = ''.join(what)
    url = "https://1-44-1.prod.copsapi.criticalforce.fi/api/public/profile?usernames=" + user
    response = requests.get(url)
    text = response.text
    


    if "Error 53" in text:
        await ctx.send("User not found.")
        return
    
    # Splitting the text by lines
    lines = text.split('\n')
    # Initialize variables to store extracted information
    user_info = {}
    clan_info = {}
    banned = True

    # Variable to keep track of whether we are parsing user info or clan info
    parsing_user_info = True

    for line in lines:
        # Extracting user information
        if "'userID'" in line:
            user_info['userID'] = int(line.split('=>')[1].strip().rstrip(','))
        elif "'name'" in line:
            if parsing_user_info:
                user_info['name'] = line.split('=>')[1].strip().strip("',")
            else:
                clan_info['name'] = line.split('=>')[1].strip().strip("',")
                parsing_user_info = True
        elif "'playerLevel'" in line:
            user_info['playerLevel'] = {}
        elif "'level'" in line:
            user_info['playerLevel']['level'] = int(line.split('=>')[1].strip().rstrip(','))
        elif "'current_xp'" in line:
            user_info['playerLevel']['current_xp'] = int(line.split('=>')[1].strip().rstrip(','))
        elif "'next_level_xp'" in line:
            user_info['playerLevel']['next_level_xp'] = int(line.split('=>')[1].strip().rstrip(','))
        elif "'blockFriendRequests'" in line:
            user_info['blockFriendRequests'] = line.split('=>')[1].strip().rstrip(',')
        elif "'block_clan_requests'" in line:
            user_info['block_clan_requests'] = line.split('=>')[1].strip().rstrip(',')
        elif "'ban' => NULL" in line:
            banned = False
        elif "\CriticalOps\Classes\Enums\BanType::" in line:
            line_without_substring = line.replace("\CriticalOps\Classes\Enums\BanType::", "")
            user_info['banType'] = line_without_substring.rstrip(',')
        elif "\CriticalOps\Classes\Enums\BanReason::" in line:
            line_without_substring = line.replace("\CriticalOps\Classes\Enums\BanReason::", "")
            user_info['banReason'] = line_without_substring.rstrip(',')
        elif "'tag'" in line:
            clan_info['tag'] = str(line.split('=>')[1].strip().rstrip(',')).strip("',")
        elif "'clan'" in line:
            parsing_user_info = False

    # Embed
    embed = discord.Embed(title="User Information", color=discord.Color.red())
    embed.add_field(name="User ID", value=user_info.get('userID', 'N/A'), inline=True)
    embed.add_field(name="Account Name", value=user_info.get('name', 'N/A'), inline=True)
    embed.add_field(name="Player Level", value=user_info.get('playerLevel', {}).get('level', 'N/A'), inline=True)
    embed.add_field(name="Current XP", value=user_info.get('playerLevel', {}).get('current_xp', 'N/A'), inline=True)
    embed.add_field(name="Next Level XP", value=user_info.get('playerLevel', {}).get('next_level_xp', 'N/A'), inline=True)
    embed.add_field(name="Block Friend Requests", value=user_info.get('blockFriendRequests', 'N/A'), inline=True)
    embed.add_field(name="Block Clan Requests", value=user_info.get('block_clan_requests', 'N/A'), inline=True)
    if banned:
        embed.add_field(name="Banned", value="True", inline=True)
        embed.add_field(name="Ban Type", value=user_info.get('banType', 'N/A'), inline=True)
        embed.add_field(name="Ban Reason", value=user_info.get('banReason', 'N/A'), inline=True)
    else:
        embed.add_field(name="Banned", value="False", inline=True)
    embed.add_field(name="Clan Name", value=clan_info.get('name', 'N/A'), inline=True)
    embed.add_field(name="Clan Tag", value=clan_info.get('tag', 'N/A'), inline=True)

    await ctx.send(embed=embed)

@bot.command(aliases=['id'])
async def ids(ctx, *what):
    """ Info Lookup about player by ID"""
    if not what:  # Check if any arguments were provided
        await ctx.send("Please provide an id.")
        return

    user = ''.join(what)
    url = "https://1-44-1.prod.copsapi.criticalforce.fi/api/public/profile?ids=" + user
    response = requests.get(url)
    text = response.text
    


    if "Error 53" in text:
        await ctx.send("User not found.")
        return
    
    # Splitting the text by lines
    lines = text.split('\n')
    # Initialize variables to store extracted information
    user_info = {}
    clan_info = {}
    banned = True

    # Variable to keep track of whether we are parsing user info or clan info
    parsing_user_info = True

    for line in lines:
        # Extracting user information
        if "'userID'" in line:
            user_info['userID'] = int(line.split('=>')[1].strip().rstrip(','))
        elif "'name'" in line:
            if parsing_user_info:
                user_info['name'] = line.split('=>')[1].strip().strip("',")
            else:
                clan_info['name'] = line.split('=>')[1].strip().strip("',")
                parsing_user_info = True
        elif "'playerLevel'" in line:
            user_info['playerLevel'] = {}
        elif "'level'" in line:
            user_info['playerLevel']['level'] = int(line.split('=>')[1].strip().rstrip(','))
        elif "'current_xp'" in line:
            user_info['playerLevel']['current_xp'] = int(line.split('=>')[1].strip().rstrip(','))
        elif "'next_level_xp'" in line:
            user_info['playerLevel']['next_level_xp'] = int(line.split('=>')[1].strip().rstrip(','))
        elif "'blockFriendRequests'" in line:
            user_info['blockFriendRequests'] = line.split('=>')[1].strip().rstrip(',')
        elif "'block_clan_requests'" in line:
            user_info['block_clan_requests'] = line.split('=>')[1].strip().rstrip(',')
        elif "'ban' => NULL" in line:
            banned = False
        elif "\CriticalOps\Classes\Enums\BanType::" in line:
            line_without_substring = line.replace("\CriticalOps\Classes\Enums\BanType::", "")
            user_info['banType'] = line_without_substring.rstrip(',')
        elif "\CriticalOps\Classes\Enums\BanReason::" in line:
            line_without_substring = line.replace("\CriticalOps\Classes\Enums\BanReason::", "")
            user_info['banReason'] = line_without_substring.rstrip(',')
        elif "'tag'" in line:
            clan_info['tag'] = str(line.split('=>')[1].strip().rstrip(',')).strip("',")
        elif "'clan'" in line:
            parsing_user_info = False

    # Embed
    embed = discord.Embed(title="User Information", color=discord.Color.red())
    embed.add_field(name="User ID", value=user_info.get('userID', 'N/A'), inline=True)
    embed.add_field(name="Account Name", value=user_info.get('name', 'N/A'), inline=True)
    embed.add_field(name="Player Level", value=user_info.get('playerLevel', {}).get('level', 'N/A'), inline=True)
    embed.add_field(name="Current XP", value=user_info.get('playerLevel', {}).get('current_xp', 'N/A'), inline=True)
    embed.add_field(name="Next Level XP", value=user_info.get('playerLevel', {}).get('next_level_xp', 'N/A'), inline=True)
    embed.add_field(name="Block Friend Requests", value=user_info.get('blockFriendRequests', 'N/A'), inline=True)
    embed.add_field(name="Block Clan Requests", value=user_info.get('block_clan_requests', 'N/A'), inline=True)
    if banned:
        embed.add_field(name="Banned", value="True", inline=True)
        embed.add_field(name="Ban Type", value=user_info.get('banType', 'N/A'), inline=True)
        embed.add_field(name="Ban Reason", value=user_info.get('banReason', 'N/A'), inline=True)
    else:
        embed.add_field(name="Banned", value="False", inline=True)
    embed.add_field(name="Clan Name", value=clan_info.get('name', 'N/A'), inline=True)
    embed.add_field(name="Clan Tag", value=clan_info.get('tag', 'N/A'), inline=True)

    await ctx.send(embed=embed)
 
bot.run('') # INPUT HERE YOUR TOKEN