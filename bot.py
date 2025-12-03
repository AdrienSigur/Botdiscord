import discord
import datetime
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

TOKEN = "" #Token de l api discord 
CHANNEL_ID =  # ID du salon où envoyer le message
ROLE_ID= # ID du role ou envoyer le message 

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

now = datetime.datetime.now().strftime("%d/%m/%Y")

scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Paris"))

async def message_matin():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f" **  ☀️ SIGNATURE DU MATIN  ☀️ !!!** <@&{ROLE_ID}>  {now}")



async def message_aprem():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"** 🌕  SIGNATURE CET APREM  🌕  !!! ** <@&{ROLE_ID}> {now}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # --------- CRON LUNDI ---------
    # Lundi 9h30
    scheduler.add_job(message_matin, CronTrigger(day_of_week="mon", hour=9, minute=30))

    # Lundi 13h30
    scheduler.add_job(message_aprem, CronTrigger(day_of_week="mon", hour=13, minute=30))

    # --------- CRON MARDI → VENDREDI ---------
    # Du mardi au vendredi 9h00
    scheduler.add_job(message_matin, CronTrigger(day_of_week="tue-fri", hour=9, minute=0))

    # Du mardi au vendredi 13h00
    scheduler.add_job(message_aprem,  CronTrigger(day_of_week="tue-fri", hour=13, minute=30))

    scheduler.start()


bot.run(TOKEN)