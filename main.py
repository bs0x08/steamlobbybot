import discord
from discord.ext import commands
from aiohttp import web
import asyncio

# ===============================
# setting / cfg
# ===============================
DISCORD_TOKEN = "MTQxMzk0MjI4ODgxOTk0OTczOQ.GAr5_H.wbmk3lD7u80GcKgYNDIohjKxduSuGg3MFGh1XE"
LOG_CHANNEL_ID = 1240615487646203924

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# ===============================
# gmod sup sup sap
# ===============================
async def handle_gmod_log(request):
    try:
        data = await request.post()
        admin = data.get("admin", "UNKNOWN")
        target = data.get("target", "UNKNOWN")
        action = data.get("action", "UNKNOWN")
        time = data.get("time", "N/A")
        reason = data.get("reason", "N/A")

        embed = discord.Embed(title="🛡 Админ-действие", color=0xff0000)
        embed.add_field(name="Администратор", value=admin, inline=False)
        embed.add_field(name="Игрок", value=target, inline=False)
        embed.add_field(name="Действие", value=action, inline=False)
        embed.add_field(name="Время", value=str(time), inline=False)
        embed.add_field(name="Причина", value=reason, inline=False)

        channel = bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)
        return web.Response(text="OK")

    except Exception as e:
        return web.Response(text=f"Error: {e}")


async def start_webserver():
    app = web.Application()
    app.router.add_post("/log", handle_gmod_log)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 5000)  # port5000
    await site.start()

# ===============================
# start
# ===============================
@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")
    asyncio.create_task(start_webserver())

bot.run(DISCORD_TOKEN)
