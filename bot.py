import discord
from discord.ext import commands
import os
import fastf1
from dotenv import load_dotenv
from keep_alive import keep_alive
import asyncio
import signal
import sys

fastf1.Cache.enable_cache('fastf1_data')

load_dotenv()
TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

class HoneybadgerBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir("./commands"):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    await self.load_extension(f"commands.{filename[:-3]}")
                    print(f"✅ Loaded command: {filename}")
                except Exception as e:
                    print(f"❌ Failed to load command {filename}: {e}")

        for filename in os.listdir("./tasks"):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    await self.load_extension(f"tasks.{filename[:-3]}")
                    print(f"✅ Loaded task: {filename}")
                except Exception as e:
                    print(f"❌ Failed to load task {filename}: {e}")

    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")
        try:
            synced = await self.tree.sync()
            print(f"🔧 Synced {len(synced)} slash commands")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")

bot = HoneybadgerBot()

async def main():
    keep_alive() 
    try:
        await bot.start(TOKEN)
    except discord.HTTPException as e:
        if e.status == 429:
            print("⚠️ Rate limited. Sleeping for 15 minutes...")
            await asyncio.sleep(900)
        raise e


def shutdown():
    print("⛔ Bot manually stopped.")
    try:
        asyncio.get_event_loop().stop()
    except:
        pass
    sys.exit(0)


if __name__ == "__main__":
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: shutdown())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        shutdown()
