import asyncio
import json
import discord
from discord.ext import commands

with open('../data/config.json') as f:
    sid = json.load(f)['sid']


class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='clear')
    async def clear(self, ctx, amount=1):
        if ctx.message.author.guild_permissions.administrator:
            try:
                amount += 1
                await ctx.channel.purge(limit=amount)
                if amount - 1 == 1:
                    await ctx.send('Deleted 1 message')
                else:
                    await ctx.send(f'Deleted {amount - 1} messages')
            except ValueError:
                await ctx.send(
                    'Invalid command usage!\nCommand syntax: `\\clear {Number of messages to delete(Default = 1)}`')

    @commands.command(name='kick')
    async def kick(self, ctx, mention: discord.Member, *, reason='No reason provided.'):
        if mention.id == sid:
            await ctx.send('no fok u he\'s cool')
        else:
            if (ctx.guild.me.top_role.position > mention.top_role.position
                    and not mention.guild_permissions.administrator and ctx.author.top_role.position > mention.top_role.position):
                message = await ctx.reply('Kick? React with "👍" to confirm, or ignore for 30 seconds to cancel.')
                await message.add_reaction('👍')

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) == '👍'

                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check)
                except asyncio.TimeoutError:
                    await ctx.send(f'Well I guess we\'re not banning {str(mention)}')
                else:
                    await mention.kick(reason=reason)

                    embed = discord.Embed(title="Member kicked",
                                          colour=0xDD2222)

                    embed.set_thumbnail(url=mention.avatar_url)

                    fields = [("Member", f"{mention.display_name}({str(mention)})", False),
                              ("Actioned by", ctx.author.display_name, False),
                              ("Reason", reason, False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    await ctx.send(embed=embed)
            else:
                await ctx.send('no.')

    @commands.command(name='ban')
    async def ban(self, ctx, mention: discord.Member, *, reason='No reason provided.'):
        if mention.id == sid:
            await ctx.send('no fok u he\'s cool')
        else:
            if (ctx.guild.me.top_role.position > mention.top_role.position
                    and not mention.guild_permissions.administrator and ctx.author.top_role.position > mention.top_role.position):
                message = await ctx.reply('Ban? React with "👍" to confirm, or ignore for 30 seconds to cancel.')
                await message.add_reaction('👍')

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) == '👍'

                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check)
                except asyncio.TimeoutError:
                    await ctx.send(f'Well I guess we\'re not banning {str(mention)}')
                else:
                    await mention.ban(reason=reason)

                    embed = discord.Embed(title="Member banned",
                                          colour=0xDD2222)

                    embed.set_thumbnail(url=mention.avatar_url)

                    fields = [("Member", f"{mention.display_name}({str(mention)})", False),
                              ("Actioned by", ctx.author.display_name, False),
                              ("Reason", reason, False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    await ctx.send(embed=embed)
            else:
                await ctx.send('no.')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Incorrect command usage!\nCommand syntax: `\\ban {Member} {Reason(Optional)}`')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send('That person\'s not in your server what do you mean')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('just ping a person how did you mess this up')
        else:
            await ctx.send(f'Something went wrong and I don\'t know why.\nError: {error}')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Incorrect command usage!\nCommand syntax: `\\kick {Member} {Reason(Optional)}`')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send('That person\'s not in your server what do you mean')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('just ping a person how did you mess this up')
        else:
            await ctx.send(f'Something went wrong and I don\'t know why.\nError: {error}')


def setup(client):
    client.add_cog(Mod(client))
