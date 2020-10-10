import requests
from bs4 import BeautifulSoup as scrapper
from discord.ext import commands
import os
from cricbot_api import *
import random

choices = ["CSK", "RR"]

base_url = 'https://www.cricbuzz.com/cricket-match/'


class Urls:
    URL1 = base_url + 'live-scores'
    ##URL2 = base_url + 'live-scores/upcoming-matches'
    URL2 = 'http://mapps.cricbuzz.com/cbzios/match/30369/scorecard'
    #URL3 = 'https://www.cricbuzz.com/api/html/cricket-scorecard/30350'
    URL3 = 'https://www.cricbuzz.com/api/cricket-match/commentary/30354'


def soup(url):
    response = requests.get(url)
    bsoup = scrapper(response.content, 'html.parser')
    return bsoup


iterator = 0


client = commands.Bot(command_prefix='*')


@client.event
async def on_ready():
    print('bot is running.')


@client.command()
async def score(ctx, index_number=0):
    try:
        await ctx.send(get_live_status(int(index_number), soup(Urls.URL1)))
    except:
        await ctx.send('No match available at position {}'.format(str(index_number)))


@client.command()
async def winner(ctx):
    try:
        await ctx.send(random.choice(choices))
    except:
        await ctx.send('Oops.. something went wroong.')


@client.command()
async def schedule(ctx, index_number=0):
    try:
        await ctx.send(get_match_schedule(int(index_number), soup(Urls.URL2)))
    except:
        # await ctx.send('No match available for {}'.format(str(index_number)))
        await ctx.send(soup(Urls.URL2))


@client.command()
async def status(ctx):
    try:
        await ctx.send(get_match_status(soup(Urls.URL1)))
    except:
        await ctx.send('Match on the way.')


@client.command()
async def disconnect(ctx):
    await ctx.send('Ok. Bye.')
    await client.logout()

auth_token = os.environ.get('DISCORD_BOT_TOKEN')
#auth_token = open('api_key.txt', 'r')
client.run(auth_token)
