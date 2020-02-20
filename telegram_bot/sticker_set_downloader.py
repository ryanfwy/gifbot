''''''

import os
from PIL import Image
from telegram import Bot

from global_config.protected_config import _telegrambot_token
from global_config.environment_config import _base_dir, _temp_dir
from telegram_bot.func_helper import random_string, zip_dir


class StickerSetDownloader():
    def __init__(self):
        ''''''
        self.num_threads = 4
        self.bot = Bot(_telegrambot_token)

    @staticmethod
    def webp2png(in_file_path, out_file_path):
        ''''''
        im = Image.open(in_file_path)
        im.save(out_file_path, 'PNG')
        return out_file_path

    @staticmethod
    def tgs2mp4(in_file_path, out_file_path):
        ''''''
        json_path = out_file_path.replace('mp4', 'json')
        command = 'tgsconvert.py %(tgs)s %(json)s > /dev/null 2>&1'
        command = command % {'tgs': in_file_path, 'json': json_path}
        status = os.system(command)
        if status != 0:
            os.remove(json_path)
            raise Exception('tgsconvert.py error: execute .tgs => .json')

        command = 'puppeteer-lottie -q -i %(json)s -o %(mp4)s > /dev/null 2>&1'
        command = command % {'json': json_path, 'mp4': out_file_path}
        status = os.system(command)
        os.remove(json_path)
        if status != 0:
            raise Exception('puppeteer-lottie error: execute .json => .mp4')
        else:
            return out_file_path

    @staticmethod
    def mp42gif(in_file_path, out_file_path):
        ''''''
        command = 'ffmpeg -y -i %(mp4)s -filter_complex "fps=30" %(gif)s'
        command = command % {'mp4': in_file_path, 'gif': out_file_path}
        status = os.system(command + ' > /dev/null 2>&1')
        if status != 0:
            raise Exception('ffmpeg error: execute .mp4 => .gif')
        else:
            return out_file_path

    def download_sticker(self, file_id, save_dir=None, random_name=False):
        ''''''
        sticker = file_id if not isinstance(file_id, str) else self.bot.get_file(file_id)

        # use default `temp` path
        save_dir = save_dir or _temp_dir
        file_name = sticker.file_path.split('/')[-1]
        if random_name:
            file_name = random_string() + '.webp'
        file_path = os.path.join(save_dir, file_name)
        out_path = file_path.replace('webp', 'png')

        # download and convert
        sticker.download(custom_path=file_path)
        self.webp2png(file_path, out_path)

        return (file_path, out_path)

    def download_sticker_set(self, sticker_set_name, out_path=None):
        ''''''
        sticker_set = self.bot.get_sticker_set(sticker_set_name)
        stickers = sticker_set.stickers

        # make dir `sticker_set_name`
        file_dir = os.path.join(_temp_dir, sticker_set_name)
        os.path.isdir(file_dir) or os.makedirs(file_dir)

        # download and convert
        for sticker in stickers:
            file_id = sticker.file_id
            self.download_sticker(file_id, save_dir=file_dir, random_name=True)

        # zip
        out_path = out_path or file_dir + '.zip'
        zip_dir(file_dir, out_path)
        return out_path

    def download_sticker_animated(self, file_id, save_dir=None, random_name=False):
        ''''''
        sticker = file_id if not isinstance(file_id, str) else self.bot.get_file(file_id)

        # use default `temp` path
        save_dir = save_dir or _temp_dir
        file_name = sticker.file_path.split('/')[-1]
        if random_name:
            file_name = random_string() + '.tgs'
        file_path = os.path.join(save_dir, file_name)
        out_path_mp4 = file_path.replace('tgs', 'mp4')
        out_path_gif = file_path.replace('tgs', 'gif')

        # download and convert
        sticker.download(custom_path=file_path)
        self.tgs2mp4(file_path, out_path_mp4)
        self.mp42gif(out_path_mp4, out_path_gif)

        return (file_path, out_path_mp4, out_path_gif)

    def download_sticker_animated_pack(self, file_id, pack_name, out_path=None):
        ''''''
        # make dir `pack_name`
        file_dir = os.path.join(_temp_dir, pack_name)
        os.path.isdir(file_dir) or os.makedirs(file_dir)

        # download and convert
        self.download_sticker_animated(file_id, save_dir=file_dir, random_name=True)

        # zip
        out_path = out_path or file_dir + '.zip'
        zip_dir(file_dir, out_path)

        return out_path


_sticker = StickerSetDownloader()
download_sticker = _sticker.download_sticker
download_sticker_set = _sticker.download_sticker_set
download_sticker_animated_pack = _sticker.download_sticker_animated_pack


if __name__ == '__main__':
    pass
