#!/usr/bin/env python3
"""
Модуль криптографических утилит для работы с защищёнными HLS-потоками.
Поддерживает XOR-обфускацию и AES-128 расшифровку.
"""

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


class CryptoUtils:
    """Утилиты для криптографических операций"""
    
    @staticmethod
    def xor_decrypt(data: bytes, key: str) -> bytes:
        """
        XOR-расшифровка данных с использованием строкового ключа.
        
        Args:
            data: Зашифрованные данные
            key: Строковый ключ для расшифровки
            
        Returns:
            Расшифрованные данные
        """
        key_bytes = key.encode('utf-8')
        key_len = len(key_bytes)
        
        result = bytearray()
        for i, byte in enumerate(data):
            result.append(byte ^ key_bytes[i % key_len])
        
        return bytes(result)
    
    @staticmethod
    def aes128_decrypt(data: bytes, key: bytes, iv: bytes = None) -> bytes:
        """
        AES-128 расшифровка в режиме CBC.
        
        Args:
            data: Зашифрованные данные
            key: 16-байтный ключ
            iv: Вектор инициализации (по умолчанию нулевой)
            
        Returns:
            Расшифрованные данные
        """
        if iv is None:
            iv = b'\x00' * 16
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(data)
        
        try:
            return unpad(decrypted, AES.block_size)
        except ValueError:
            # Если padding некорректен, возвращаем как есть
            return decrypted
    
    @staticmethod
    def md5_hash(data: str) -> str:
        """
        Вычисление MD5-хеша строки.
        
        Args:
            data: Входная строка
            
        Returns:
            MD5-хеш в hex-формате
        """
        return hashlib.md5(data.encode('utf-8')).hexdigest()


class TokenGenerator:
    """Генератор токенов доступа для защищённых потоков"""
    
    @staticmethod
    def generate_token(video_id: str, secret: str) -> str:
        """
        Генерация токена доступа на основе ID видео и секрета.
        
        Args:
            video_id: Идентификатор видео
            secret: Секретный ключ
            
        Returns:
            Сгенерированный токен
        """
        raw = f"{video_id}{secret}"
        return CryptoUtils.md5_hash(raw)
