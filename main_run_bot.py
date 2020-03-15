''''''

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
