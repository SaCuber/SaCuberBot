import discord
import os
import json
import requests
import asyncio
import moviepy.editor as mpe
from discord.ext import commands
from pytube import YouTube, exceptions
from PIL import Image, ImageEnhance
from PIL.ImageFilter import EDGE_ENHANCE_MORE, DETAIL

with open('../data/config.json') as f:
    temp_path = json.load(f)['temp_path']


class Media(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def mp4process(self, ctx, link=None, resolution='720p'):

        def combine_audio(vidname, audname, outname, vid_fps):
            vid_clip = mpe.VideoFileClip(vidname)
            aud_clip = mpe.AudioFileClip(audname)
            final_clip = vid_clip.set_audio(aud_clip)
            final_clip.write_videofile(outname, fps=vid_fps)

        def mp4tomp3(file):
            base, ext = os.path.splitext(file)
            file_mp3 = base + '.mp3'
            os.rename(file, file_mp3)

        if link is None:
            await ctx.send('You must include a link!')
        else:
            try:
                yt = YouTube(link)
            except Exception or exceptions.VideoUnavailable:
                await ctx.send('Video is unavailable or not valid.')
            else:
                if yt.streams.filter(res=resolution, only_video=True).first() is None:
                    resolution = yt.streams.filter(only_video=True).order_by('resolution').last().resolution
                    await ctx.send('That video doesn\'t have that resolution, so it\'s converting the highest one')
                try:
                    await asyncio.sleep(15)

                    await ctx.send(f'Converting Video: `{yt.title}` by `{yt.author}` at `{resolution}`')
                    invalids = [
                        '"', '*', '<', '>', ',', '?', '\\', '|', '/', ':', 'CON', 'PRN', 'AUX', 'NUL', 'COM1',
                        'COM2',
                        'COM3',
                        'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5',
                        'LPT6',
                        'LPT7', 'LPT8', 'LPT9'
                    ]
                    vid_title = yt.title
                    fps = yt.streams.filter(res=resolution, only_video=True).first().fps
                    for char in vid_title:
                        if char in invalids:
                            vid_title = vid_title.replace(char, '')

                    await asyncio.sleep(0.1)

                    yt.streams.filter(res=resolution, only_video=True).first().download(
                        temp_path, 'vid')
                    mp4tomp3(yt.streams.filter(only_audio=True).first().download(
                        f'{temp_path}\\', 'aud'))

                    combine_audio(f'{temp_path}\\vid.mp4',
                                  f'{temp_path}\\aud.mp3',
                                  f'{temp_path}\\{vid_title}.mp4', fps)

                except exceptions.PytubeError or AttributeError:

                    await asyncio.sleep(0.1)

                    await ctx.send('That video doesn\'t have that resolution!')
                else:
                    if os.stat(
                            f'{temp_path}\\{vid_title}.mp4').st_size > 8000000:
                        print(os.stat(
                            f'{temp_path}\\{vid_title}.mp4').st_size)
                        await ctx.send(
                            'Video file is too large (More than 8MB)! Please download at a lower resolution!')

                    else:
                        await ctx.send(f'{ctx.author.mention} Done!',
                                       file=discord.File(
                                           f'{temp_path}\\{vid_title}.mp4'))
                    os.remove(f'./temp/{vid_title}.mp4')
                    os.remove(f'./temp/vid.mp4')
                    os.remove(f'./temp/aud.mp3')

    @commands.command(name='mp4', aliases=['ytmp4'])
    async def mp4(self, ctx, link=None, resolution='720p'):
        ctx.bot.loop.create_task(self.mp4process(ctx, link, resolution))

    @commands.command(name='mp3', aliases=['ytmp3'])
    async def mp3(self, ctx, link=None):

        if link is None:
            await ctx.send('You must include a link!')
        else:
            try:
                yt = YouTube(link)
            except Exception or exceptions.VideoUnavailable as error:
                await ctx.send('Link is unavailable or not valid')
                await ctx.send(error)
            else:
                await ctx.send(f'Converting Video: `{yt.title}` by `{yt.author}` to MP3')
                invalids = [
                    '"', '\'', '*', '<', '>', ',', '?', '\\', '|', '/', ':', 'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2',
                    'COM3',
                    'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6',
                    'LPT7', 'LPT8', 'LPT9'
                ]
                vid_title = yt.title
                for char in vid_title:
                    if char in invalids:
                        vid_title = vid_title.replace(char, '')
                out_file = yt.streams.filter(only_audio=True).first().download(
                    temp_path, f'{vid_title}')

                base, ext = os.path.splitext(out_file)
                file_mp3 = base + '.mp3'
                os.rename(out_file, file_mp3)

                if os.stat(f'{temp_path}\\{vid_title}.mp3').st_size > 8000000:
                    await ctx.send('Video file is too large (More than 8MB)!')
                else:
                    await ctx.send('Done!', file=discord.File(
                        f'{temp_path}\\{vid_title}.mp3'))
                os.remove(f'{temp_path}\\{vid_title}.mp3')

    @commands.command(name='fry', aliases=['deepfry', 'imagefry', 'fryimage'])
    async def fry(self, ctx):

        def image_fry(link, filename, extension):
            r = requests.get(link)
            with open(f'{temp_path}\\{filename}{extension}', 'wb') as outfile:
                outfile.write(r.content)
            im = Image.open(f'{temp_path}\\{filename}{extension}')
            ehm = im.filter(EDGE_ENHANCE_MORE)
            ed = ehm.filter(DETAIL)
            ihc = ImageEnhance.Contrast(ed)
            ihc.enhance(4).save(f'{temp_path}\\{filename}{extension}')

        try:
            attachment = ctx.message.attachments[0]
            if not str(attachment.url).endswith(('png', 'jpg', 'jpeg', 'webp')):
                await ctx.send('Please input a valid image file!')
            else:
                name, ext = os.path.splitext(str(attachment.filename))
                try:
                    image_fry(attachment.url, name, ext)
                    await ctx.send(file=discord.File(
                        f'{temp_path}\\{str(attachment.filename)}'))
                except ValueError:
                    await ctx.send('Something went wrong! Make sure your image isn\'t transparent!')
                os.remove(f'{temp_path}\\{str(attachment.filename)}')
        except IndexError:
            attachment = str(ctx.message.author.avatar_url).replace('webp', 'png')[:-10]
            name = str(ctx.message.author.display_name)
            ext = '.png'
            try:
                image_fry(attachment, name, ext)
                await ctx.send(file=discord.File(f'{temp_path}\\{name + ext}'))
            except ValueError:
                await ctx.send('Something went wrong! Make sure your image isn\'t transparent!')
            os.remove(f'{temp_path}\\{name + ext}')

    @commands.command(name='pixelate', aliases=['pixel', 'downscale', 'pixelize'])
    async def pixelate(self, ctx, scale=None):

        def pixelate_image(link, filename, extension, img_scale: int):
            r = requests.get(link)
            with open(f'{temp_path}\\{filename}{extension}', 'wb') as outfile:
                outfile.write(r.content)
            im = Image.open(f'{temp_path}\\{filename}{extension}')
            width, height = im.size
            width = round(width / img_scale)
            height = round(height / img_scale)
            resized = im.resize((width, height))
            result = resized.resize(im.size, Image.NEAREST)
            result.save(f'{temp_path}\\{filename}{extension}')

        if scale is None:
            await ctx.send('You must include a scale (Number that resolution will be divided by)')
        else:
            try:
                if int(scale) <= 0:
                    await ctx.send('You must enter a natural number!')
                else:
                    scale = int(scale)
                    try:
                        attachment = ctx.message.attachments[0]
                        if not str(attachment.url).endswith(('png', 'jpg', 'jpeg', 'webp')):
                            await ctx.send('Please input a valid image file!')
                        else:
                            name, ext = os.path.splitext(str(attachment.filename))
                            try:
                                pixelate_image(attachment.url, name, ext, scale)
                                await ctx.send(file=discord.File(
                                    f'{temp_path}\\{str(attachment.filename)}'))
                            except ValueError:
                                await ctx.send('Something went wrong! Make sure your image isn\'t transparent!')
                            os.remove(
                                f'{temp_path}\\{str(attachment.filename)}')
                    except IndexError:
                        attachment = str(ctx.message.author.avatar_url).replace('webp', 'png')[:-10]
                        name = str(ctx.message.author.display_name)
                        ext = '.png'
                        try:
                            pixelate_image(attachment, name, ext, scale)
                            await ctx.send(
                                file=discord.File(f'{temp_path}\\{name + ext}'))
                        except ValueError:
                            await ctx.send('Something went wrong! Make sure your image isn\'t transparent!')
                        os.remove(f'{temp_path}\\{name + ext}')
            except ValueError:
                await ctx.send('Invalid scale character!')


def setup(client):
    client.add_cog(Media(client))
