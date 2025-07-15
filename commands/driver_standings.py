from discord.ext import commands
from discord import app_commands, Interaction, Embed
import fastf1
from fastf1.ergast import Ergast

class DriverStandings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="driver_standings", description="View current F1 driver championship standings")
    async def driver_standings(self, interaction: Interaction):
        await interaction.response.defer()  # Show "thinking..." status

        ergast = Ergast()
        standings = ergast.get_driver_standings(season=2025).content  # Automatically gets latest round
        top_10 = standings[:10]

        embed = Embed(
            title="🏆 F1 2025 Driver Standings (Top 10)",
            color=0xFFD700
        )

        for driver in top_10:
            name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
            team = driver['Constructors'][0]['name']
            points = driver['points']
            position = driver['position']
            embed.add_field(
                name=f"{position}. {name}",
                value=f"Team: **{team}**\nPoints: **{points}**",
                inline=False
            )

        embed.set_footer(text="Honeybadger F1 Bot • Data by Ergast API")
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DriverStandings(bot))
