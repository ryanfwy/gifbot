''''''

import os
import re
import time
from telegram import File, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CommandHandler, MessageHandler, CallbackQueryHandler, RegexHandler,
                          Updater, Filters, PicklePersistence)
from telegram.ext.dispatcher import run_async

from global_config.protected_config import _telegrambot_token
from global_config.environment_config import _base_dir, _temp_dir
from telegram_bot.sticker_set_downloader import (download_sticker, download_sticker_set,
                                                 download_sticker_animated_pack)
from telegram_bot.gif_downloader import download_gif_pack
from telegram_bot.func_helper import random_string
from localization.translator import l10n
from log_helper.msg_logger import MsgLogger


STICKER_SET = 'sticker_set'
LIMITATION = 100 * 1024 * 1024 # 100MB
LIMITATION_STRING = str(round(LIMITATION/(1024*1024))) + 'MB'


def is_usage_exceed(context, limit=LIMITATION):
    # check new day
    today = time.strftime('%Y-%m-%d', time.localtime())
    user_dict = context.user_data

    # get usage
    if 'today_tag' not in user_dict or user_dict['today_tag'] != today:
        user_dict['today_tag'] = today
        user_dict['today_usage'] = 0
    elif 'today_usage' not in user_dict:
        user_dict['today_usage'] = 0

    usage = user_dict['today_usage']
    return usage >= limit

def set_usage(context, file_path=None):
    if not os.path.isfile(file_path):
        return -1

    # set usage
    file_size = os.path.getsize(file_path)
    user_dict = context.user_data
    user_dict['today_usage'] += file_size
    return user_dict['today_usage']

def check_usage_limit(func):
    def warpper(*args, **kwargs):
        _, update, context, *_ = args
        if is_usage_exceed(context):
            # language
            locale = update.effective_user.language_code
            message = l10n('limit_exceed', locale) % {'limit': LIMITATION_STRING}
            update.effective_message.reply_text(message)
            return None
        else:
            return func(*args, **kwargs)
    return warpper


class BotExecutor():
    def __init__(self,
                 cert_path=None,
                 key_path=None,
                 webhook_url=None,
                 persistence_file_path=os.path.join(_base_dir, '.app_cache/bot_data'),
                 log_file_path=os.path.join(_base_dir, '.app_cache/app.log')):
        ''''''
        # telegram
        self.cert_path = cert_path
        self.key_path = key_path
        self.webhook_url = webhook_url

        # persistence
        _dir = os.path.dirname(persistence_file_path)
        os.path.isdir(_dir) or os.makedirs(_dir)
        self.persistence_file_path = persistence_file_path

        # log
        _dir = os.path.dirname(log_file_path)
        os.path.isdir(_dir) or os.makedirs(_dir)
        self.logger = MsgLogger(log_file=log_file_path).get_logger()

        self.gif_file_size_max = 1 * 1024 * 1024 # 1MB


    ''' helper functions '''

    def base_send_zip(self, file_name, callback, callback_args,
                      update=None, context=None, pack_name=None):
        if not update and not context:
            return -1

        # language
        locale = update.effective_user.language_code

        # parse update and context
        chat = update.effective_chat
        message = update.effective_message

        try:
            file_dir = os.path.join(_temp_dir, file_name)
            zip_file_path = os.path.join(_temp_dir, file_name+'.zip')
            if os.path.isfile(zip_file_path):
                pass
            elif os.path.isdir(file_dir):
                message.reply_text(l10n('zip_packing', locale))
                # wait 10 times, 30 seconds for each
                for _ in range(10):
                    if not os.path.isfile(zip_file_path):
                        time.sleep(30)
                    else:
                        break
                else:
                    message.reply_text(l10n('zip_timeout', locale))
                    return -1
            else:
                message.reply_text(l10n('zip_preparing', locale))
                zip_file_path = callback(*callback_args)

            with open(zip_file_path, 'rb') as f:
                filename = pack_name or file_name
                chat.send_action('upload_document')
                chat.send_document(f, filename=filename+'.zip',
                                reply_to_message_id=message.message_id)

            # count usage
            set_usage(context, file_path=zip_file_path)

        except Exception as e:
            message.reply_text(l10n('exec_error', locale))
            self.logger.error('Exception msg: %s', str(e), exc_info=True)

    @run_async
    def download_sticker_set_async(self, sticker_set_name, update=None, context=None):
        if not update and not context:
            return -1

        # parse update and context
        callback = download_sticker_set
        args = (sticker_set_name,)
        self.base_send_zip(sticker_set_name, callback, args, update=update, context=context)

    @run_async
    def download_gif_pack_async(self, file_id, update=None, context=None):
        if not update or not context:
            return -1

        # language
        locale = update.effective_user.language_code
        message = update.effective_message

        try:
            # parse update and context
            bot = context.bot
            gif = bot.get_file(file_id)
            gif_pack_name = gif.file_path.split('/')[-1].split('.')[0]
            gif_unique_id = random_string() # gif.file_unique_id

            callback = download_gif_pack
            args = (gif, gif_pack_name)
            self.base_send_zip(gif_pack_name, callback, args,
                            update=update, context=context, pack_name=gif_unique_id)

        except Exception as e:
            message.reply_text(l10n('exec_error', locale))
            self.logger.error('Exception msg: %s', str(e), exc_info=True)

    @run_async
    def download_sticker_animated_async(self, file_id, update=None, context=None):
        if not update or not context:
            return -1

        # language
        locale = update.effective_user.language_code
        message = update.effective_message

        try:
            # parse update and context
            bot = context.bot
            sticker = bot.get_file(file_id)
            sticker_pack_name = sticker.file_path.split('/')[-1].split('.')[0]
            sticker_unique_id = random_string() # sticker.file_unique_id

            callback = download_sticker_animated_pack
            args = (sticker, sticker_pack_name)
            self.base_send_zip(sticker_pack_name, callback, args,
                            update=update, context=context, pack_name=sticker_unique_id)

        except Exception as e:
            message.reply_text(l10n('exec_error', locale))
            self.logger.error('Exception msg: %s', str(e), exc_info=True)

    def download_sticker_async(self, file_id, update=None, context=None):
        if not update or not context:
            return -1

        # language
        locale = update.effective_user.language_code

        # parse update and context
        bot = context.bot
        sticker = bot.get_file(file_id)
        sticker_name = sticker.file_path.split('/')[-1].split('.')[0]
        sticker_unique_id = random_string() # sticker.file_unique_id

        chat = update.effective_chat
        message = update.effective_message

        # send action
        chat.send_action('upload_document')

        # download sticker
        file_dir = os.path.join(_temp_dir, sticker_name)
        file_path = os.path.join(_temp_dir, sticker_name, sticker_name+'.png')
        if os.path.isfile(file_path):
            pass
        elif os.path.isdir(file_dir):
            # wait 10 times, 10 seconds for each
            for _ in range(10):
                if not os.path.isfile(file_path):
                    time.sleep(10)
                else:
                    break
            else:
                message.reply_text(l10n('zip_timeout', locale))
                return -1
        else:
            # make dir `sticker_name`
            os.path.isdir(file_dir) or os.makedirs(file_dir)
            _, file_path = download_sticker(sticker, save_dir=file_dir)

        # send document
        sticker_set_name = message.sticker.set_name
        callback_data = ''.join([STICKER_SET, ':', sticker_set_name])
        keyboard = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text=l10n('kb_sticker_set', locale),
                                    callback_data=callback_data),
            ]]
        )
        with open(file_path, 'rb') as f:
            chat.send_document(f, reply_markup=keyboard,
                            filename=sticker_unique_id+'.png',
                            reply_to_message_id=message.message_id)

        # count usage
        set_usage(context, file_path=file_path)


    ''' command functions '''

    def cmd_start(self, update, context):
        ''''''
        # language
        locale = update.effective_user.language_code

        user = update.effective_user
        user_name = '@' + str(user.username)
        first_name = user.first_name
        last_name = user.last_name
        if first_name and last_name:
            user_name = first_name + ' ' + last_name
        elif first_name:
            user_name = first_name
        elif last_name:
            user_name = last_name

        update.message.reply_text(l10n('start', locale) % {'user': user_name})

    def cmd_help(self, update, context):
        ''''''
        # language
        locale = update.effective_user.language_code
        update.message.reply_markdown(l10n('help', locale))

    @check_usage_limit
    def cmd_sticker(self, update, context):
        ''''''
        # language
        locale = update.effective_user.language_code

        file_id = update.effective_message.sticker.file_id
        if update.effective_message.sticker.is_animated:
            update.effective_message.reply_text(l10n('unsupport', locale))
            # print(update.effective_message.sticker)
            # self.download_sticker_animated_async(file_id, update=update, context=context)
        else:
            self.download_sticker_async(file_id, update=update, context=context)

    @check_usage_limit
    def cmd_sticker_set(self, update, context):
        ''''''
        sticker_set_name = context.match.group('sticker_set')
        self.download_sticker_set_async(sticker_set_name, update=update, context=context)

    @check_usage_limit
    def callback_sticker_set(self, update, context):
        ''''''
        # answer
        update.callback_query.answer()

        # remove keyboard
        update.callback_query.edit_message_reply_markup(None)

        # download or send
        callback_data = update.callback_query.data
        sticker_set_name = callback_data.split(':')[-1]
        self.download_sticker_set_async(sticker_set_name, update=update, context=context)

    @check_usage_limit
    def cmd_gif(self, update, context):
        ''''''
        # language
        locale = update.effective_user.language_code

        file_id = update.effective_message.document.file_id
        file_size = update.effective_message.document.file_size or 1.0e10
        if file_size > self.gif_file_size_max:
            update.effective_message.reply_text(l10n('file_size_exceed', locale))
        else:
            self.download_gif_pack_async(file_id, update=update, context=context)

    def error_handler(self, update, context):
        ''''''
        self.logger.error('Exception msg: %s\nUpdate: %s', context.error, update)

    def execute(self):
        ''''''
        # persistence
        pp = PicklePersistence(self.persistence_file_path, single_file=False)

        updater = Updater(_telegrambot_token, use_context=True, persistence=pp)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler('start', self.cmd_start))
        dp.add_handler(CommandHandler('help', self.cmd_help))
        # sticker
        dp.add_handler(MessageHandler(Filters.sticker, self.cmd_sticker))
        # sticker set
        dp.add_handler(CallbackQueryHandler(self.callback_sticker_set, pattern='^%s' % (STICKER_SET)))
        dp.add_handler(MessageHandler(Filters.regex(r'https://t.me/addstickers/(?P<sticker_set>[\s\S]+)'),
                                      self.cmd_sticker_set))
        # gif
        dp.add_handler(MessageHandler(Filters.document.gif, self.cmd_gif))
        # error handler
        dp.add_error_handler(self.error_handler)

        if not self.cert_path or not self.key_path or not self.webhook_url:
            updater.start_polling()
        else:
            updater.start_webhook(listen='0.0.0.0', port=8443, url_path='gifbot',
                                  cert=self.cert_path, key=self.key_path,
                                  webhook_url=self.webhook_url,
                                  bootstrap_retries=0,
                                  clean=True)

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()


if __name__ == '__main__':
    BotExecutor().execute()
