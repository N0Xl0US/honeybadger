import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import discord
import fastf1
import datetime
load_dotenv()
F1_CHANNEL_ID = int(os.environ["F1_CHANNEL_ID"])
F1_YEAR = int(os.environ.get("F1_YEAR", 2025))

class ManualAlert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="manual_alert", description="Send a manual F1 alert for testing")
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def manual_alert(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        try:
            channel = self.bot.get_channel(F1_CHANNEL_ID)
            if not channel:
                await interaction.followup.send("❌ F1 channel not found.")
                return
            
            embed = discord.Embed(
                title="🧪 Manual Test Alert",
                description="This is a test alert to verify the bot is working correctly.",
                color=discord.Color.purple()
            )
            embed.add_field(
                name="Test Information",
                value=f"Time: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\nChannel: {channel.name}",
                inline=False
            )
            embed.set_footer(text="Honeybadger F1 Bot • Manual Test")
            
            await channel.send(embed=embed)
            await interaction.followup.send("✅ Manual alert sent successfully!")
            
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to send manual alert: {e}")

async def setup(bot):
    await bot.add_cog(ManualAlert(bot))