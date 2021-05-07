import os
import json
import mcuuid
import discord
import requests
from discord.ext import commands

with open('../data/config.json') as f:
    temp_path = json.load(f)['temp_path']


class Minecraft(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='mcavatar', aliases=['mca', 'mc_avatar', 'minecraftavatar', 'minecraft_avatar'])
    async def mcavatar(self, ctx, person):
        try:
            uuid = mcuuid.MCUUID(person).uuid
        except ValueError:
            await ctx.send('Ayo there\'s no one with that name what do you mean')
        else:
            r = requests.get(f'https://crafatar.com/avatars/{str(uuid)}?overlay')
            with open(f'{temp_path}\\{str(uuid)}_avatar.png', 'wb') as outfile:
                outfile.write(r.content)
            await ctx.send(file=discord.File(f'{temp_path}\\{str(uuid)}_avatar.png'))
            os.remove(f'{temp_path}\\{str(uuid)}_avatar.png')

    @commands.command(name='mchead', aliases=['mch', 'mc_head', 'minecrafthead', 'minecraft_head'])
    async def mchead(self, ctx, person):
        try:
            uuid = mcuuid.MCUUID(person).uuid
        except ValueError:
            await ctx.send('Ayo there\'s no one with that name what do you mean')
        else:
            r = requests.get(f'https://crafatar.com/renders/head/{str(uuid)}?overlay')
            with open(f'{temp_path}\\{str(uuid)}_head.png', 'wb') as outfile:
                outfile.write(r.content)
            await ctx.send(file=discord.File(f'{temp_path}\\{str(uuid)}_head.png'))
            os.remove(f'{temp_path}\\{str(uuid)}_head.png')

    @commands.command(name='mcbody', aliases=['mcb', 'mc_body', 'minecraftbody', 'minecraft_body'])
    async def mcbody(self, ctx, person):
        try:
            uuid = mcuuid.MCUUID(person).uuid
        except ValueError:
            await ctx.send('Ayo there\'s no one with that name what do you mean')
        else:
            r = requests.get(f'https://crafatar.com/renders/body/{str(uuid)}?overlay')
            with open(f'{temp_path}\\{str(uuid)}_body.png', 'wb') as outfile:
                outfile.write(r.content)
            await ctx.send(file=discord.File(f'{temp_path}\\{str(uuid)}_body.png'))
            os.remove(f'{temp_path}\\{str(uuid)}_body.png')

    @commands.command(name='mcskin', aliases=['mcs', 'mc_skin', 'minecraftskin', 'minecraft_skin'])
    async def mcskin(self, ctx, person):
        try:
            uuid = mcuuid.MCUUID(person).uuid
        except ValueError:
            await ctx.send('Ayo there\'s no one with that name what do you mean')
        else:
            r = requests.get(f'https://crafatar.com/skins/{str(uuid)}')
            with open(f'{temp_path}\\{str(uuid)}_skin.png', 'wb') as outfile:
                outfile.write(r.content)
            await ctx.send(file=discord.File(f'{temp_path}\\{str(uuid)}_skin.png'))
            os.remove(f'{temp_path}\\{str(uuid)}_skin.png')

    @commands.command(name='mcuuid', aliases=['mcu', 'mc_uuid', 'minecraftuuid', 'minecraft_uuid'])
    async def mcuuid(self, ctx, person):
        try:
            await ctx.send(mcuuid.MCUUID(person).uuid)
        except ValueError:
            await ctx.send('Ayo there\'s no one with that name what do you mean')

    @mcavatar.error
    async def mcavatar_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Ayo where person huh')
        else:
            await ctx.send(f'Something just went wrong but idk why nor how.\nError: {error}')

    @mcuuid.error
    async def mcuuid_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Ayo where person huh')
        else:
            await ctx.send(f'Something just went wrong but idk why nor how.\nError: {error}')

    @mchead.error
    async def mchead_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Ayo where person huh')
        else:
            await ctx.send(f'Something just went wrong but idk why nor how.\nError: {error}')

    @mcbody.error
    async def mcbody_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Ayo where person huh')
        else:
            await ctx.send(f'Something just went wrong but idk why nor how.\nError: {error}')

    @mcskin.error
    async def mcskin_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Ayo where person huh')
        else:
            await ctx.send(f'Something just went wrong but idk why nor how.\nError: {error}')


def setup(client):
    client.add_cog(Minecraft(client))
