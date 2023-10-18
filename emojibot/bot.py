import asyncio
import logging
import logging.handlers
import os
import sys
from pathlib import Path
from time import time

import discord
from discord.ext.commands import Bot
from dotenv import dotenv_values

BOT_DIR = Path(__file__).absolute().parent
cfg = dotenv_values(BOT_DIR / ".env")


class EmojiBot(Bot):
    cfg: dict[str, str | None]
    launch_time: float

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


async def startup():
    if ((token := cfg.get("DISCORD_TOKEN")) is None) and (
        (token := os.getenv("DISCORD_TOKEN")) is None
    ):
        sys.exit(
            '[ERROR] token not found, make sure "DISCORD_TOKEN" is set in the environment. exiting.'
        )

    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )
    date_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", date_fmt, style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    (intents := discord.Intents.default()).message_content = True
    bot = EmojiBot(command_prefix=".", intents=intents)
    bot.cfg = cfg

    try:
        dev = cfg["DEV"] == "1"
    except KeyError:
        dev = os.getenv("DEV") == "1"

    if dev:
        await bot.load_extension("cogs.hotreload")
        print("loaded cogs.hotreload")
        await bot.load_extension("jishaku")
        print("loaded jishaku")

    for file in (BOT_DIR / "emojibot/cogs").glob("*.py"):
        if file.stem in ["hotreload", "__init__"]:
            continue

        try:
            await bot.load_extension(f"cogs.{file.stem}")
            print(f"loaded cogs.{file.stem}")
        except Exception as e:
            print(f"failed to load extension cogs.{file.stem}")
            print(f"{type(e).__name__}: {e}")

    try:
        bot.launch_time = time()
        await bot.start(token)
    except discord.LoginFailure:
        sys.exit(
            '[ERROR] token not found, make sure "DISCORD_TOKEN" is set in the .env file. exiting.'
        )
    except discord.PrivilegedIntentsRequired:
        sys.exit(
            '[ERROR] message content intent not enabled. go to "https://discord.com/developers/applications" and enable the message content intent. exiting.'
        )


if __name__ == "__main__":
    asyncio.run(startup())
