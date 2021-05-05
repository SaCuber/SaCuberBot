import discord
from discord.ext import commands


class User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='profile', hidden=False, aliases=['pf', 'user', 'userinfo', 'user_info'])
    async def profile(self, ctx, mention: discord.Member = 'self'):
        if mention == 'self':
            mention = ctx.author
        pfp = mention.avatar_url
        embed = discord.Embed(
            title=f'{mention.name}\'s Profile',
            description=str(mention),
            colour=mention.colour
        )

        activity_types = {
            discord.ActivityType.unknown: 'Unkown btw how did you manage to do this:',
            discord.ActivityType.playing: 'Playing',
            discord.ActivityType.streaming: 'Streaming',
            discord.ActivityType.listening: 'Listening',
            discord.ActivityType.watching: 'Watching',
            discord.ActivityType.custom: '',
            discord.ActivityType.competing: 'Competing btw what even is this'
        }

        try:
            activity_type = activity_types[mention.activity.type]
        except AttributeError:
            activity_type = ''

        embed.set_footer(text='SaCuber Bot')
        embed.set_thumbnail(url=pfp)
        embed.add_field(name='User ID:', value=str(mention.id), inline=False)
        embed.add_field(name='Status:', value=str(mention.status).capitalize(), inline=False)
        embed.add_field(name='Activity:', value=f'{activity_type} {mention.activity}', inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='avatar', hidden=False, aliases=['pfp'])
    async def avatar(self, ctx, mention: discord.Member = "self"):
        if not mention == "self":
            pfp = str(mention.avatar_url).replace("webp", "png")
            embed = discord.Embed(
                title=f'{mention.display_name}\'s profile picture',
                description=f"Click [here]({pfp}) if you want to download it!",
                colour=discord.Colour.random()
            )
            embed.set_image(url=pfp)
            await ctx.send(embed=embed)
        else:
            pfp = str(ctx.author.avatar_url).replace("webp", "png")
            embed = discord.Embed(
                title='Your pfp',
                description=f"Click [here]({pfp}) if you want to download it!",
                colour=discord.Colour.random()
            )
            embed.set_image(url=pfp)
            await ctx.send(embed=embed)

    @commands.command(name='id', hidden=False, aliases=['userid'])
    async def id(self, ctx, tag: discord.Member = 'self'):
        if not tag == 'self':
            await ctx.send(f'{tag.mention}\'s discord id is `{str(tag.id)}`')
        else:
            await ctx.send(f'Your discord id is `{str(ctx.message.author.id)}`')

    @commands.command(name='serverinfo', aliases=['si', 'server', 'server_info'])
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            title=f'**{ctx.guild.name}**',
            description=ctx.guild.description,
            colour=discord.Colour.random()
        )

        embed.set_footer(text='SaCuber Bot')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name=f':computer: **ID**', value=f'{ctx.guild.id}', inline=True)
        embed.add_field(name=f':crown: **Owner**', value=f'`{str(ctx.guild.owner)}`\n({str(ctx.guild.owner_id)})',
                        inline=True)
        embed.add_field(name=f':earth_africa: **Region**', value=ctx.guild.region, inline=True)
        embed.add_field(name=f':speech_balloon: **Channels ({str(len(ctx.guild.channels))})**',
                        value=f':pencil: **Text:** {str(len(ctx.guild.text_channels))}\n:speaking_head: **Voice:** {str(len(ctx.guild.voice_channels))}',
                        inline=False)
        embed.add_field(name=f':busts_in_silhouette: **Members**', value=f'**{str(len(ctx.guild.members))}**',
                        inline=True)

        await ctx.send(embed=embed)

    @id.error
    async def id_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send('I couldn\'t find that person')


def setup(client):
    client.add_cog(User(client))
