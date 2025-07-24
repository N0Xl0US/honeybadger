import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import discord
import fastf1
from datetime import datetime
load_dotenv()
F1_YEAR = int(os.environ.get("F1_YEAR", 2025))

class NextRace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="next_race", description="Get info on the next Formula 1 race")
    async def next_race(self, interaction: discord.Interaction):
        try:
            now = datetime.utcnow()
            schedule = fastf1.get_event_schedule(F1_YEAR)
            for _, event in schedule.iterrows():
                event_date = event['EventDate'].to_pydatetime()
                if event_date > now:
                    # Get the actual race session start time
                    try:
                        race_event = fastf1.get_event(F1_YEAR, event['RoundNumber'])
                        race_session = race_event.get_session('Race')
                        race_start_time = race_session.session_start_time
                    except Exception as e:
                        race_start_time = event_date  # fallback
                    embed = discord.Embed(
                        title=f"Next Race: {event['EventName']}",
                        description=f"\U0001F4CD {event['Location']}\n\U0001F4C5 {race_start_time.strftime('%A, %d %B %Y')}\n\U0001F552 {race_start_time.strftime('%H:%M UTC')}",
                        color=discord.Color.green()
                    )
                    embed.set_footer(text="Honeybadger F1 Bot • FastF1")
                    await interaction.response.send_message(embed=embed)
                    return
            await interaction.response.send_message("No upcoming races found.")
        except Exception as e:
            await interaction.response.send_message(f"Error fetching next race: {e}")

async def setup(bot):
    await bot.add_cog(NextRace(bot))
