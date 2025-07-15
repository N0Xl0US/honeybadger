from discord.ext import commands
from discord import app_commands, Interaction, Embed
import fastf1
from fastf1.ergast import Ergast
from datetime import datetime

class LastRace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="last_race", description="View results of the most recent Formula 1 race")
    async def last_race(self, interaction: Interaction):
        await interaction.response.defer()

        ergast = Ergast()
        races = ergast.get_race_results(season=2025).content

        if not races:
            await interaction.followup.send("No race results available for 2025 yet.")
            return

        last_race = races[-1]
        race_name = last_race['raceName']
        date_str = last_race['date']
        date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")

        embed = Embed(
            title=f"🏁 {race_name} Results ({date})",
            description="Top 5 finishers:",
            color=0xE74C3C
        )

        for result in last_race['Results'][:5]:
            position = result['position']
            driver = result['Driver']
            name = f"{driver['givenName']} {driver['familyName']}"
            constructor = result['Constructor']['name']
            time_info = result.get('Time', {}).get('time', '—')

            embed.add_field(
                name=f"{position}. {name}",
                value=f"🏎️ {constructor}\n⏱️ {time_info}",
                inline=False
            )

        embed.set_footer(text="Honeybadger F1 Bot • Dat_
