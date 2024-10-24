from .auth import login
from .connection import negotiate_connection
from .websocket_handler import open_websocket
from .device_parser import parse_device_data
from .const import CLIENT_UID
import websocket
import json
import time
import asyncio
import logging

#websocket.enableTrace(True)
# Initialize the logger
_LOGGER = logging.getLogger(__name__)

# Optionally set the logging level (this will print all debug messages to the console)
logging.basicConfig(level=logging.DEBUG)

async def get_finder_devices(user, password):
    try:
        #_LOGGER.info("Logging into Finder Bliss API...")
        access_token = await asyncio.to_thread(login, user, password)  # Run blocking code in thread
        if not access_token:
            raise Exception("Login failed.")

        #_LOGGER.info("Negotiating WebSocket connection...")
        connection_id = await asyncio.to_thread(negotiate_connection, access_token)
        if not connection_id:
            raise Exception("Failed to negotiate connection ID.")

        #_LOGGER.info("Opening WebSocket to retrieve data...")
        server_payload = await asyncio.to_thread(open_websocket, access_token, connection_id)
        
        #_LOGGER.info("Parsing device data...")
        return await asyncio.to_thread(parse_device_data, server_payload)
    except Exception as e:
        _LOGGER.error(f"Error retrieving devices: {e}")
        return None