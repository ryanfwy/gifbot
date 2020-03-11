''''''

import os
from telegram import Bot

from global_config.protected_config import _telegrambot_token
from global_config.environment_config import _base_dir, _temp_dir
from telegram_bot.func_helper import random_string, zip_dir


class GifDownloader():
    def __init__(self):
        ''''''
        self.bot = Bot(_telegrambot_token)

    @staticmethod
    def mp42gif(in_file_path, out_file_path):
        ''''''
        palette_path = out_file_path.replace('.gif', '_palette.png')
        command = 'ffmpeg -y -i %(mp4)s -vf fps=10,scale=-1:-1:flags=lanczos,palettegen %(palette)s'
        command = command % {'mp4': in_file_path, 'palette': palette_path}
        status = os.system(command + ' > /dev/null 2>&1')
        if status != 0:
            os.path.isfile(palette_path) and os.remove(palette_path)
            raise Exception('ffmpeg error: execute gif => _palette.png')

        command = 'ffmpeg -y -i %(mp4)s -i %(palette)s -filter_complex "fps=10,scale=-1:-1:flags=lanczos[x];[x][1:v]paletteuse" %(gif)s'
        command = command % {'mp4': in_file_path, 'palette': palette_path, 'gif': out_file_path}
        status = os.system(command + ' > /dev/null 2>&1')
        os.path.isfile(palette_path) and os.remove(palette_path)
        if status != 0:
            raise Exception('ffmpeg error: execute .gif => .mp4')
        else:
            return out_file_path

    def download_gif(self, file_id, save_dir=None, random_name=False):
        ''''''
        gif = file_id if not isinstance(file_id, str) else self.bot.get_file(file_id)

        # use default `temp` path
        save_dir = save_dir or _temp_dir
        file_name = gif.file_path.split('/')[-1]
        if random_name:
            file_name = random_string() + '.mp4'
        file_path = os.path.join(save_dir, file_name)
        out_path = file_path.replace('mp4', 'gif')

        # download and convert
        gif.download(custom_path=file_path)
        self.mp42gif(file_path, out_path)

        return (file_path, out_path)

    def download_gif_pack(self, file_id, pack_name, out_path=None):
        ''''''
        # make dir `pack_name`
        file_dir = os.path.join(_temp_dir, pack_name)
        os.path.isdir(file_dir) or os.makedirs(file_dir)

        # download and convert
        self.download_gif(file_id, save_dir=file_dir, random_name=True)

        # zip
        out_path = out_path or file_dir + '.zip'
        zip_dir(file_dir, out_path)

        return out_path


_gif = GifDownloader()
download_gif = _gif.download_gif
download_gif_pack = _gif.download_gif_pack


if __name__ == '__main__':
    pass
