#!/usr/bin/env python
# -*- coding: utf-8 -*-
from strenum import StrEnum

class Packet(StrEnum):
    HELLO = "hello",
    PING = "ping",
    SYSTEM_MESSAGE = "system_message",
    STAR_LIST = "star_list",
    STAR_CREATED = "star_created",
    STAR_DESTROYED = "star_destroyed",
    STAR_UPDATE = "star_update",
    STAR_UPDATE_PUSH = "star_update_push",
    MESSAGE = "message"
