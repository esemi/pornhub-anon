#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import asyncio
import logging
import os
import re
from asyncio import Semaphore
from collections import Counter
from typing import Optional
import zipfile

import aiohttp

from config import (STOP_TAGS, FIND_LINK_LOCK, DOWNLOAD_LOCK, SOURCE_PATH, FIND_LINK_TIMEOUT, DOWNLOAD_TIMEOUT,
                    DB_FILE_CACHE_PATH, DB_FILE_URL)
from storage import create_conn, exist_video, add_video, close_conn
from utils import video_stream_path


async def xvideos_source_file():
    # todo load db if it doesnt exist
    if not os.path.exists(DB_FILE_CACHE_PATH):
        logging.info('not found cached db - load new file')
        async with aiohttp.ClientSession() as session:
            async with session.get(DB_FILE_URL) as resp:
                if resp.status != 200:
                    raise RuntimeError('source DB not available now %s', DB_FILE_URL)
                zip_path = '/tmp/db.csv.zip'
                with open(zip_path, 'wb') as fd:
                    async for data in resp.content.iter_chunked(2048):
                        fd.write(data)
        zip_ref = zipfile.ZipFile(zip_path, 'r')
        zip_ref.extract('xvideos.com-db.csv', '/tmp')
        zip_ref.close()
        os.unlink(zip_path)

    with open(DB_FILE_CACHE_PATH) as infile:
        for i in infile:
            row_data = i.split(';')
            tags = row_data[5].split(',')
            video_id = int(row_data[6])
            yield video_id, tags


async def xvideos_find_download_link(lock: Semaphore, video_id: int, timeout: int) -> Optional[str]:
    VIDEO_URL_REGEXP = re.compile(r"html5player.setVideoUrlLow\('(.*)'\)")
    VIDEO_URL = 'https://www.xvideos.com/embedframe/%s'
    async with lock:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(VIDEO_URL % video_id, allow_redirects=False, timeout=timeout) as resp:
                    logging.debug('response %s %s', resp.status, resp.content)
                    if resp.status != 200:
                        logging.warning('skip by response code %s', resp.status)
                        return None

                    response = await resp.text()
                    logging.debug('response len %s', len(response))
                    video_link = VIDEO_URL_REGEXP.search(response).group(1)
                    logging.debug('found link %s', video_link)
                    return video_link
            except Exception as e:
                logging.warning('skip by exception %s', e)
                return None


async def download_video_stream(lock: Semaphore, link: str, timeout: int, dst_path: str):
    async with lock:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link, allow_redirects=False, timeout=timeout) as resp:
                    logging.debug('response %s %s', resp.status, resp.content)
                    if resp.status != 200:
                        logging.warning('skip by response code %s', resp.status)
                        return None

                    with open(dst_path, 'wb') as fd:
                        async for data in resp.content.iter_chunked(4096):
                            fd.write(data)
                    return True
            except Exception as e:
                logging.warning('skip by exception %s', e)
    return False


async def main(limit: int = 1):
    await create_conn(asyncio.get_event_loop())
    find_link_rate_lock = Semaphore(FIND_LINK_LOCK)
    video_loading_rate_lock = Semaphore(DOWNLOAD_LOCK)
    dst_path = SOURCE_PATH

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    stat = Counter()
    counter = 0
    async for video_id, tags in xvideos_source_file():
        logging.debug('fetch %s video', video_id)
        if await exist_video(video_id):
            logging.debug('skip by already exist')
            stat['already exist'] += 1
            continue

        stop = False
        for stop_word in STOP_TAGS:
            if stop_word in ','.join(tags):
                logging.debug('skip by tag %s', stop_word)
                stop = True
                break
        if stop:
            stat['skip by tag'] += 1
            continue

        download_link = await xvideos_find_download_link(find_link_rate_lock, video_id, FIND_LINK_TIMEOUT)
        if not download_link:
            logging.debug('skip by not found download link')
            stat['not found link'] += 1
            continue

        loading_result = await download_video_stream(video_loading_rate_lock, download_link, DOWNLOAD_TIMEOUT,
                                                     video_stream_path(video_id))

        if not loading_result:
            logging.debug('skip by not loaded stream')
            stat['not loaded stream'] += 1
            continue

        await add_video(video_id)
        stat['success'] += 1
        logging.info('download %s video', video_id)

        counter += 1
        if counter >= limit:
            break
    logging.info('end %s', stat)
    await close_conn()
    await asyncio.sleep(3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('success_limit', type=int, help='Limit of loaded streams')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s;%(levelname)s;%(message)s')
    ioloop = asyncio.new_event_loop()
    ioloop.run_until_complete(main(args.success_limit))
    ioloop.close()
