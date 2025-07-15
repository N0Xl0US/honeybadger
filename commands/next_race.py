from discord import app_commands
from discord.ext import commands
import discord
import fastf1
from datetime import datetime

class NextRace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        fastf1.Cache.enable_cache('fastf1_cache')

    @app_commands.command(name="next_race", description="Get info on the next Formula 1 race")
    async def next_race(self, interaction: discord.Interaction):
        now = datetime.utcnow()
        schedule = fastf1.get_event_schedule(2025)

        for _, event in schedule.iterrows():
            event_date = event['EventDate'].to_pydatetime()
            if event_date > now:
                embed = discord.Embed(
                    title=f"Next Race: {event['EventName']}",
                    description=f"📍 {event['Location']}\n🗓️ {event_date.strftime('%A, %d %B %Y')}\n🕒 {event_date.strftime('%H:%M UTC')}",
                    color=discord.Color.green()
                )
                embed.set_footer(text="Honeybadger F1 Bot • FastF1")
                await interaction.response.send_message(embed=embed)
                return

async def setup(bot):
    await bot.add_cog(NextRace(bot))
