import subprocess
import sys
import time

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import oauth_url

from bot import EmojiBot


class MiscCog(commands.Cog, name="miscellaneous"):
    def __init__(self, bot: EmojiBot) -> None:
        self.bot = bot

    @commands.command("invite")
    async def invite(self, ctx: Context):
        """
        invite this bot to your server!
        """

        permissions = discord.Permissions(
            read_messages=True,
            send_messages=True,
            send_messages_in_threads=True,
            manage_messages=True,
            read_message_history=True,
            create_expressions=True,
            manage_expressions=True,
        )

        invite_link = oauth_url(self.bot.user.id, permissions=permissions)  # type: ignore

        embed = discord.Embed(
            title="invite me!",
            description=f"click [here]({invite_link}) to invite the bot to your server!",
        )

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command("status")
    async def status(self, ctx: Context):
        """
        view the bot's status.
        """

        try:
            revision = (
                subprocess.run(
                    ["git", "rev-parse", "--short", "HEAD"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                .stdout.decode("utf-8")
                .replace("\n", "")
            )
        except FileNotFoundError:
            revision = "unknown"
        if not revision:
            revision = "unknown"

        summary = [
            f"emojibot revision `{revision}`",
            f"discord.py `{discord.__version__}`",
            f"python `{sys.version}` on `{sys.platform}`",
            "",
            f"online since <t:{int(self.bot.launch_time)}:R>",
            "",
            f"average latency: `{round(self.bot.latency * 1000, 2)}`ms.",
        ]

        embed = discord.Embed(
            title="status",
            description="\n".join(summary),
        )

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command("ping")
    async def ping(self, ctx: Context):
        """
        ping the bot!
        """
        start = time.perf_counter()
        message = await ctx.send(embed=discord.Embed(title="ping..."))
        end = time.perf_counter()
        duration = (end - start) * 1000
        await message.edit(
            embed=discord.Embed(
                title="pong!",
                description=f"took {duration:.2f}ms.\nwebsocket latency: {round(self.bot.latency * 1000, 2)}ms.",
            )
        )


async def setup(bot: EmojiBot) -> None:
    await bot.add_cog(MiscCog(bot))
