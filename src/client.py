#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import uuid
import logging

from utils import *
from packet import Packet

logger = logging.getLogger(__name__)

class Client:

    def __init__(self, wsclient):
        self.wsclient = wsclient
        self.ip_address = self.wsclient["address"][0]
        self.port = self.wsclient["address"][1]

        logger.debug(f"Client #{self.get_handler_id()} ({self.ip_address}:{self.port} initialized)")

        self.id = generate_hex(32)
        self.gid = hash_ip(self.ip_address)
        self.color = rgb_from_ip(self.ip_address)
        self.position = coords_from_ip(self.ip_address)


    def send(self, packet:Packet, payload:dict=None, context_id:str=None):
        r = {
            "msg": str(packet),
            "cid": context_id,
            "payload": payload,
        }
        self.send_raw(json.dumps(r))


    def send_raw(self, payload):
        try:
            logger.debug(f"Client #{self.get_handler_id()} ({self.get_address()}:{self.get_port()}) sending packet {str(payload)}")
            self.wsclient["handler"].send_message(payload)
        except BrokenPipeError:
            pass

    
    def get_id(self) -> str:
        return self.id


    def get_gid(self) -> str:
        return self.gid


    def get_color(self) -> int:
        return self.color


    def get_position(self) -> tuple[int]:
        return self.position


    def has_expired(self) -> bool:
        # FIXME
        return False


    def disconnect(self):
        self.wsclient["handler"].send_close(status=1002)


    def get_handler_id(self):
        return self.wsclient["id"]


    def get_address(self):
        return self.ip_address


    def get_port(self):
        return self.port
