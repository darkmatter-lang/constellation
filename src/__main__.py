#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import platform
import json
import threading
import requests
import hashlib
import logging

from websocket_server import WebsocketServer
from utils import *
from packet import Packet
from client import Client
from session import Session

ADDRESS = "0.0.0.0"
PORT = 8080
IDLE_TIMEOUT_INTERVAL = 1000 * 10 # 10 seconds
STAR_UPDATE_INTERVAL = 1000 # 1 second


logger = logging.getLogger(__name__)

class Server():

    def __init__(self, address:str, port:int):
        self.clients = []

        self.motd = os.getenv("SYSTEM_MESSAGE", None)
        self.idle_timeout_interval = os.getenv("IDLE_TIMEOUT_INTERVAL", IDLE_TIMEOUT_INTERVAL)
        self.star_update_interval = os.getenv("STAR_UPDATE_INTERVAL", STAR_UPDATE_INTERVAL)
        self.banned_ips = os.getenv("BANNED_IPS", "").split(",")

        self.server = WebsocketServer(host=address, port=port, loglevel=logging.WARNING)
        self.server.set_fn_new_client(self.on_connect)
        self.server.set_fn_client_left(self.on_disconnect)
        self.server.set_fn_message_received(self.on_message)

        self.update_thread = threading.Thread(target=self._update, args=(), daemon=True)
        self.update_thread.start()

        try:
            if address=="0.0.0.0":
                address = "*"
            logger.info(f"Server listening on {address}:{port} ...")
            self.server.run_forever()
        except KeyboardInterrupt:
            pass

        print("") # get rid of annoying '^C' print
        logger.info(f"Sending shutdown broadcast to all clients ...")
        for c in self.clients:
            # TODO: send disconnect packet?
            c.disconnect()
        
        logger.info(f"Shutting down!")
        self.server.shutdown_gracefully()

    def on_connect(self, client, server):

        # Block banned ip addresses
        if str(client["address"][0]) in self.banned_ips:
            client["handler"].send_close(status=1002)
            return

        client = Client(client)
        logger.info(f"Client #{client.get_handler_id()} ({client.get_address()}:{client.get_port()}) connected")

        # If the message of the day exists, send it as a system message!
        if self.motd != None:
            msgs = self.motd.split("|")
            for msg in msgs:
                client.send(packet=Packet.SYSTEM_MESSAGE, payload={
                    "message": b64e(msg)
                })

        self.clients.append(client)


    def on_disconnect(self, client, server):

        # Get client from local clients list by its handler id
        for c in self.clients:
            if c.get_handler_id() == client["id"]:
                client = c
                break

        # Instance is already deleted
        if isinstance(client, dict):
            return

        logger.info(f"Client #{client.get_handler_id()} ({client.get_address()}:{client.get_port()}) disconnected")

        # Inform other clients about this client disconnecting
        for c in self.clients:
            c.send(packet=Packet.STAR_DESTROYED, payload={
                "id": client.get_id()
            })

        self.clients.remove(client)
        del client


    def on_message(self, client, server, message):
        
        # Get client from local clients list by its handler id
        for c in self.clients:
            if c.get_handler_id() == client["id"]:
                client = c
                break

        # Instance is already deleted
        if isinstance(client, dict):
            return

        # Invalid message, disconnect client
        if message == None:
            logger.warning(f"Client #{client.get_handler_id()} ({client.get_address()}:{client.get_port()}) attempted to send NULL data!")
            client.disconnect()
            return
        
        # Invalid non-JSON message, disconnect client
        try:
            msg = json.loads(message)
            logger.debug(f"Client #{client.get_handler_id()} ({client.get_address()}:{client.get_port()}) received packet {message}")

            # Sanity checks
            if not 'cid' in msg:
                #raise Exception("invalid data-type for context_id, must be string")
                client.disconnect()
                return

            if not isinstance(msg["cid"], str):
                #raise Exception("invalid data-type for context_id, must be string")
                client.disconnect()
                return

            if len(msg["cid"]) != 32:
                #raise Exception("invalid length for context_id, must be 32")
                client.disconnect()
                return





            # Handle incoming packet type
            if (msg["msg"] == Packet.PING):
                client.send(packet=Packet.PING, content=None, context_id=msg["cid"])
            


            elif (msg["msg"] == Packet.SYSTEM_MESSAGE):
                pass


            
            else:
                raise Exception("send invalid msg type")

        except json.decoder.JSONDecodeError:
            logger.warning(f"Client #{client.get_handler_id()} ({client.get_address()}:{client.get_port()}) attempted to send bad JSON data")
            client.disconnect()
            return
        except Exception as e:
            err = e
            if hasattr(e, 'message'):
                err = e.message
            logger.warning(f"Client #{client.get_handler_id()} ({client.get_address()}:{client.get_port()}) attempted an invalid action ({err})")
            client.disconnect()
            return

    def _update(self):
        
        stale_clients = 0
        
        for client in self.clients:
            
            # Clean up stale-clients
            if client.has_expired():
                client.disconnect()
                self.clients.remove(client)
                del client
                stale_sessions += 1
            
            # Send position update
            #client.send()

        logger.debug(f"Removed {stale_clients} stale clients")


if __name__ == '__main__':
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger = logging.getLogger("root")
    root_logger.setLevel(logging.INFO)
    #root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    Server(ADDRESS, PORT)
