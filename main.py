#!usrbinenv python3

HLS Video Downloader - универсальная утилита для загрузки HLS-видео.

Поддерживает
- Обычные m3u8-плейлисты
- Защищённые потоки с кастомным шифрованием
- Выбор качества видео
- Пакетную загрузку


import sys
import argparse
from typing import Optional

from core.downloader import HLSDownloader
from extractors.generic import GenericExtractor
from extractors.protected import ProtectedExtractor


class VideoDownloaderCLI
    Интерфейс командной строки для загрузчика
    
    def __init__(self)
        self.downloader = HLSDownloader()
        self.extractors = [
            GenericExtractor,
            ProtectedExtractor
        ]
    
    def get_extractor(self, url str, xor_key str = None)
        
        Выбор подходящего экстрактора для URL.
        
        Args
            url URL видео
            xor_key XOR-ключ для защищённых потоков
            
        Returns
            Экземпляр экстрактора
        
        for extractor_class in self.extractors
            if extractor_class.can_handle(url)
                print(f[] Используется экстрактор {extractor_class.__name__})
                
                if extractor_class == ProtectedExtractor
                    return extractor_class(url, xor_key=xor_key)
                else
                    return extractor_class(url)
        
        # По умолчанию используем generic
        print([] Используется универсальный экстрактор)
        return GenericExtractor(url)
    
    def download_video(self, url str, output str = None, 
                      resolution str = None, xor_key str = None) - bool
        
        Загрузка одного видео.
        
        Args
            url URL видео или m3u8-плейлиста
            output Имя выходного файла
            resolution Желаемое разрешение
            xor_key XOR-ключ для защищённых потоков
            
        Returns
            True при успешной загрузке
        
        # Получаем экстрактор
        extractor = self.get_extractor(url, xor_key)
        
        # Извлекаем информацию
        print(f[] Извлечение информации из {url})
        video_info = extractor.extract()
        
        if not video_info
            print([!] Не удалось извлечь информацию о видео)
            return False
        
        # Определяем имя файла
        if not output
            output = f{video_info.get('title', 'video')}.mp4
        
        # Загружаем
        print(f[] Начало загрузки {output})
        success = self.downloader.download(
            m3u8_url=video_info['m3u8_url'],
            output_file=output,
            headers=video_info.get('headers'),
            resolution=resolution
        )
        
        return success
    
    def run(self)
        Запуск CLI
        parser = argparse.ArgumentParser(
            description='HLS Video Downloader - загрузка видео из m3u8-плейлистов',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=
Примеры использования

  # Загрузка обычного HLS-потока
  %(prog)s httpsexample.comvideoplaylist.m3u8

  # Загрузка с выбором качества
  %(prog)s httpsexample.comvideo.m3u8 -r 1920x1080

  # Загрузка защищённого потока с XOR-ключом
  %(prog)s httpsprotected.complayer.phpid=123 -k secret_key -o video.mp4

  # Пакетная загрузка из файла
  %(prog)s -i urls.txt -o output_dir
            
        )
        
        parser.add_argument('url', nargs='', help='URL видео или m3u8-плейлиста')
        parser.add_argument('-o', '--output', help='Имя выходного файла')
        parser.add_argument('-r', '--resolution', help='Разрешение (например, 1920x1080)')
        parser.add_argument('-k', '--xor-key', help='XOR-ключ для защищённых потоков')
        parser.add_argument('-i', '--input-file', help='Файл со списком URL для пакетной загрузки')
        parser.add_argument('-d', '--output-dir', default='downloads', help='Директория для сохранения')
        
        args = parser.parse_args()
        
        # Устанавливаем директорию вывода
        self.downloader.output_dir = args.output_dir
        
        # Пакетная загрузка
        if args.input_file
            with open(args.input_file, 'r') as f
                urls = [line.strip() for line in f if line.strip()]
            
            print(f[] Пакетная загрузка {len(urls)} видео)
            for i, url in enumerate(urls, 1)
                print(fn[] Видео {i}{len(urls)})
                output = fvideo_{i03d}.mp4
                self.download_video(url, output, args.resolution, args.xor_key)
        
        # Одиночная загрузка
        elif args.url
            success = self.download_video(
                args.url,
                args.output,
                args.resolution,
                args.xor_key
            )
            sys.exit(0 if success else 1)
        
        else
            parser.print_help()
            sys.exit(1)


if __name__ == '__main__'
    cli = VideoDownloaderCLI()
    cli.run()
