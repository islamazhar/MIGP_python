# -*- coding: utf-8 -*-

import argon2
import hashlib
import random 
import string
import time 
import numpy as np

SALT = bytes("39902880320387397838562462499352873999292776702085415867387464148861516806822", encoding="UTF-8")

def _argon2(byte_str):
    hash = argon2.hash_password_raw (time_cost=argon2.DEFAULT_TIME_COST, memory_cost=argon2.DEFAULT_MEMORY_COST, parallelism=argon2.DEFAULT_PARALLELISM, hash_len=argon2.DEFAULT_HASH_LENGTH, password=byte_str, salt=SALT, type=argon2.low_level.Type.ID)
    return hash

def sha256(str):
    hash = hashlib.sha256(str.encode('utf-8')).digest()
    return hash.hex()

def sha256bin(byte_str):
    digest = hashlib.sha256(byte_str).digest()
    return digest

def get_random_string(size):
    random_number = [random.choice(string.ascii_letters + string.digits) for n in range(size)] # 32 bytes
    return "".join(random_number)
