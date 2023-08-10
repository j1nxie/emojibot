# emojibot

a small Discord bot to help you manage emojis in your servers.

## features

- [x] add emojis
- [ ] delete emojis
- [ ] manage emojis list

## usage

1. copy `.env.example` to `.env` and fill it in.
    - `DISCORD_TOKEN`: bot's token
    - `DEV`: `0` if you're running it on production, `1` if you're doing development work. this enables jishaku and hot reloading.

2. in your shell:
```shell
$ poetry install
$ poetry run python bot.py
```

3. your bot should be up and running!

## license

licensed under the MIT License ([LICENSE](LICENSE) or https://opensource.org/licenses/MIT)

## contribution

unless you explicitly state otherwise, any contribution intentionally submitted for inclusion by you, shall be licensed as above, without any additional terms or conditions.