import json
import discord
from discord.ext import commands

with open('../data/config.json') as f:
    sid = json.load(f)['sid']


class Dev(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='status', hidden=True)
    async def status(self, ctx, setclear, stat_type='im', *, text='very cool'):
        if ctx.author.id == sid:
            if setclear.lower() == 'set':
                if stat_type == "playing":
                    await self.client.change_presence(activity=discord.Game(name=text))
                    await ctx.send(f"Status changed to: Playing {text}")
                elif stat_type == "listening":
                    await self.client.change_presence(
                        activity=discord.Activity(type=discord.ActivityType.listening, name=text))
                    await ctx.send(f"Status changed to: Listening to {text}")
                elif stat_type == "watching":
                    await self.client.change_presence(
                        activity=discord.Activity(type=discord.ActivityType.watching, name=text))
                    await ctx.send(f"Status changed to: Watching {text}")
                else:
                    await ctx.send("An error occurred. Check if you entered a valid status type (playing, listening, "
                                   "watching) and if the content is also valid.")
            elif setclear.lower() == 'clear':
                await self.client.change_presence(activity=None)
                await ctx.send("Status cleared")
        else:
            await ctx.send("You do not have permission to perform that command")

    @commands.command(name='off', hidden=True)
    async def off(self, ctx):
        if ctx.author.id == sid:
            await ctx.send('Turning off...')
            exit()

    @commands.command(name='botserver')
    async def botserver(self, ctx, list_leave, index=None):
        if ctx.author.id == sid:
            guilds = []
            guildids = []
            for server in self.client.guilds:
                guilds.append(server.name)
                guildids.append(server.id)
            if list_leave == "list":
                try:
                    await ctx.send(f"{str(len(self.client.guilds))}\n{', '.join(guilds)}")
                except commands.CommandInvokeError:
                    await ctx.send(f'{str(len(self.client.guilds))}\nList is too long to send by message.')
            elif list_leave == "leave":
                if index is None:
                    await ctx.send('Where index huh')
                else:
                    try:
                        toleave = self.client.get_guild(guildids[(int(index) - 1)])
                    except IndexError:
                        await ctx.send('That\'s not a valid index though')
                    else:
                        try:
                            try:
                                await toleave.channels[0].send('I\'m leaving this server, so adios')
                            except Exception:
                                return
                            await toleave.leave()
                            try:
                                await ctx.send(f'Just left server named "{toleave.name}". Feeling Good!')
                            except Exception:
                                return
                        except Exception as error:
                            await ctx.send(f'Something went wrong.\nError: {str(error)}')
        else:
            return

    @botserver.error
    async def server_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing list/leave')
        else:
            await ctx.send(f'Something\'s went wrong and I don\'t know why. Error: {error}')


def setup(client):
    client.add_cog(Dev(client))
