import discord
from discord.ext import commands
import sqlite3

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

allowed_roles = [Admin / Staff Role IDs]

conn = sqlite3.connect('embeds.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS saved_embeds (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    footer TEXT)''')
conn.commit()

channel_id_temp = {}

@client.command()
async def embed(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    if any(role.id in allowed_roles for role in ctx.author.roles):
        await ctx.send("`Title:`")
        title = await client.wait_for('message', check=check)
        await ctx.send("`Description:`")
        description = await client.wait_for('message', check=check)
        await ctx.send("`Channel ID:`")
        channel_id_msg = await client.wait_for('message', check=check)
        channel_id = int(channel_id_msg.content)

        channel = client.get_channel(channel_id)
        if channel is None:
            await ctx.send("`Invalid Channel ID`")
            return

        footer = "Your Footer"

        embed = discord.Embed(title=title.content, description=description.content, color=0x000000)
        embed.set_footer(text=footer)

        message_content = "||@everyone||\n"

        await channel.send(message_content, embed=embed)
    else:
        await ctx.send("`No Permission`")

@client.command()
async def cembed(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    if any(role.id in allowed_roles for role in ctx.author.roles):
        await ctx.send("`Title:`")
        title = await client.wait_for('message', check=check)
        await ctx.send("`Description:`")
        description = await client.wait_for('message', check=check)

        footer = None

        await ctx.send("`ID:`")
        embed_id_msg = await client.wait_for('message', check=check)
        embed_id = embed_id_msg.content

        cursor.execute('INSERT INTO saved_embeds (id, title, description, footer) VALUES (?, ?, ?, ?)',
                       (embed_id, title.content, description.content, footer))
        conn.commit()

        await ctx.send(f"`Embed ID {embed_id} saved`")
    else:
        await ctx.send("`No Permission`")

@client.command()
async def sembed(ctx, embed_id: str = None, channel_id: int = None):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    if any(role.id in allowed_roles for role in ctx.author.roles):
        if embed_id is None:
            await ctx.send("`Missing Embed ID`")
            return

        if channel_id is None:
            await ctx.send("`Missing Channel ID`")
            return

        cursor.execute('SELECT * FROM saved_embeds WHERE id = ?', (embed_id,))
        row = cursor.fetchone()

        if row:
            _, title, description, footer = row
            embed = discord.Embed(title=title, description=description, color=0x000000)

            if "embed" in ctx.command.name:
                embed.set_footer(text=footer)

            channel = client.get_channel(channel_id)

            if channel is None:
                await ctx.send("`Invalid Channel ID`")
            else:
                await channel.send(embed=embed)
        else:
            await ctx.send(f"`Embed ID {embed_id} not found`")
    else:
        await ctx.send("`No Permission`")

client.run('Bot-Token')

conn.close()
