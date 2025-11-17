#!/usr/bin/env python3
"""
Базовый загрузчик HLS-потоков с использованием FFmpeg.
Универсальный модуль для скачивания видео из m3u8-плейлистов.
"""

import os
import subprocess
import re
from typing import Optional, Dict, List
import requests


class HLSDownloader:
    """Базовый класс для загрузки HLS-потоков"""
    
    def __init__(self, output_dir: str = "downloads"):
        """
        Инициализация загрузчика.
        
        Args:
            output_dir: Директория для сохранения видео
        """
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _print(self, message: str, prefix: str = "*"):
        """Вывод сообщения с префиксом"""
        print(f"[{prefix}] {message}")
    
    def parse_m3u8(self, m3u8_url: str, headers: Dict = None) -> Dict[str, str]:
        """
        Парсинг m3u8-плейлиста для извлечения доступных качеств.
        
        Args:
            m3u8_url: URL мастер-плейлиста
            headers: HTTP-заголовки для запроса
            
        Returns:
            Словарь {разрешение: URL}
        """
        try:
            response = requests.get(m3u8_url, headers=headers or {})
            response.raise_for_status()
            content = response.text
        except Exception as e:
            self._print(f"Ошибка при загрузке плейлиста: {e}", "!")
            return {}
        
        qualities = {}
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if line.startswith('#EXT-X-STREAM-INF'):
                # Извлекаем разрешение
                resolution_match = re.search(r'RESOLUTION=(\d+x\d+)', line)
                if resolution_match and i + 1 < len(lines):
                    resolution = resolution_match.group(1)
                    stream_url = lines[i + 1].strip()
                    
                    # Если URL относительный, делаем абсолютным
                    if not stream_url.startswith('http'):
                        base_url = '/'.join(m3u8_url.split('/')[:-1])
                        stream_url = f"{base_url}/{stream_url}"
                    
                    qualities[resolution] = stream_url
        
        return qualities
    
    def download(self, m3u8_url: str, output_file: str, 
                 headers: Dict = None, resolution: str = None) -> bool:
        """
        Загрузка видео из m3u8-плейлиста с помощью FFmpeg.
        
        Args:
            m3u8_url: URL плейлиста (мастер или конкретное качество)
            output_file: Имя выходного файла
            headers: HTTP-заголовки (Referer, User-Agent и т.д.)
            resolution: Желаемое разрешение (например, "1920x1080")
            
        Returns:
            True при успешной загрузке, False при ошибке
        """
        output_path = os.path.join(self.output_dir, output_file)
        
        # Если указано разрешение, пытаемся найти соответствующий поток
        if resolution:
            qualities = self.parse_m3u8(m3u8_url, headers)
            if resolution in qualities:
                m3u8_url = qualities[resolution]
                self._print(f"Выбрано качество: {resolution}")
            elif qualities:
                # Берём лучшее доступное качество
                best = max(qualities.keys(), key=lambda x: int(x.split('x')[1]))
                m3u8_url = qualities[best]
                self._print(f"Запрошенное качество недоступно, выбрано: {best}")
        
        # Формируем команду FFmpeg
        ffmpeg_cmd = ['ffmpeg', '-y']
        
        # Добавляем заголовки если есть
        if headers:
            headers_str = '\r\n'.join([f"{k}: {v}" for k, v in headers.items()])
            ffmpeg_cmd.extend(['-headers', headers_str])
        
        ffmpeg_cmd.extend([
            '-i', m3u8_url,
            '-c', 'copy',
            '-bsf:a', 'aac_adtstoasc',
            output_path
        ])
        
        self._print(f"Запуск FFmpeg для загрузки: {output_file}")
        
        try:
            result = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            self._print(f"Загрузка завершена: {output_path}", "+")
            return True
            
        except subprocess.CalledProcessError as e:
            self._print(f"Ошибка FFmpeg: {e.stderr.decode()}", "!")
            return False
        except FileNotFoundError:
            self._print("FFmpeg не найден. Установите FFmpeg.", "!")
            return False
