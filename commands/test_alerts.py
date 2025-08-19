import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import discord
import fastf1
import datetime
load_dotenv()
F1_YEAR = int(os.environ.get("F1_YEAR", 2025))

class TestAlerts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test_alerts", description="Test F1 alerts functionality")
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
    async def test_alerts(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        try:
            schedule = fastf1.get_event_schedule(F1_YEAR)
            embed = discord.Embed(
                title="🔧 F1 Alerts Test Results",
                color=discord.Color.blue()
            )
            
            today = datetime.datetime.utcnow().date()
            upcoming_sessions = []
            
            for _, event in schedule.iterrows():
                if event['EventDate'].date() >= today:
                    event_obj = fastf1.get_event(F1_YEAR, event['RoundNumber'])
                    session_types = ['FP1', 'FP2', 'FP3', 'Q', 'S', 'R']
                    session_names = ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Sprint', 'Race']
                    
                    for session_type, session_name in zip(session_types, session_names):
                        try:
                            session = event_obj.get_session(session_type)
                            start_time = session.session_start_time
                            end_time = session.session_end_time
                            upcoming_sessions.append({
                                'name': session_name,
                                'event': event['EventName'],
                                'start': start_time,
                                'end': end_time,
                                'minutes_until': (start_time - datetime.datetime.utcnow()).total_seconds() / 60
                            })
                        except Exception as e:
                            continue
            
            if upcoming_sessions:
                embed.add_field(
                    name="📅 Upcoming Sessions",
                    value=f"Found {len(upcoming_sessions)} sessions",
                    inline=False
                )
                
                for i, session in enumerate(upcoming_sessions[:3]):
                    embed.add_field(
                        name=f"{i+1}. {session['name']} - {session['event']}",
                        value=f"Starts: {session['start'].strftime('%Y-%m-%d %H:%M UTC')}\nMinutes until: {session['minutes_until']:.1f}",
                        inline=False
                    )
            else:
                embed.add_field(
                    name="❌ No Sessions Found",
                    value="No upcoming sessions found",
                    inline=False
                )
            
            embed.add_field(
                name="🕐 Current Time",
                value=f"UTC: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
                inline=False
            )
            
            embed.set_footer(text="Honeybadger F1 Bot • Test Command")
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            await interaction.followup.send(f"❌ Test failed: {e}")

async def setup(bot):
    await bot.add_cog(TestAlerts(bot))