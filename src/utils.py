from __future__ import annotations

import random

import lru


class OTPHandler:
    def __init__(self, cache_size: int = 2**10):
        self.cache_size = cache_size
        self.lru = lru.LRU(self.cache_size)

    def _generate_otp(self) -> int:
        return random.randint(100_000, 999_999)

    def generate_otp(self, *, email: str) -> int:
        self.lru[email] = self._generate_otp()
        return self.lru[email]

    def validate_otp(self, *, email: str, otp: int) -> bool:
        try:
            self.lru[email]
            validate = self.lru[email] == otp
            if validate:
                del self.lru[email]

            return validate
        except KeyError:
            return False
