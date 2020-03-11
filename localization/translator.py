''''''


_translation = {
    'zh': {
        'start': 'Hi %(user)s，欢迎光临🎊\n\n使用 /help 查看使用方法。',
        'help': '''*TG Downloader Bot 使用方法*
1. GIF 表情：
☛ 直接发送 `GIF 表情`。
☚ 打包的 `MP4` 和 `GIF` 文件。

2. 静态贴纸：
☛ 直接发送`静态贴纸`。
☚ `PNG` 文件。

3. 动态贴纸：
☛ 机器资源有限尚未支持。

4. 静态贴纸集：
☛ 直接发送`静态贴纸`，点击下方按钮「下载完整贴纸集」。
☛ 直接发送`静态贴纸集链接`，如 [EmmaWatsonStickers](https://t.me/addstickers/EmmaWatsonStickers)。
☚ 打包的 `PNG` 文件。

⚠︎ 下载贴纸集十分耗费资源，如非必要还请挑选后逐个下载。对此不胜感激。

请尽情使用 :)''',
        'limit_exceed': '今日用量已超出 %(limit)s，请明天再试',
        'kb_sticker_set': '下载完整贴纸集',
        'unsupport': '资源有限尚未支持，请自行下载转换',
        'zip_preparing': '正在准备文件，时间较长请稍等',
        'zip_packing': '等待文件打包，时间较长请稍等',
        'zip_timeout': '等待超时，请稍后重试',
        'exec_error': '执行错误，请自行下载转换',
        'file_size_exceed': '文件过大，请自行下载转换',
    },

    'en': {
        'start': 'Hi %(user)s，Welcome🎊\n\nUse /help to find detail usage.',
        'help': '''*TG Downloader Bot Usage*
1. GIF:
☛ Send `GIF` directly.
☚ File packed with `MP4` and `GIF`.

2. Static Sticker:
☛ Send `Sticker` directly.
☚ File of `PNG`.

3. Animated Sticker:
☛ Due to the resource limitation, it is not support to decode this type of sticker right now.

4. Static Sticker Set：
☛ Send `Sticker` first, then tap「Download Sticker Set」button.
☛ Send `Sticker Set Link` directly, for example [EmmaWatsonStickers](https://t.me/addstickers/EmmaWatsonStickers).
☚ File packed with a list of `PNGs`.

⚠︎ It is resource consuming to download the entire sticker set, PLEASE select and download what you want one by one if not necessary. I would deeply appreciate if you do so.

Hope you enjoy it :)''',
        'limit_exceed': 'Limit exceed %(limit)s today, try tomorrow',
        'kb_sticker_set': 'Download Sticker Set',
        'unsupport': 'Resource limited, please download and decode by yourself',
        'zip_preparing': 'File preparing, hold on please',
        'zip_packing': 'File packing, hold on please',
        'zip_timeout': 'Timeout waiting, try again later',
        'exec_error': 'Error executing, please download and decode by yourself',
        'file_size_exceed': 'File too large, please download and decode by yourself',
    }
}
_translation_default = _translation['en']


def l10n(key, locale='en'):
    ''''''
    locale = locale or 'en'
    locale = locale[:2] if len(locale) > 2 else locale
    document = _translation.get(locale, _translation_default)
    return document.get(key, key)


if __name__ == '__main__':
    pass
