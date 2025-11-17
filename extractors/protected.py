#!/usr/bin/env python3
"""
Экстрактор для защищённых HLS-потоков с кастомным шифрованием.
Основан на вашей реализации для Boomstream, но универсализирован.
"""

import os
import re
import json
import time
from base64 import b64decode
from typing import Optional, Dict
from urllib.parse import urlparse
import requests
from lxml.html import fromstring

from .base import BaseExtractor
from core.crypto import CryptoUtils


class ProtectedExtractor(BaseExtractor):
    """
    Экстрактор для защищённых потоков с XOR-обфускацией.
    
    Поддерживает схемы защиты типа:
    - XOR-шифрование конфигурации
    - Токен-based аутентификация
    - Динамическая генерация m3u8 URL
    """
    
    def __init__(self, url: str, xor_key: str = None, referer: str = None):
        """
        Инициализация экстрактора защищённых потоков.
        
        Args:
            url: URL видео
            xor_key: Ключ для XOR-расшифровки
            referer: Referer для HTTP-запросов
        """
        super().__init__(url)
        self.xor_key = xor_key
        self.referer = referer or url
        self.config = None
        self.token = None
    
    def _decode_config(self, encoded_data: str) -> Optional[Dict]:
        """
        Расшифровка XOR-обфусцированной конфигурации.
        
        Args:
            encoded_data: Base64-закодированные и XOR-зашифрованные данные
            
        Returns:
            Распарсенный JSON-конфиг или None при ошибке
        """
        if not self.xor_key:
            print("[!] XOR-ключ не предоставлен")
            return None
        
        try:
            # Декодируем из Base64
            encrypted = b64decode(encoded_data)
            
            # XOR-расшифровка
            decrypted = CryptoUtils.xor_decrypt(encrypted, self.xor_key)
            
            # Парсим JSON
            config = json.loads(decrypted.decode('utf-8'))
            return config
            
        except Exception as e:
            print(f"[!] Ошибка расшифровки конфига: {e}")
            return None
    
    def _fetch_config(self) -> bool:
        """
        Загрузка и расшифровка конфигурации видео.
        
        Returns:
            True при успешной загрузке
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': self.referer
            }
            
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            
            # Парсим HTML для извлечения зашифрованного конфига
            tree = fromstring(response.content)
            
            # Ищем data-config атрибут (или другое место хранения)
            config_element = tree.xpath('//div[@data-config]')
            if not config_element:
                print("[!] Зашифрованный конфиг не найден")
                return False
            
            encoded_config = config_element[0].get('data-config')
            
            # Расшифровываем
            self.config = self._decode_config(encoded_config)
            return self.config is not None
            
        except Exception as e:
            print(f"[!] Ошибка загрузки конфига: {e}")
            return False
    
    def _get_token(self) -> Optional[str]:
        """
        Получение токена доступа к потоку.
        
        Returns:
            Токен или None при ошибке
        """
        if not self.config:
            return None
        
        try:
            # Извлекаем параметры для получения токена
            token_url = self.config.get('token_url')
            video_id = self.config.get('id')
            
            if not token_url or not video_id:
                print("[!] Недостаточно данных для получения токена")
                return None
            
            # Запрашиваем токен
            response = requests.get(
                token_url,
                params={'video_id': video_id},
                headers={'Referer': self.referer}
            )
            response.raise_for_status()
            
            token_data = response.json()
            return token_data.get('token')
            
        except Exception as e:
            print(f"[!] Ошибка получения токена: {e}")
            return None
    
    def extract(self) -> Optional[Dict]:
        """
        Извлечение m3u8 URL из защищённого потока.
        
        Returns:
            Словарь с информацией о видео
        """
        print("[*] Загрузка конфигурации...")
        if not self._fetch_config():
            return None
        
        print("[*] Получение токена доступа...")
        self.token = self._get_token()
        if not self.token:
            print("[!] Не удалось получить токен")
            return None
        
        # Формируем URL m3u8-плейлиста
        base_url = self.config.get('base_url')
        playlist = self.config.get('playlist')
        
        if not base_url or not playlist:
            print("[!] Недостаточно данных для формирования m3u8 URL")
            return None
        
        m3u8_url = f"{base_url}/{playlist}?token={self.token}"
        
        return {
            'm3u8_url': m3u8_url,
            'title': self.config.get('title', 'video'),
            'headers': {
                'Referer': self.referer,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
    
    @staticmethod
    def can_handle(url: str) -> bool:
        """
        Проверка, является ли URL защищённым потоком.
        
        Можно добавить проверку по домену или паттернам URL.
        """
        # Пример: проверка по домену или наличию специфичных паттернов
        protected_patterns = [
            'player.php',
            'embed',
            'protected'
        ]
        return any(pattern in url for pattern in protected_patterns)
