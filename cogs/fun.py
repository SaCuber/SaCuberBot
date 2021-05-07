import discord
import random
import requests
import praw
import asyncio
import json
import prawcore
import contextlib
import io
from random import choice
from math import *
from pokedex import pokedex
from prawcore import NotFound
from discord.ext import commands

with open('../data/config.json') as f:
    reddit_client = json.load(f)['reddit_client']
    reddit_secret = json.load(f)['reddit_secret']
    reddit_ua = json.load(f)['reddit_ua']
    data_path = json.load(f)['data_path']

pokedex = pokedex.Pokedex()

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def reddit(self, ctx, *, subreddit='homepage'):

        global submission
        reddit = praw.Reddit(client_id=reddit_client,
                             client_secret=reddit_secret,
                             user_agent=reddit_ua,
                             check_for_async=False)

        def sub_exists(sub):
            exists = True
            try:
                reddit.subreddits.search_by_name(sub, exact=True)
            except NotFound:
                exists = False
            return exists

        if sub_exists(subreddit):
            if not subreddit == 'homepage':
                memes_submissions = reddit.subreddit(subreddit).hot()
                post_to_pick = random.randint(1, 40)
                try:
                    for i in range(0, post_to_pick):
                        submission = next(x for x in memes_submissions if not x.stickied)
                except prawcore.Forbidden:
                    await ctx.send('That subreddit\'s private!')
                else:
                    embed = discord.Embed(
                        title=f'u/{submission.author} in r/{subreddit}',
                        description=f'\"{submission.title}\"\n\nPost URL: {submission.url}\n\n',
                        colour=discord.Colour.random()
                    )

                    embed.set_footer(text='SaCuber Bot')

                    if submission.over_18:
                        if ctx.channel.is_nsfw():
                            if submission.is_self:
                                embed.add_field(name='Post Description:', value=submission.selftext)
                            embed.set_image(url=submission.url)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(
                                'The post you\'re trying to view is NSFW and you\'re not in an NSFW channel!')
                    else:
                        if submission.is_self:
                            embed.add_field(name='Post Description:', value=submission.selftext)
                        embed.set_image(url=submission.url)
                        await ctx.send(embed=embed)
            else:
                await ctx.send('You must include a subreddit.\nExample: `\\reddit minecraft`')
        else:
            await ctx.send('That subreddit doesn\'t exist')

    @commands.command(name='roll', aliases=['dice', 'die'])
    async def roll(self, ctx, faces=6, amount=1):
        try:
            faces = int(faces)
            amount = int(amount)
        except ValueError:
            await ctx.send('Invalid Character! Integer expected.')
        else:
            response = []
            for dice in range(1, amount + 1):
                response.append(str(random.randint(1, faces)))
            await ctx.send(', '.join(response))

    @commands.command(name='python', aliases=['py'])
    async def python(self, ctx, *, code='print("Hello World!")'):
        str_obj = io.StringIO()
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as err:
            return await ctx.send(f"{err.__class__.__name__}: {err}")
        await ctx.send(f'{str_obj.getvalue()}')

    @commands.command(name='quality')
    async def quality(self, ctx, *, msg=None):
        if msg is None:
            await ctx.send('You must include a message!')
        else:
            await ctx.send(' '.join(msg.upper()))

    @commands.command(name='tictactoe', aliases=['ttt'])
    async def tictactoe(self, ctx, p2: discord.Member):
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = ctx.author
            player2 = p2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send(f"It is {player1.mention}'s turn.")
            elif num == 2:
                turn = player2
                await ctx.send(f"It is {player2.mention}'s turn.")
        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")

    @commands.command()
    async def place(self, ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    if gameOver == True:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("You're both bad")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Full numbers between 1 and 9 only")
            else:
                await ctx.send("It's not your turn you stopid")
        else:
            await ctx.send("How do you want to play if you havent started a game")

    @commands.command(name='howcool', aliases=['cool', 'hc'])
    async def cool(self, ctx, mention: discord.Member = 'self'):
        with open(f'{data_path}\\cool.json', "r") as file:
            content = json.load(file)
        if mention == 'self':
            if str(ctx.author.id) in content:
                await ctx.send(f'You\'re {content[str(ctx.author.id)]}% cool')
            else:
                content[str(ctx.author.id)] = random.randint(0, 100)
                with open(f'{data_path}\\cool.json', "w") as file:
                    json.dump(content, file, indent=4)
                await ctx.send(f'You\'re {content[str(ctx.author.id)]}% cool')
        else:
            if str(mention.id) in content:
                await ctx.send(f'{mention.mention} is {content[str(mention.id)]}% cool')
            else:
                content[str(mention.id)] = random.randint(0, 100)
                with open(f'{data_path}\\cool.json', "w") as file:
                    json.dump(content, file, indent=4)
                await ctx.send(f'{mention.mention} is {content[str(mention.id)]}% cool')

    @commands.command(name='forcecool', hidden=True)
    async def forcecool(self, ctx, mention: discord.Member, *, thing):
        if ctx.author.id == 559805065486008331:
            with open(f'{data_path}\\cool.json', "r") as file:
                content = json.load(file)
            content[str(mention.id)] = thing
            with open(f'{data_path}\\cool.json', "w") as file:
                json.dump(content, file, indent=4)
            await ctx.send('alr')
        else:
            await ctx.send('no')

    @commands.command(name='ship', aliases=['sp', 's'])
    async def ship(self, ctx, p1, p2):
        with open(f'{data_path}\\ship.json', 'r') as file:
            content = json.load(file)
        p1 = p1.replace("!", "")
        p2 = p2.replace("!", "")
        joined = f'{p1.lower()} {p2.lower()}'
        joined_r = f'{p2.lower()} {p1.lower()}'
        if joined in content:
            await ctx.send(f'{p1} ------ {str(content[joined])}% ------ {p2}')
        elif joined_r in content:
            await ctx.send(f'{p1} ------ {str(content[joined_r])}% ------ {p2}')
        else:
            content[joined] = random.randint(0, 100)
            with open(f'{data_path}\\ship.json', 'w') as file:
                json.dump(content, file, indent=4)
            await ctx.send(f'{p1} ------ {str(content[joined])}% ------ {p2}')

    def checkWinner(self, winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True

    @commands.command(aliases=['tttleave', 'tictactoeleave', 'leavettt', 'leave_ttt'])
    async def ttt_leave(self, ctx):
        global player1, player2, gameOver
        if gameOver == False:
            if ctx.author == player1:
                gameOver = True
                await ctx.send(f'{ctx.author.mention} forfeited. {player2.mention} wins!')
            elif ctx.author == player2:
                gameOver = True
                await ctx.send(f'{ctx.author.mention} forfeited. {player1.mention} wins!')
            else:
                await ctx.send('You aren\'t playing in any game. Why do you want to leave')
        else:
            await ctx.send('A game isnt fucking running what do you want')

    @commands.command(name='pokedex', aliases=['pokemon'])
    async def pokedex(self, ctx, pokemon):
        pokeinfo = pokedex.get_pokemon(pokemon.lower())
        if 'error' in pokeinfo:
            await ctx.send('Thats not a fucking pokemon you moron')
        else:
            embed = discord.Embed(
                title=pokeinfo[0]['name'],
                description=pokeinfo[0]['description'],
                colour=discord.Colour.random()
            )
            embed.set_footer(text='SaCuber Bot')
            embed.set_image(url=pokeinfo[0]['sprite'])
            embed.add_field(name='Name: ', value=pokeinfo[0]['name'], inline=False)
            embed.add_field(name='Number: ', value=pokeinfo[0]['number'], inline=False)
            embed.add_field(name='Generation: ', value=str(pokeinfo[0]['gen']), inline=True)
            embed.add_field(name='Type(s): ', value=', '.join(pokeinfo[0]['types']), inline=False)
            embed.add_field(name='Height: ', value=pokeinfo[0]['height'], inline=True)
            embed.add_field(name='Weight: ', value=pokeinfo[0]['weight'], inline=False)
            embed.add_field(name='Evolutions: ', value=', '.join(pokeinfo[0]['family']['evolutionLine']), inline=True)
            embed.add_field(name='Is Starter: ', value=pokeinfo[0]['starter'], inline=False)
            embed.add_field(name='Is Legendary: ', value=pokeinfo[0]['legendary'], inline=True)
            embed.add_field(name='Abilities: ',
                            value=f'Normal: {", ".join(pokeinfo[0]["abilities"]["normal"])}; Hidden: {", ".join(pokeinfo[0]["abilities"]["hidden"])}',
                            inline=False)
            await ctx.send(embed=embed)

    @commands.command(name='clap')
    async def clap(self, ctx, *, message):
        split = message.split(' ')
        await ctx.send(' :clap: '.join(split))

    @commands.command(name='emojify')
    async def emojify(self, ctx, *, message):
        end_message = []
        with open(f'{data_path}\\emojicharacters.json', "r") as file:
            emoji_characters = json.load(file)
        for character in message:
            if character.lower() in emoji_characters:
                end_message.append(f'{emoji_characters[character.lower()]} ')
            else:
                return
        await ctx.send(''.join(end_message))

    @commands.command(name='hack')
    async def hack(self, ctx, person: discord.Member):
        message = await ctx.send(f'Initiating hack against {person.mention}...')
        await asyncio.sleep(1)
        await message.edit(content=f'Gaining access to {person.name}\' account... (Retrieving email)')
        await asyncio.sleep(0.7)
        await message.edit(content=f'Gaining access to {person.name}\'s account... (Email Retrieved)')
        await asyncio.sleep(0.4)
        await message.edit(content=f'Gaining access to {person.name}\'s account... (Brute Forcing Password)')
        await asyncio.sleep(0.7)
        await message.edit(content=f'Gaining access to {person.name}\'s account... (Password Brute Forced)')
        await asyncio.sleep(0.55)
        await message.edit(content=f'Gaining access to {person.name}\'s account... (Bypassing 2FA)')
        await asyncio.sleep(0.7)
        await message.edit(content=f'Gaining acess to {person.name}\'s account... (2FA Bypassed)')
        await asyncio.sleep(0.3)
        await message.edit(content='Access Gained')
        await asyncio.sleep(0.55)
        await message.edit(content='Checking Discord Info...')
        await asyncio.sleep(2)
        await message.edit(content=f'Checking Discord Info:\n**Server list:** {ctx.guild.name}, The Official Furry '
                                   f'Community Discord Server, Flat Earth Society Discord, Official BTS Fan Discord '
                                   f'Server')
        await asyncio.sleep(2.3)
        await message.edit(content=f'Checking Discord Info:\n**Server list:** {ctx.guild.name}, The Official Furry '
                                   f'Community Discord Server, Flat Earth Society Discord, Official BTS Fan Discord '
                                   f'Server\n**Latest DM:**\n"i thought it\'d be bigger, really"')
        await asyncio.sleep(1.5)
        await message.edit(content=f'Checking Discord Info:\n**Server list:** {ctx.guild.name}, The Official Furry '
                                   f'Community Discord Server, Flat Earth Society Discord, Official BTS Fan Discord '
                                   f'Server\n**Latest DM:**\n"i thought it\'d be bigger, really"\n**Most common '
                                   f'word:**\n"OwO"')
        await asyncio.sleep(1)
        await message.edit(content='Finding IP address:')
        await asyncio.sleep(0.6)
        await message.edit(content='IP address: `192.168.42.69`')
        await asyncio.sleep(0.7)
        await message.edit(content=f'Reporting {person.name} for violating discord\'s TOS')
        await asyncio.sleep(0.8)
        await message.edit(content=f'{person.mention} has been hacked. No problem. Get pwned')

    @commands.command(name='mock')
    async def mock(self, ctx, *, message):
        lst = [str.upper, str.lower]
        await ctx.send(f'"{"".join(choice(lst)(c) for c in message)}"')

    @commands.command(name='leetify', aliases=['leet'])
    async def leetify(self, ctx, *, message):
        changes = {
            'A': '4',
            'B': '8',
            'E': '3',
            'G': '9',
            'I': '1',
            'O': '0',
            'S': '5',
            'T': '7',
            'Z': '2',
            'CK': 'X'
        }

        change_list = changes.keys()

        message = message.upper()

        for change in change_list:
            if change in change_list:
                message = message.replace(change, changes[change])
            else:
                return

        await ctx.send(message)

    @commands.command(name='spoil', aliases=['spoiler'])
    async def spoil(self, ctx, *, message):
        split = []
        for character in message:
            split.append(f'||{character}||')
        await ctx.send("".join(split))

    @commands.command(name='joke', aliases=['jokes'])
    async def joke(self, ctx, *, selectors='Any'):
        selectors = selectors.split(' ')

        categories = ['Misc']
        blacklisted = ['nsfw', 'religious', 'political', 'racist', 'sexist', 'explicit']

        for selector in selectors:
            if selector.lower().capitalize() in ['Programming', 'Misc', 'Dark', 'Pun', 'Spooky', 'Christmas', 'Any']:
                categories.append(selector)
            elif selector in blacklisted:
                blacklisted.remove(selector)
            else:
                await ctx.send(f'"{selector}" That\'s not a thing wdym')

        if not blacklisted:
            blacklisted_url = '?format=txt'
        else:
            blacklisted_url = f'?blacklistFlags={",".join(blacklisted)}&format=txt'

        if 'Misc' in categories and len(categories) > 1:
            categories.remove('Misc')

        url_selectors = f'{",".join(categories)}{blacklisted_url}'

        joke = requests.get(f'https://v2.jokeapi.dev/joke/{url_selectors}')
        await ctx.send(joke.text)

    @commands.command(name='pun')
    async def pun(self, ctx):
        await ctx.send(requests.get(f'https://v2.jokeapi.dev/joke/pun?format=txt').text)

    @commands.command(name='doot')
    async def doot(self, ctx, *, message):
        message = message.split(' ')
        await ctx.send(' \💀\🎺 '.join(message))

    @commands.command(name='imagine')
    async def imagine(self, ctx, *, message):
        embed = discord.Embed(
            name="\u200b",
            description=f'imagine {message}',
            colour=discord.Colour.random()
        )
        embed.set_footer(text=f"{ctx.author.name} is using all their brain power to imagine")
        await ctx.send(embed=embed)

    @commands.command(name='trump', aliases=['donald_trump', 'donald'])
    async def trump(self, ctx):
        r = requests.get('https://www.tronalddump.io/random/quote')
        quote = r.json()['value'].split('https://')[0]
        date = r.json()['appeared_at'][0:-14].split('-')
        await ctx.send(f'"{quote}"\n\n*-Donald Trump, {date[2]}/{date[1]}/{date[0]}*')

    @commands.command(name='advice', aliases=['advise'])
    async def advice(self, ctx):
        await ctx.send(requests.get('https://api.adviceslip.com/advice').json()['slip']['advice'])

    @commands.command(name='dog')
    async def dog(self, ctx, *, breed = 'random'):
        if breed == 'random':
            r = requests.get(f'https://dog.ceo/api/breeds/image/random').json()
        else:
            breed_split = breed.split(' ')
            if len(breed_split) == 1:
                r = requests.get(f'https://dog.ceo/api/breed/{breed.lower()}/images/random').json()
            else:
                r = requests.get(f'https://dog.ceo/api/breed/{breed_split[1].lower()}/{breed_split[0].lower()}/images/random').json()
        if r['status'] != 'success':
            if r['message'] == 'Breed not found (master breed does not exist)':
                await ctx.send('That\'s not a breed what do you mean do you have stupid')
            else:
                await ctx.send(f'Ayo something went wrong and I don\'t know why.\nError: {r["message"]}')
        else:
            embed = discord.Embed(
                title='Here ya go :)',
                description='\u200b',
                colour=discord.Colour.random()
            )
            embed.set_footer(text='SaCuber Bot')
            embed.set_image(url=r['message'])
            await ctx.send(embed=embed)


    @trump.error
    async def trump_error(self, ctx, error):
        await ctx.send(f'Something\'s gone wrong and I don\'t know why.\nError: {error}')

    @advice.error
    async def advice_error(self, ctx, error):
        await ctx.send(f'Something\'s gone wrong and I don\'t know why.\nError: {error}')

    @doot.error
    async def doot_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('What do you want to doot-ify bro')
        else:
            await ctx.send(f'Something\'s gone wrong and I don\'t know why.\nError: {error}')

    @spoil.error
    async def spoil_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('What do you even want to spoil?')
        else:
            await ctx.send(f'Something\'s gone wrong and I don\'t know why.\nError: {error}')

    @leetify.error
    async def leetify_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Y0U\'R3 FUX1N9 57UP1D.')
        else:
            await ctx.send(f'Something went wrong and i dont know why.\nError: {error}')

    @mock.error
    async def mock_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('what are you gonna mock? me? no you aren\'t you fool')
        else:
            await ctx.send(f'Something went wrong and I don\'t know what nor why\nError: {error}')

    @hack.error
    async def hack_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Hold on who tf do you want to hack')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('You have to ping someone yknow')
        else:
            await ctx.send(f'Something went wrong and I dont know what nor how.\nError: {error}')

    @ship.error
    async def ship_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('ayo put 2 things in you stopid')

    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")

    @cool.error
    async def cool_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Ayo das not a person')

    @pokedex.error
    async def pokedex_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('yo where pokemon')


def setup(client):
    client.add_cog(Fun(client))
