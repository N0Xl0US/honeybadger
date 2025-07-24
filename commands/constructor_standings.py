import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands, Interaction, Embed
import fastf1
from fastf1.ergast import Ergast
load_dotenv()
F1_YEAR = int(os.environ.get("F1_YEAR", 2025))

class ConstructorStandings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="constructor_standings", description="View current F1 constructors championship standings")
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def constructor_standings(self, interaction: Interaction):
        await interaction.response.defer()  # Shows "thinking..." status
        try:
            ergast = Ergast()
            standings = ergast.get_constructor_standings(season=F1_YEAR).content
            embed = Embed(
                title=f"🔧 F1 {F1_YEAR} Constructor Standings (Top 10)",
                color=0x3498DB
            )
            rows = []
            if isinstance(standings, list) and len(standings) > 0:
                df = standings[0]
                if hasattr(df, "itertuples"):
                    rows = list(df.itertuples(index=False))[:10]
            for row in rows:
                name = getattr(row, 'constructorName', 'Unknown')
                points = getattr(row, 'points', '?')
                position = getattr(row, 'position', '?')
                field_name = f"{position}. {name}"
                if len(field_name) > 256:
                    field_name = field_name[:253] + '...'
                embed.add_field(
                    name=field_name,
                    value=f"Points: **{points}**",
                    inline=False
                )
            embed.set_footer(text="Honeybadger F1 Bot • Data by Ergast API")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"Error fetching constructor standings: {e}")

async def setup(bot):
    await bot.add_cog(ConstructorStandings(bot))
