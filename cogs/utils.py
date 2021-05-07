import os
import random
import json
import pytesseract
from pyowm.owm import OWM
from currency_converter import CurrencyConverter
from PyDictionary import PyDictionary
import textwrap
from pyzbar.pyzbar import decode
import discord
from PIL import Image
import requests
import googletrans
from googletrans import Translator
from discord.ext import commands

iso_langs = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-CN': 'chinese (simplified)',
    'zh-TW': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'}

langs = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb',
         'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka',
         'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw',
         'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo',
         'la', 'lv', 'lt', 'lb', 'mk',
         'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru',
         'sm', 'sr',
         'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv',
         'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']

with open('../data/config.json') as f:
    temp_path = json.load(f)['temp_path']
    tesseract_path = json.load(f)['tesseract_path']
    wapi_key = json.load(f)['wapi_key']


class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='calc', aliases=['calculator', 'calculate', 'math'])
    async def calc(self, ctx, *, expression=None):
        if expression is None:
            await ctx.send('You must input an arithmetic expression (aka math)!')
        else:
            try:
                await ctx.send(eval(expression))
            except NameError:
                await ctx.send('Something went wrong!')

    @commands.command(name='translate', aliases=['t', 'tr', 'tl'])
    async def translate(self, ctx, lang, *, message):
        if lang in langs:
            translator = Translator()
            translated = translator.translate(message, dest=lang)
            end_message = translated.origin + f' ({translated.src}) --> ' + translated.text + f' ({translated.dest})'
            if len(end_message) > 2000:
                for part in textwrap.wrap(end_message, 2000):
                    await ctx.send(part)
            else:
                await ctx.send(end_message)
        else:
            await ctx.send(
                'u gotta put the language as 2 letters (example: "en" for english) (iso 639-1 language codes)')

    @commands.command(name='language', aliases=['l', 'lang', 'detect_language', 'detect_lang', 'detectlang', 'detectlanguage'])
    async def language(self, ctx, *, message):
        translator = Translator()
        detected_lang = translator.detect(message)
        await ctx.send(
            'Ayo i know that language! im ' + str(round(detected_lang.confidence * 100)) + '% sure that it\'s ' +
            iso_langs[detected_lang.lang])

    @commands.command(name='qr / bar', aliases=['qr', 'qrcode ', 'qc', 'barcode', 'bc', 'bar'])
    async def qr_bar(self, ctx):
        try:
            attachment = ctx.message.attachments[0]
            if not str(attachment.url).endswith(('png', 'jpg', 'jpeg', 'webp')):
                await ctx.send('Please input a valid image file!')
            else:
                r = requests.get(attachment.url)
                with open(f'{temp_path}\\code_image.png',
                          'wb') as outfile:
                    outfile.write(r.content)

                data = decode(Image.open(f"{temp_path}\\code_image.png"))
                try:
                    content = data[0][0].decode('utf-8')
                    await ctx.send(content)
                except IndexError:
                    await ctx.send('That doesnt have a code what do you mean')
                os.remove(f'{temp_path}\\code_image.png')
        except IndexError:
            await ctx.send('You gotta attach an image you dumbass')

    @commands.command(name='coinflip', aliases=['flipacoin', 'cf', 'flipcoin', 'headstails'])
    async def coinflip(self, ctx):
        await ctx.send(''.join(random.choice(['Heads', 'Tails'])))

    @commands.command(name='choose')
    async def choose(self, ctx, *, message):
        split_message = message.split(',')
        await ctx.send(split_message[random.randint(0, len(split_message) - 1)])

    @commands.command(name='read')
    async def read(self, ctx):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        try:
            attachment = ctx.message.attachments[0]
            r = requests.get(attachment.url)

            if not str(attachment.url).endswith(('png', 'jpg', 'jpeg', 'webp')):
                await ctx.send('Please input a valid image file!')
            else:
                with open(f'{temp_path}\\{str(ctx.author.id)}',
                          'wb') as outfile:
                    outfile.write(r.content)
                try:
                    await ctx.send(pytesseract.image_to_string(
                        f'{temp_path}\\{str(ctx.author.id)}'))
                except discord.HTTPException:
                    await ctx.send('Couldn\'t identify any letters')
        except IndexError:
            await ctx.send('Attach an image dumbass')

    @commands.command(name='dictionary', aliases=['meaning', 'dict'])
    async def dictionary(self, ctx, *, message):
        final_message = []
        dictionary = PyDictionary()
        meaning = dictionary.meaning(message)
        for category in meaning:
            final_message.append(f'**{category}** - {f". {chr(10)}".join(meaning[category])}')
        await ctx.send(f'**{message.capitalize()}**\n\n{chr(10).join(final_message)}')

    @commands.command(name='synonym', aliases=['synonyms'])
    async def synonym(self, ctx, *, message):
        dictionary = PyDictionary()
        synonyms = dictionary.synonym(message)
        await ctx.send(', '.join(synonyms))

    @commands.command(name='antonym', aliases=['antonyms'])
    async def antonym(self, ctx, *, message):
        dictionary = PyDictionary()
        antonyms = dictionary.antonym(message)
        await ctx.send(', '.join(antonyms))

    @commands.command(name='money', aliases=['currency', 'cc', 'convertcurrency'])
    async def money(self, ctx, source, target, value='1'):
        c = CurrencyConverter()
        source = source.upper()
        target = target.upper()
        value = value.replace(',', '.')
        try:
            int_value = int(value)
        except ValueError:
            await ctx.send('Ayo something\'s wrong i can feel it')
        else:
            try:
                converted = c.convert(int_value, source, target)
            except ValueError:
                await ctx.send('Ayo thats not a currency what do you mean')
            else:
                if converted is not None:
                    await ctx.send(f'{value} ({source}) **->** {str(converted)} ({target})')

    @commands.command(name='weather', aliases=['wt', 'w'])
    async def weather(self, ctx, *, location):
        location = location.capitalize()
        apikey = wapi_key
        owm = OWM(apikey)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(location)
        weather = observation.weather

        embed = discord.Embed(
            title=f'Weather in **{observation.location.name}**',
            description='',
            colour=discord.Colour.random()
        )

        embed.set_footer(text='SaCuber Bot')
        embed.add_field(name='Current Weather Status: ', value=weather.detailed_status.capitalize(), inline=False)
        embed.add_field(name='Today\'s Minimum Temperature: ', value=f'{weather.temperature("celsius")["temp_min"]}Cº ({weather.temperature("fahrenheit")["temp_min"]}Fº)', inline=False)
        embed.add_field(name='Today\'s Maximum Temperature: ', value=f'{weather.temperature("celsius")["temp_max"]}Cº ({weather.temperature("fahrenheit")["temp_max"]}Fº)', inline=False)
        embed.add_field(name='Wind Speed: ', value=f'{weather.wind()["speed"]} m/s ({observation.weather.wind(unit="knots")["speed"]} knots)', inline=False)
        embed.add_field(name='Wind direction: ', value=f'{weather.wind()["deg"]}º', inline=False)
        embed.add_field(name='Today\'s Sunrise: ', value=str(weather.sunrise_time(timeformat='iso')), inline=False)
        embed.add_field(name='Today\'s Sunset: ', value=str(weather.sunset_time(timeformat='iso')), inline=False)
        await ctx.send(embed=embed)

    @weather.error
    async def weather_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Ayo where tf do you want to know the weather on')
        elif str(error) == 'Command raised an exception: NotFoundError: Unable to find the resource':
            await ctx.send('Thats not a valid country or a city you are stupid')
        else:
            await ctx.send(f'Something\'s gone wrong and I don\'t know why.\nError: {error}')

    @money.error
    async def money_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'ve gotta do \\money (Source currency) (Target currency) (Amount)')
        else:
            await ctx.send(f'Something\'s gone wrong and I don\'t know why.\nError: {error}')

    @dictionary.error
    async def dictionary_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('What do you wanna know the meaning of bruh')
        else:
            await ctx.send(f'Something went wrong and I don\'t know why.\nError: {error}')

    @synonym.error
    async def synonym_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('What do you wanna know synonyms of bruh')
        elif TypeError:
            await ctx.send('That word doesn\'t have a synonym')
        else:
            await ctx.send(f'Something went wrong and I don\'t know why.\nError: {error}')

    @antonym.error
    async def antonym_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('What do you wanna know antonyms of bruh')
        elif TypeError:
            await ctx.send('That word doesn\'t have an antonym')
        else:
            await ctx.send(f'Something went wrong and I don\'t know why.\nError: {error}')

    @choose.error
    async def choose_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('What do you wanna choose from')

    @translate.error
    async def translate_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Ayo syntax is \\translate {language} {what you want to translate}')
        elif isinstance(error, googletrans.Translator):
            await ctx.send('u gotta put the language as 2 letters (example: "en" for english)')
        else:
            await ctx.send(f'Something went wrong and I don\'t know what or why\nError: {error}')


def setup(client):
    client.add_cog(Utils(client))
