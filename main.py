import os
import requests
import discord
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    notification.start()
    print(f"We have logged in as {bot.user}")
    try:
        await bot.tree.sync()
    except Exception as e:
        print(f'Could not sync commands: {e}')

revealed = False


@tasks.loop(seconds=3)
async def notification():
    global revealed
    r = requests.get(
        "https://store.steampowered.com/app/1030300/Hollow_Knight_Silksong/"
    )
    soup = BeautifulSoup(r.content, "html.parser")
    release_date = soup.find_all("div", {"class": "date"})[0].get_text()
    if release_date == "To be announced" and revealed == False:
        print(f"Release date: {release_date}")
        pass
    elif release_date != "To be announced" and revealed == False:
        for guild in bot.guilds:
            if guild.system_channel:
                await guild.system_channel.send("The release date has just been updated to: " + release_date)
        revealed = True


@bot.hybrid_command()
async def status(ctx):
    r = requests.get(
        "https://store.steampowered.com/app/1030300/Hollow_Knight_Silksong/"
    )
    soup = BeautifulSoup(r.content, "html.parser")
    release_date = soup.find_all("div", {"class": "date"})[0].get_text()
    await ctx.send(f"Current release date: **{release_date}**")


bot.run(str(TOKEN))
