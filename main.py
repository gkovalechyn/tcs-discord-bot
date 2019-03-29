import discord
from random import randint
from discord.ext import commands
from com.pbo_downloader import PBODownloader
from com.role_selector import RoleSelector
from com.data.cues import cue_message
from com.data.cues import reading_message
from com.briefer import Briefer
from com.deploy import batch_exec
from com.next_next_op import next_next_main
from com.data.amazon_embed import amazon_embed
from config import client, TOKEN, main_path, ww2_path

client.remove_command('help')
msgs = []

@client.command(pass_context=True)
@commands.has_any_role('upload', 'admin', 'moderator')
async def upload(ctx):
    pbo = PBODownloader()
    await pbo.downloader(ctx, main_path)

@client.command(pass_context=True)
@commands.has_any_role('upload', 'admin', 'moderator')
async def uploadww2(ctx):
    pbo = PBODownloader()
    await pbo.downloader(ctx, ww2_path)

@client.command(pass_context=True)
@commands.has_role('admin')
async def deploy(ctx):
    await client.delete_message(ctx.message)
    await batch_exec()

@client.command(pass_context=True)
async def tism(ctx):
    await client.delete_message(ctx.message)
    await client.send_message(ctx.message.channel, cue_message)

@client.command(pass_context=True)
async def booktism(ctx):
    await client.delete_message(ctx.message)
    await client.send_message(ctx.message.channel, reading_message)

@client.command(pass_context=True)
async def embed(ctx):
    await client.delete_message(ctx.message)
    role = RoleSelector()
    await role.rotation(ctx, msgs)

@client.command(pass_context=True)
async def briefing(ctx):
    br = Briefer()
    await br.rotation(ctx)

@client.command(pass_context=True)
async def eject(ctx):
    await client.say("*has kicked " + ctx.message.author.display_name + " from the server!*")
    luck = randint(1, 20)
    if luck == 20:
        await client.say("*" + ctx.message.author.display_name + " has hit the canopy!*")
        user_id = ctx.message.server.get_member(ctx.message.author.id)
        await client.kick(user_id)

@client.command(pass_context=True)
async def amazon(ctx):
    await client.send_message(ctx.message.channel, embed=amazon_embed)

@client.event
async def on_reaction_add(reaction, ctx):
    roleChannelId = '557248486324699176'
    if reaction.message.channel.id != roleChannelId:
        return
    if reaction.emoji == "👍":
        user_id = ctx.reaction.server.get_member(ctx.message.author.id)
        await client.add_roles(user_id, '558351518831607831')

@client.event
async def on_message(message):
    if client.user in message.mentions:
        await client.add_reaction(message, '\U0001f5de')
    msg = str(message.content)
    com_msg = msg.split(" ", 2)
    msg = msg.replace(" ", "")
    if message.author.id == '206380629523300352' \
        and msg.startswith('<:') \
        and msg.endswith('>'):
        await client.delete_message(message)
    if com_msg[0].lower().startswith('!nextnext') \
        and com_msg[0].lower().endswith('op'):
        await next_next_main(com_msg[0], message.channel)
    await client.process_commands(message)

client.run(TOKEN)