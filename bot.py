import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger 
import pytz
from datetime import datetime

TOKEN = "env.file"
CHANNEL_ID = 1414258422379053066 # ID du salon où envoyer le message
ROLE_ID= 1398011699528728776

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Paris"))

# --- Fonctions de signature ---
async def message_matin():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        time_str = datetime.now().strftime("%d/%m/%Y")
        await channel.send(f"**☀️ SIGNATURE DU MATIN ({time_str})☀️ ** <@&{ROLE_ID}>")

async def message_aprem():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        time_str = datetime.now().strftime("%d/%m/%Y")
        await channel.send(f"**🌖 SIGNATURE CET APREM ({time_str})🌖 ** <@&{ROLE_ID}>")

# async def test():
#     channel = bot.get_channel(CHANNEL_ID)
#     if channel:
#         time_str = datetime.now().strftime("%d/%m/%Y")
#         await channel.send(f"test {time_str}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    # --- CRON LUNDI ---
    scheduler.add_job(message_matin, CronTrigger(day_of_week="mon", hour=9, minute=30))
    scheduler.add_job(message_aprem, CronTrigger(day_of_week="mon", hour=13, minute=30))

    # --- CRON MARDI - VENDREDI ---
    scheduler.add_job(message_matin, CronTrigger(day_of_week="tue-fri", hour=9, minute=0))
    scheduler.add_job(message_aprem, CronTrigger(day_of_week="tue-fri", hour=13, minute=30))
    
    # --- JOB DE TEST (DÉSACTIVÉ) ---
    # scheduler.add_job(test, CronTrigger(day_of_week="tue", hour=11, minute=48))
    
    scheduler.start()

bot.run(TOKEN)