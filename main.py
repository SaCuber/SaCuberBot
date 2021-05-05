import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix='\\', case_insensitive=True, intents=intents)


@client.event
async def on_ready():
    print('Bot is logged in as {0.user}, id {0.user.id}'.format(client))


@client.command(name='ping', hidden=False)
async def ping(ctx):
    await ctx.message.channel.send(
        f'Pong mother trucker I am {(round(client.latency * 1000))}ms behind the world but I DONT CARE')


@client.command(name='load', hidden=True)
async def load(ctx, extension):
    if ctx.message.author.id == (my_id):
        if extension == 'all':
            for file in os.listdir('./cogs'):
                if file == '__pycache__':
                    pass
                else:
                    file = file.replace('.py', '')
                    client.load_extension(f'cogs.{file}')
                    print('All cogs loaded successfully')
            await ctx.message.channel.send('All cogs loaded successfully')
        else:
            extension_low = extension.lower()
            client.load_extension(f'cogs.{extension_low}')
            print(f'{extension} was loaded successfully')
            await ctx.message.channel.send(f'{extension} was loaded successfully')


@client.command(name='unload', hidden=True)
async def unload(ctx, extension):
    if ctx.message.author.id == (my_id):
        if extension == 'all':
            for file in os.listdir('./cogs'):
                if file == '__pycache__':
                    pass
                else:
                    file = file.replace('.py', '')
                    client.unload_extension(f'cogs.{file}')
                    print('All cogs unloaded successfully')
            await ctx.message.channel.send('All cogs unloaded successfully')
        else:
            extension_low = extension.lower()
            client.unload_extension(f'cogs.{extension_low}')
            print(f'{extension} was unloaded successfully')
            await ctx.message.channel.send(f'{extension} was unloaded successfully')


@client.command(name='reload', hidden=True)
async def reload(ctx, extension):
    if ctx.message.author.id == (my_id):
        if extension == 'all':
            for file in os.listdir('./cogs'):
                if file == '__pycache__':
                    return
                else:
                    file = file.replace('.py', '')
                    client.unload_extension(f'cogs.{file}')
                    client.load_extension(f'cogs.{file}')
                    print('All cogs reloaded successfully')
            await ctx.message.channel.send('All cogs reloaded successfully')
        else:
            extension_low = extension.lower()
            client.unload_extension(f'cogs.{extension_low}')
            client.load_extension(f'cogs.{extension_low}')
            print(f'{extension} was reloaded successfully')
            await ctx.message.channel.send(f'{extension} was reloaded successfully')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(MyTokenWhyAreYouEvenLookingAtThisYouBastard)
