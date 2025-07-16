from discord.ext import commands, tasks
import discord
import fastf1
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
F1_CHANNEL_ID = int(os.environ["F1_CHANNEL_ID"])
F1_YEAR = int(os.environ.get("F1_YEAR", 2025))

class F1Alerts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session_alerts_sent = set()
        self.eight_hour_alerts_sent = set()
        self.session_results_sent = set()
        try:
            self.schedule = fastf1.get_event_schedule(F1_YEAR)
        except Exception as e:
            print(f"Failed to get event schedule: {e}")
            self.schedule = []
        self.check_sessions.start()

    def get_upcoming_sessions(self):
        today = datetime.datetime.utcnow().date()
        sessions = []
        for _, event in getattr(self.schedule, 'iterrows', lambda:[])():
            if event['EventDate'].date() >= today:
                for session_type in ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Sprint', 'Race']:
                    try:
                        session = fastf1.get_event(F1_YEAR, event['RoundNumber']).get_session(session_type)
                        session_time = session.session_start_time
                        end_time = session.session_end_time
                        sessions.append((session_type, event['EventName'], session_time, end_time, event['RoundNumber']))
                    except Exception as e:
                        print(f"Failed to get session {session_type} for event {event['EventName']}: {e}")
                        continue
        return sessions

    @tasks.loop(minutes=10)
    async def check_sessions(self):
        channel = self.bot.get_channel(F1_CHANNEL_ID)
        if not channel:
            print("⚠️ F1 channel not found.")
            return
        now = datetime.datetime.utcnow()
        try:
            sessions = self.get_upcoming_sessions()
        except Exception as e:
            print(f"Failed to get upcoming sessions: {e}")
            return
        for session_type, event_name, start_time, end_time, round_number in sessions:
            key = (session_type, event_name)
            # 🔔 8 Hours Before Alert
            minutes_until_start = (start_time - now).total_seconds() / 60
            if 470 <= minutes_until_start <= 490:
                if key not in self.eight_hour_alerts_sent:
                    try:
                        embed = discord.Embed(
                            title=f"⏰ {session_type} in 8 Hours",
                            description=f"**{event_name}** {session_type} starts at {start_time.strftime('%H:%M UTC')}",
                            color=discord.Color.gold()
                        )
                        embed.set_footer(text="Honeybadger F1 Bot • FastF1")
                        await channel.send(embed=embed)
                        self.eight_hour_alerts_sent.add(key)
                    except Exception as e:
                        print(f"Failed to send 8 hour alert: {e}")
            # 🕐 15 Min Before Alert
            if 0 <= minutes_until_start <= 15:
                if key not in self.session_alerts_sent:
                    try:
                        embed = discord.Embed(
                            title=f"🏁 {session_type} Starting Soon!",
                            description=f"{event_name} {session_type} starts at **{start_time.strftime('%H:%M UTC')}**",
                            color=discord.Color.red()
                        )
                        embed.set_footer(text="Honeybadger F1 Bot • FastF1")
                        await channel.send(embed=embed)
                        self.session_alerts_sent.add(key)
                    except Exception as e:
                        print(f"Failed to send 15 min alert: {e}")
            # ✅ Session Results (After End)
            minutes_after_end = (now - end_time).total_seconds() / 60
            if 0 <= minutes_after_end <= 30:
                if key not in self.session_results_sent:
                    try:
                        session = fastf1.get_session(F1_YEAR, round_number, session_type)
                        session.load()
                        results = session.results
                        if results is not None:
                            embed = discord.Embed(
                                title=f"📊 {session_type} Results - {event_name}",
                                color=discord.Color.green()
                            )
                            for i, row in results.head(10).iterrows():
                                pos = int(row['Position'])
                                driver = row['FullName']
                                team = row['TeamName']
                                embed.add_field(
                                    name=f"{pos}. {driver}",
                                    value=f"🏎️ {team}",
                                    inline=False
                                )
                            embed.set_footer(text="Honeybadger F1 Bot • Powered by FastF1")
                            await channel.send(embed=embed)
                            self.session_results_sent.add(key)
                    except Exception as e:
                        print(f"⚠️ Failed to fetch results for {key}: {e}")
    @check_sessions.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(F1Alerts(bot))
