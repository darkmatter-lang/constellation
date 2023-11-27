#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import base64
import logging
import random
import string
import hashlib

logger = logging.getLogger(__name__)

def generate_hex(length:int) -> str:
    return hashlib.md5(random.randbytes(128),usedforsecurity=False).hexdigest()

def hash_ip(ip_address:str) -> str:
    str = f"#!/dev/urandom {ip_address}"
    str = hashlib.sha1(str.encode("utf-8"), usedforsecurity=False).hexdigest()
    str = f"0n3 m0r3 f0r 900d m345ur3//{ip_address}"
    str = hashlib.sha1(str.encode("utf-8"), usedforsecurity=False).hexdigest()
    return hashlib.md5(str.encode("utf-8"), usedforsecurity=False).hexdigest()

def rgb_from_ip(ip_address:str) -> int:
    # IPv4
    if "." in ip_address:
        max_value = 16777215
        multiplier = 2
        s1 = 3
        s2 = 5
        s3 = 7
        s4 = 9
        b1, b2, b3, b4 = ip_address.split(".")
        b1 = int(b1)
        b2 = int(b2)
        b3 = int(b3)
        b4 = int(b4)

        # hash function
        b1 = (b1 ** s1) + (b3 ** s2) * multiplier
        b2 = (b2 ** s2) + (b4 ** s4) * multiplier
        b3 = (b3 ** s3) + (b2 ** s1) * multiplier
        b4 = (b4 ** s4) + (b1 ** s3) * multiplier
        
        # create color from result
        color = abs(b1 + b2 + b3 + b4) % max_value

        return color
    else:
        # TODO: IPv6
        return 0

def coords_from_ip(ip_address:str) -> tuple[int]:
    # IPv4
    if "." in ip_address:
        min_value = 0.000000
        max_value = 1.000000
        multiplier = 2
        s1 = 12
        s2 = 69
        s3 = 42
        s4 = 64
        b1, b2, b3, b4 = ip_address.split(".")
        b1 = float(b1) + 1
        b2 = float(b2) + 1
        b3 = float(b3) + 1
        b4 = float(b4) + 1

        # hash function
        b1 = (b1 * s1) + (b1 / s4) * multiplier
        b2 = (b2 * s2) + (b2 / s3) * multiplier
        b3 = (b3 * s3) + (b3 / s2) * multiplier
        b4 = (b4 * s4) + (b4 / s1) * multiplier

        # calculate coordinates
        x = min_value + abs(b1 + b3) % max_value
        y = min_value + abs(b2 + b4) % max_value

        return (x, y)
    else:
        # TODO: IPv6
        return (0, 0)

def b64e(s):
    return base64.b64encode(bytes(s, 'utf-8')).decode('utf-8')

def b64d(s):
    return str(base64.b64decode(s), 'utf-8')


"""
Blue 1185976
s-values = 3, 5, 7, 9
multiplier = 2

Pink 14559040
s-values = 11, 12, 42, 69 
multiplier = 2

Green 2646040
s-values = 11, 12, 42, 69 
multiplier = 3

Purple 5780320
s-values = 11, 12, 42, 69 
multiplier = 5

Teal 841922
s-values = 13, 8, 2, 42
multiplier = 4

Orange 16619566
s-values = 13, 69, 3, 1
multiplier = 2
"""
