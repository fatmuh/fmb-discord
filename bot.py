import discord
import os
import requests
import locale
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)
voice_client = None
load_dotenv()

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

    embed.add_field(name="Command Categories :", value="📅 `libur <bulan>    :` untuk mengetahui tanggal hari libur nasional atau cuti bersama. Contoh: >libur juni\n" + "👑 `pemilu  :` Melihat quick count voting seputar PEMILU\n\nTo view the commands of a category, send `>h`", inline=False)

    embed.set_footer(icon_url=ctx.author.avatar, text="Help requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
# End Help Center #

# Start Hari Libur #
@bot.command()
async def libur(ctx, nama_bulan: str):
    bulan_lower = nama_bulan.lower()
    if bulan_lower in bulan_inggris:
        bulan = bulan_inggris[bulan_lower]
        response = requests.get(os.getenv('API_HARI_LIBUR'))
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
        
# Start Pengecekan Harga Koin #
@bot.command()
async def price(ctx, symbol: str):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    coin = get_coin_from_symbol(symbol)
    if coin:
        price_data = get_coin_price(coin)
        if price_data:
            change_24h = round(price_data['usd_24h_change'], 2)
            embed = discord.Embed(title=f"{coin.capitalize()} Price", color=0x74E291)
            embed.add_field(name="Price (USD)", value=f"`{price_data['usd']}`", inline=False)
            embed.add_field(name="Change (24h)", value=f"`{change_24h}%`", inline=False)
            embed.set_footer(text="Requested by: {}".format(ctx.author.display_name), icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Gagal mendapatkan data harga untuk {coin.upper()}.")
    else:
        await ctx.send(f"Koin dengan simbol {symbol.upper()} tidak ditemukan.")

def get_coin_from_symbol(symbol):
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for coin in data:
            if coin['symbol'] == symbol:
                return coin['id']
    return None

def get_coin_price(coin):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if coin in data:
            return data[coin]
    return None
# End Pengecekan Harga Koin #

bot.run(os.getenv('TOKEN'))