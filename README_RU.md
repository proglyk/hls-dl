## hls-dl
Универсальная утилита для загрузки видео из HLS-потоков (HTTP Live Streaming).
### Возможности
- ✅ Загрузка обычных m3u8-плейлистов
- ✅ Поддержка защищённых потоков с кастомным шифрованием
- ✅ Выбор качества видео
- ✅ Пакетная загрузка
- ✅ Расширяемая архитектура экстракторов
- ✅ XOR/AES расшифровка
### Требования
pip install requests lxml pycryptodome
FFmpeg должен быть установлен и доступен в PATH.
### Установка
```
git clone https://https://github.com/proglyk/hls-dl.git
cd hls-dl
pip install -r requirements.txt
```
### Использование
#### Обычный HLS-поток
```
python main.py https://test1.flashphoner.com:8445/test/test.m3u8
```
#### Выбор качества
```
python main.py https://test1.flashphoner.com:8445/test/test.m3u8 -r 1280x720
```
#### Защищённый поток
```sh
python main.py https://play.boomstream.com/VCcNtuiw
-k "your_xor_key"
-o video.mp4
```
#### Пакетная загрузка
```sh
python main.py -i urls.txt -o downloads/
```
Формат `urls.txt`: \
https://example.com/video1.m3u8 \
https://example.com/video2.m3u8 \
https://example.com/video3.m3u8
### Архитектура
hls-dl/ \
&nbsp;&nbsp;&nbsp;&nbsp;core/ \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;crypto.py \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;downloader.py \
&nbsp;&nbsp;&nbsp;&nbsp;extractors/ \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;base.py \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;generic.py \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;protected.py \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;boomstream.py \
&nbsp;&nbsp;&nbsp;&nbsp;main.py \
&nbsp;&nbsp;&nbsp;&nbsp;requirements.txt \
&nbsp;&nbsp;&nbsp;&nbsp;README.md

### Создание своего экстрактора
```python
from extractors.base import BaseExtractor

class MyExtractor(BaseExtractor):
def extract(self):
    # Ваша логика извлечения m3u8 URL
    return {
        'm3u8_url': 'https://...',
        'title': 'video_title',
        'headers': {'Referer': '...'}
    }
@staticmethod
def can_handle(url):
    return 'myservice.com' in url
```
### Лицензия
MIT License
### Disclaimer
Эта утилита предназначена только для образовательных целей. 
Уважайте авторские права и условия использования контента.
