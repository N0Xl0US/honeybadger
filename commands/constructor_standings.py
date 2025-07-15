from discord.ext import commands
from discord import app_commands, Interaction, Embed
import fastf1
from fastf1.ergast import Ergast

class ConstructorStandings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="constructor_standings", description="View current F1 constructors championship standings")
    async def constructor_standings(self, interaction: Interaction):
        await interaction.response.defer()  # Shows "thinking..." status

        ergast = Ergast()
        standings = ergast.get_constructor_standings(season=2025).content
        top_10 = standings[:10]

        embed = Embed(
            title="🔧 F1 2025 Constructor Standings (Top 10)",
            color=0x3498DB
        )

        for team in top_10:
            name = team['Constructor']['name']
            points = team['points']
            position = team['position']
            embed.add_field(
                name=f"{position}. {name}",
                value=f"Points: **{points}**",
                inline=False
            )

        embed.set_footer(text="Honeybadger F1 Bot • Data by Ergast API")
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ConstructorStandings(bot))
