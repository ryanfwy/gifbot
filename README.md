# GIFBot

Here is the repo of [@GIFDownloader_bot](https://t.me/GIFDownloader_bot) which help exporting GIF, Sticker and Sticker Set from Telegram to local.

To develop and run this bot, you may require the following basic environments.

1. A machine that can install `Python 3.6` and `FFmpeg`, for example `Linux (CentOS 7.4)`.
2. Check your security settings and ensure the port `8443` is opened if you want to setup webhook with your bot.
3. Own a bot and get the token from [@BotFather](https://t.me/BotFather).
4. Follow the installation tips.


## Installation

This guidance requires `CentOS 7.4`. If not, you can try translate them to your system commands.

**Notice**: before installation, don't forget to change to `root` user by calling `sudo su -`.

### 1. [Python3](https://www.python.org/downloads/)
```bash
yum -y install epel-release
yum -y install https://centos7.iuscommunity.org/ius-release.rpm
yum -y install python36u
yum -y install python36u-pip
```

Check if it is installed successfully, run:

```bash
python3.6 -V
pip3.6 -V
```

### 2. [FFmpeg](https://www.ffmpeg.org/download.html)
```bash
rpm –import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
yum -y install ffmpeg ffmpeg-devel
```

Check if it is installed successfully, run:

```bash
ffmpeg -version
```

### 3. Repository

```
git clone https://github.com/ryanfwy/gifbot.git
```

It is highly recommend you to install python `requirements.txt` under the virtual environment.

```bash
cd gifbot

python3 -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt
```

### 4. Configuration

#### 1) Setup bot token

It requires a file `global_config/protected_config.py` to place your bot token.

```bash
touch global_config/protected_config.py
echo "_telegrambot_token = 'YOUR_TOKEN'" > global_config/protected_config.py
```

And your bot's locations on `global_config/environment_config.py`.

```python
_base_dir = 'YOUR_ABSOLUTE_BOT_LOCATION'
_temp_dir = 'YOUR_ABSOLUTE_CACHE_LOCATION'
```

#### 2) Setup webhook (optional)

If you want to run your bot using webhook, it requires a SSL certificate and your own domain.

```bash
mkdir .openssl && cd .openssl
openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out cert.pem && cd ..
```

#### 3) Setup entrance

If you want to run your bot using webhook, you should change `YOUR_DOMAIN` on `main_run_bot.py`.

```python
import os

from global_config.environment_config import _base_dir
from telegram_bot.bot_executor import BotExecutor


if __name__ == '__main__':
    cert_path = os.path.join(_base_dir, '.openssl/cert.pem')
    key_path = os.path.join(_base_dir, '.openssl/private.key')
    webhook_url = 'https://YOUR_DOMAIN:8443/gifbot'
    BotExecutor(cert_path=cert_path,
                key_path=key_path,
                webhook_url=webhook_url).execute()
```

Otherwise, if you just simply debug and test the code, overwrite `main_run_bot.py` like this:

```python
from telegram_bot.bot_executor import BotExecutor

if __name__ == '__main__':
    BotExecutor().execute()
```

#### 4) Run
```bash
python3 main_run_bot.py
```

## Quick Installation

Install on this way WON'T setup all the steps metioned above, such as webhook and bot entrance, but it can help you to install some basic environments quickly.

**Notice**: `CentOS 7.4` required.

```bash
bash install_centos.sh
```

## Questions

To `activate` and `deactivate` the vitural environment, run:

```bash
# activate
source .env/bin/activate

# deactivate
deactivate
```

## License

This repo has been licnesed by [MIT](https://github.com/ryanfwy/gifbot/blob/master/LICENSE).
