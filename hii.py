import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
WATCHED_USER_IDS = [1032678253627981906, 1032678253627981906]  
ALERT_CHANNEL_ID = 1358749924178788414  
BOT_TOKEN = "MTM2NzU5MDg4ODg2NzUwMDA3Mg.G8ieUW.3oW2BVNDvWHt5T8VMyp0EeZNXBf5WJefsA_l-4"  # 🔴 REPLACE WITH YOUR TOKEN!

# --- KEEP-ALIVE (FOR REPLIT/FREE HOSTING) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_webserver():
    app.run(host='0.0.0.0', port=8080)

# --- BOT SETUP ---
intents = discord.Intents.default()
intents.members = True  # Required for tracking joins

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user} (ID: {bot.user.id})")
    print("Watching for users:", WATCHED_USER_IDS)

@bot.event
async def on_member_join(member):
    if member.id in WATCHED_USER_IDS:
        channel = bot.get_channel(ALERT_CHANNEL_ID)
        if channel:
            await channel.send(
                f"{member.mention} (ID: `{member.id}`) joined!\n"
                "**This user was flagged for suspicious activity!** @Staff"
            )

# --- ERROR HANDLING ---
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error in {event}: {args} {kwargs}")

# --- START BOT ---
if __name__ == "__main__":
    # Start Flask webserver in a thread (for Replit/Uptime)
    Thread(target=run_webserver).start()
    
    # Run the bot (with reconnect logic)
    while True:
        try:
            bot.run(BOT_TOKEN)
        except Exception as e:
            print(f"Bot crashed: {e}. Restarting in 5 sec...")
            time.sleep(5)
