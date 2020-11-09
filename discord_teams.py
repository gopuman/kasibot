import discord
import re
import numpy as np
from itertools import combinations
import os
from os import environ
import random


pattern = "\$cleps [0-9]"
TOKEN = environ["API_KEY"]

n = ['anishkasi', 'Wolfinthehouse', 'pindabc', 'aprbhd', 'the_week', 'JakeSuli', 'gopuman', 'akshara', 'greybeard278', 'Dobby']
nicknames = {
        'anishkasi': set(['kasi','anishkasi','kass','kmaams','lebron','dumbbitch!']),
        'Wolfinthehouse': set(['neil','pratith','juice','Wolfinthehouse','neilesh','benadryl']),
        'pindabc': set(['pinds','yogesh','dips','pindabc','upsc','nipflix']),
        'aprbhd' : set(['apar','jose','aprbhd','apr','appameya']),
        'the_week' : set(['aveek','tupperware','shelly','pt','anxx','telegram','tacobell','tapori']),
        'JakeSuli' : set(['arvi','ssr','ronnie','jakesuli']),
        'gopuman': set(['gops','chilly','gopuman']),
        'akshara': set(['akshara','hak','omg']),
        'greybeard278': set(['paro','greybeard278','parz','yawn']), # gops add some funny nickname for me and paro  and others also if you can
        'Dobby': set(['dobby','kuneil','dpdp','google']),
        }

weights = {
        'anishkasi': 2.3 + 0.81*3,
        'Wolfinthehouse': 3.5 + 0.86*3,
        'pindabc': 2.1 + 0.8*3,
        'aprbhd' : 2.3 + 0.78*3,
        'the_week' : 1 + 0.8*3,
        'JakeSuli' : 2 + 0.83*3,
        'gopuman': 2.25 + 0.85*3,
        'akshara': 1.3 + 0.78*3,
        'greybeard278': 1.5 + 0.77*3,
        'Dobby': 1.2 + 0.76*3,
        }

def return_names(split):
    names = []
    ss = set(split)
    for key,val in nicknames.items():
        if(len(val.intersection(ss)) >= 1):
            names.append(key)
    return names

def create_weighted_team(names,num_teams):
    tol = 2
    numppl = len(names)//num_teams
    if(num_teams == 2):
        combs = list(combinations(names,numppl))
        other_team = [[i for i in names if i not in s] for s in combs]
        team_scores = np.array([sum([weights[i] for i in s]) for s in combs])
        other_team_scores = np.array([sum([weights[i] for i in s]) for s in other_team])
        diff_in_scores = np.abs(team_scores - other_team_scores)
        inds = np.where(diff_in_scores < tol)[0]
        ttp = np.array(combs)
        ttp = ttp[inds]
        np.random.shuffle(ttp)
        final_team = list(ttp[0])
        final_other_team = [i for i in names if i not in final_team]
        return final_team,final_other_team

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

def filterOnlyOnlineMembers(member):
    return member.status != discord.Status.offline and not member.bot

def online_members(message):
    guild = message.guild 
    vc = guild.voice_channels
    mems = []
    for i in vc:
        members = i.members
        mems.extend(members)
    return [i.name for i in mems]
    
@client.event
async def on_message(message):
    if(message.content == "help"):
        output = []
        for key,value in nicknames.items():
            conc = key.capitalize() + ': ' + ', '.join(value) + '\n\n'
            output.append(conc)
        msg1 = "You can refer to the members using any one of these: \n\n"
        msg2 = " ".join(output)
        msg3 = "##~~ Made by Anish Kasi ~~##"
        msg = msg1+msg2+msg3
        await message.channel.send(msg) 
    z = re.findall(pattern,message.content)
    if(len(z) > 0):
        split_msg = message.content.split(" ")
        exclude = return_names(split_msg)
        names = online_members(message)
        names = [i for i in names if i not in exclude]
        print(names)
        if("-w" in split_msg):
            t1,t2 = create_weighted_team(names,2)

            embed = discord.Embed(
                title = "Weighted Teams Generated\n",
                colour = discord.Colour.blue()
                )
            nl = "\n"
            embed.add_field(name="__Team A__", value=f"**{nl.join(t1)}**", inline=True)
            embed.add_field(name="__Team B__", value=f"**{nl.join(t2)}**", inline=True)

            await message.channel.send(embed=embed)
        #onlineMembersCount = len(onlineMembersInServer)
        else:
            numteams = int(z[0][-1])
            np.random.shuffle(names)
            if(numteams == 3):
                msg1 = names[0:3]
                msg2 = names[3:6]
                msg3 = names[6:9]
                embed = discord.Embed(
                title = "Teams Generated\n",
                colour = discord.Colour.blue()
                )
                nl = "\n"
                embed.add_field(name="__Team A__", value=f"**{nl.join(msg1)}**", inline=True)
                embed.add_field(name="__Team B__", value=f"**{nl.join(msg2)}**", inline=True)
                embed.add_field(name="__Team C__", value=f"**{nl.join(msg3)}**", inline=True)
                await message.channel.send(embed=embed)
            
            elif(numteams == 2):
                msg1 = names[:4]
                msg2 = names[4:]
                embed = discord.Embed(
                title = "Teams Generated\n",
                colour = discord.Colour.blue()
                )
                nl = "\n"
                embed.add_field(name="__Team A__", value=f"**{nl.join(msg1)}**", inline=True)
                embed.add_field(name="__Team B__", value=f"**{nl.join(msg2)}**", inline=True)
                await message.channel.send(embed=embed)
                
            else:
                msg = " ".join(names)
                await message.channel.send(msg)

@client.event
async def on_voice_state_update(member, before, after):
    user = str(member).split("#")[0]
    s = nicknames[user]
    channel = client.get_channel(443835387438301196)
    if before.channel is None and after.channel is not None:
        await channel.send('Welcome, ' + random.choice(tuple(s)).capitalize())

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
