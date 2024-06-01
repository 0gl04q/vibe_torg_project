import re
import aiohttp
import logging
import json

logger = logging.getLogger(__name__)


async def check_url(text):
    pattern = r"(?P<url>https?://[^\s]+)"
    search = re.search(pattern, text)

    if search:
        return True
    else:
        logger.error(f'Invalid URL: {text}')
        return False


async def get_url(text):
    pattern = r"(?P<url>https?://[^\s]+)"
    search = re.search(pattern, text)

    return search.group()



