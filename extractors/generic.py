#!/usr/bin/env python3
"""
Универсальный экстрактор для обычных HLS-потоков.
Работает с прямыми ссылками на m3u8-плейлисты.
"""

from typing import Optional, Dict
from .base import BaseExtractor


class GenericExtractor(BaseExtractor):
    """Экстрактор для стандартных HLS-потоков"""
    
    def extract(self) -> Optional[Dict]:
        """
        Извлечение информации для обычного m3u8.
        
        Returns:
            Словарь с m3u8_url
        """
        # Для generic экстрактора URL уже является m3u8
        return {
            'm3u8_url': self.url,
            'title': 'video',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
    
    @staticmethod
    def can_handle(url: str) -> bool:
        """Проверка на m3u8 URL"""
        return url.endswith('.m3u8') or 'm3u8' in url
