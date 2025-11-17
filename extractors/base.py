#!/usr/bin/env python3
"""
Базовый класс для экстракторов.
Определяет интерфейс для извлечения m3u8-URL из различных источников.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional


class BaseExtractor(ABC):
    """Абстрактный базовый класс для всех экстракторов"""
    
    def __init__(self, url: str):
        """
        Инициализация экстрактора.
        
        Args:
            url: URL видео или страницы
        """
        self.url = url
    
    @abstractmethod
    def extract(self) -> Optional[Dict]:
        """
        Извлечение информации о видео.
        
        Returns:
            Словарь с ключами:
            - m3u8_url: URL m3u8-плейлиста
            - title: Название видео (опционально)
            - headers: HTTP-заголовки (опционально)
        """
        pass
    
    @staticmethod
    def can_handle(url: str) -> bool:
        """
        Проверка, может ли экстрактор обработать данный URL.
        
        Args:
            url: URL для проверки
            
        Returns:
            True если экстрактор поддерживает данный URL
        """
        return False
