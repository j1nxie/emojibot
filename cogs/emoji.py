from typing import Optional

import discord
import requests
from discord.ext import commands
from discord.ext.commands import Context

from bot import EmojiBot


class EmojiCog(commands.Cog, name="emoji"):
    def __init__(self, bot: EmojiBot) -> None:
        self.bot = bot

    @commands.command("addemoji")
    async def add_emoji(
        self, ctx: Context, emoji: str, emoji_url: Optional[str] = None
    ):
        if emoji_url is not None:
            for guild_emoji in ctx.guild.emojis:  # type: ignore
                name = guild_emoji.name
                print(name)
                if emoji == name:
                    embed = discord.Embed(
                        title="emoji already exists!",
                        description=f"an emoji with the name `{emoji}` already exists in the server.",
                    )
                    await ctx.reply(embed=embed, mention_author=False)
                    return

            emoji_image = requests.get(emoji_url).content
            await ctx.guild.create_custom_emoji(  # type: ignore
                name=emoji, image=emoji_image, roles=[]
            )
            embed = discord.Embed(
                title="added a new emoji!",
                description=f"new emoji `{emoji}` has been added.",
            )
            await ctx.reply(embed=embed, mention_author=False)
        else:
            emoji_data = discord.PartialEmoji.from_str(emoji)
            for guild_emoji in ctx.guild.emojis:  # type: ignore
                name = guild_emoji.name
                if emoji_data.name == name:
                    embed = discord.Embed(
                        title="emoji already exists!",
                        description=f"an emoji with the name `{emoji}` already exists in the server.",
                    )
                    await ctx.reply(embed=embed, mention_author=False)
                    return

            if emoji_data.is_custom_emoji():
                emoji_image = requests.get(emoji_data.url).content
                await ctx.guild.create_custom_emoji(  # type: ignore
                    name=emoji_data.name, image=emoji_image, roles=[]
                )
                embed = discord.Embed(
                    title="added a new emoji!",
                    description=f"new emoji `{emoji}` has been added.",
                )
                await ctx.reply(embed=embed, mention_author=False)


async def setup(bot: EmojiBot):
    await bot.add_cog(EmojiCog(bot))
