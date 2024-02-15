import discord
import os
import requests
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)
api_url = "https://raw.githubusercontent.com/guangrei/APIHariLibur_V2/main/calendar.min.json"

# Bulan Inggris Declare #
bulan_inggris = {
    "januari": 1,
    "februari": 2,
    "maret": 3,
    "april": 4,
    "mei": 5,
    "juni": 6,
    "juli": 7,
    "agustus": 8,
    "september": 9,
    "oktober": 10,
    "november": 11,
    "desember": 12
}

# Start Help Center #
@bot.command()
async def h(ctx):
    embed = discord.Embed(title="FMB Help Center ✨", color=0xF49726)

    # embed.add_field(name="Command Categories :", value="📅 `libur <bulan>    :` untuk mengetahui tanggal hari libur nasional atau cuti bersama.\n" + "🔧 `utility  :` Bot utility zone\n😏 `nsfw     :` Image generation with a memey twist.\n\nTo view the commands of a category, send `.help <category>`", inline=False)

    embed.add_field(name="Command Categories :", value="📅 `libur <nama_bulan>    :` untuk mengetahui tanggal hari libur nasional atau cuti bersama. Contoh: .libur juni\n" + "\n\nTo view the commands of a category, send `.h <category>`", inline=False)
    embed.set_footer(icon_url=ctx.author.avatar, text="Help requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
# End Help Center #

# Start Hari Libur #
@bot.command()
async def libur(ctx, nama_bulan: str):
    bulan_lower = nama_bulan.lower()
    if bulan_lower in bulan_inggris:
        bulan = bulan_inggris[bulan_lower]
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            response_msg = f"***Hari Libur Pada Bulan {nama_bulan.capitalize()} {datetime.now().year}:*** \n"
            current_length = len(response_msg)
            for date, holiday_info in data.items():
                date_parts = date.split('-')
                if len(date_parts) == 3 and int(date_parts[1]) == bulan:
                    description = holiday_info.get("description", [""])
                    if holiday_info.get("holiday", False):
                        # Mengonversi tanggal ke format "DD Bulan YYYY" dengan nama bulan dalam bahasa Indonesia
                        formatted_date = f"{date_parts[2]} {nama_bulan.capitalize()} {date_parts[0]}"
                        holiday_summary = ', '.join(holiday_info.get('summary', ['']))
                        holiday_str = f"\nTanggal {formatted_date}: {holiday_summary}"
                        if current_length + len(holiday_str) > 2000:
                            await ctx.send(response_msg)
                            response_msg = ""
                            current_length = 0
                        response_msg += holiday_str
                        current_length += len(holiday_str)
            if response_msg:
                await ctx.send(response_msg)
        else:
            await ctx.send("Gagal mengambil data hari libur.")
    else:
        await ctx.send("Bulan tidak valid. Silakan masukkan nama bulan dalam bahasa Indonesia.")
# End Hari Libur #

load_dotenv()
bot.run(os.getenv('TOKEN'))