import discord
import youtube_dl
from discord.ext import commands

TOKEN = ""

bot = commands.Bot(command_prefix = '?', help_command = None)
playlist = {}

helpCommand = ("""
I'm here to help! Use the prefix '?'
```
Useless:
    echo "[text]"    - I can copy what you say!
    hello            - hi!

Music:
    join             - I'll join if you're lonely!
    leave            - I guess I'll leave ...
```
""")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('-> Use "?BMO"'))

@bot.command()
async def echo(ctx, string):
    userId = ctx.author

    await ctx.send(f"""
{userId.mention} said:
```
{string}
```
""")

@bot.command(aliases = ['hi', 'hey'])
async def hello(ctx):
    userId = ctx.author
    await ctx.send(f'Hello {userId.mention}, I am BMO!')

@bot.command(aliases=["help, bmo"])
async def BMO(ctx):
    await ctx.send(helpCommand)

@bot.command()
async def join(ctx):
    if ctx.author.voice == None:
        await ctx.send("I'm lost! Connect to a voice channel so I can find you!")
    else:
        await ctx.author.voice.channel.connect()
        await ctx.send("I found you!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client == None:
        await ctx.send("I'm not in a voice channel!")
    else:
        await ctx.voice_client.disconnect()
        await ctx.send("Byebye!")

@bot.command(pass_context = True)
async def play(ctx, url):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio'}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download = False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
        vc.play(source)
        await ctx.send(f"Playing ... {url}")


bot.run(TOKEN)