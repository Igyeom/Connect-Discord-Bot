import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
threads = []
streaks = []

with open("words.txt", "r") as f:
    words = f.read().splitlines()

bot = commands.Bot(command_prefix='c!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    global threads
    global streaks


    if message.author == bot.user:
        return
    if message.content.startswith('c!'):
        await bot.process_commands(message)
    else:
        if message.channel in threads:
            if message.content in words and message.content not in streaks[threads.index(message.channel)]:
                if len(streaks[threads.index(message.channel)]) == 0:
                    streaks[threads.index(message.channel)].append(message.content)
                    await message.channel.send("Streak: **" + str(len(streaks[threads.index(message.channel)])) + "**")
                elif message.content[:2] == streaks[threads.index(message.channel)][-1][-2:]:
                    streaks[threads.index(message.channel)].append(message.content)
                    await message.channel.send("Streak: **" + str(len(streaks[threads.index(message.channel)])) + f"**\nPrevious word: **{streaks[threads.index(message.channel)][-1]}**")
                else:
                    print(message.content[:2], streaks[threads.index(message.channel)][-1][-2:])
                    await message.channel.send("Streak: **" + str(len(streaks[threads.index(message.channel)])) + f"**\nPrevious word: **{streaks[threads.index(message.channel)][-1]}**\n_The word must start with the last two letters of the previous word. Try again._")
            else:
                if len(streaks[threads.index(message.channel)]) == 0:
                    await message.channel.send("Streak: **" + str(len(streaks[threads.index(message.channel)])) + "**\n_You must state a valid word that you haven't used yet. Try again._")
                else:
                    await message.channel.send("Streak: **" + str(len(streaks[threads.index(message.channel)])) + f"**\nPrevious word: **{streaks[threads.index(message.channel)][-1]}**\n_You must state a valid word that you haven't used yet. Try again._")

@bot.command()
async def streak(ctx):
    global threads
    global streaks


    threads.append(await ctx.channel.create_thread(name=ctx.message.author.name + "'s streak #" + str(random.randint(10000, 99999)), auto_archive_duration=1440))
    streaks.append([])
    await threads[-1].send('State your first word here to start the game. ' + ctx.message.author.mention)
    await ctx.send('Your streak starts now. Good luck!')


@bot.command()
async def quit(ctx):
    global threads
    global streaks


    if ctx.channel in threads:
        await threads[threads.index(ctx.channel)].delete()
        threads.remove(ctx.channel)
        streaks.pop(threads.index(ctx.channel))
    else:
        await ctx.send('You are not in a streak game.')

bot.run('TOKEN')
