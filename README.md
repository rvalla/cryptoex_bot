![logo](https://gitlab.com/rodrigovalla/cryptoex/-/raw/themoststable/assets/img/icon.png)

# CryptoEx: telegram bot changelog

This is the code for a telegram bot. The idea is to play with different algorithms to encrypt messages.
It is related to [CryptoEX](https://gitlab.com/rodrigovalla/cryptoex) and [CryptoIM](https://gitlab.com/rodrigovalla/cryptoim) projects.

## online status

**CryptoEX Bot** is not currently deployed. It will be available during some moments of the week while I run
some tests. Stay tuned!  

## running the code

Note that you will need a *config.json* file on root which includes the bot's token to run this software.
I suggest the following fields. Currently only *token* (provided by [@BotFather](https://t.me/BotFather)
and *logging* (info, debugging or persistent) are always mandatory:

```
{
	"bot_name": "CryptoEX Bot",
	"date": "2023-05-10",
	"username": "cryptoexperiments_bot",
	"admin_id": "A mistery",
	"link": "https://t.me/cryptoexperiments_bot",
	"token": "I won't tell you my token",
	"password": "I won't tell you my password either",
	"public_ip": "129.151.114.88",
	"webhook": false,
	"webhook_path": "a_webhook_url_path",
	"webhook_port": 8443,
	"logging": "info"
}

```
## standing upon the shoulders of giants

This little project is possible thanks to a lot of work done by others in the *open-source* community. Particularly in
this case I need to mention:

- [**Python**](https://www.python.org/): the programming language I used.  
- [**python-telegram-bot**](https://python-telegram-bot.org/): the library I used to contact the *Telegram API*.  

Reach **cryptoex bot** [here](https://t.me/cryptoexperiments_bot).
Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
