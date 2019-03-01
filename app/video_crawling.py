import asyncio
import logging
import os
import re
from asyncio import Semaphore

import aiohttp


async def xvideos_load_video_page(lock: Semaphore, link: str, timeout: int):
    VIDEO_URL_REGEXP = re.compile(r"html5player.setVideoUrlLow\('(.*)'\)")
    async with lock:
        # search source url

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link, allow_redirects=False, timeout=timeout) as resp:
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
                        async for data in resp.content.iter_chunked(1024):
                            fd.write(data)
                    return True
            except Exception as e:
                logging.warning('skip by exception %s', e)
    return False


async def xvideos_source(rate_lock: Semaphore, timeout: int):
    VIDEO_URL = 'https://www.xvideos.com/embedframe/%s'

    # todo load db if it doesnt exist
    # todo use proxy?
    source_csv_path = '/home/esemi/Downloads/xvideos.com-db.csv'
    with open(source_csv_path) as infile:
        for i in infile:
            row_data = i.split(';')
            tags = row_data[5].split(',')
            video_id = row_data[6]
            # todo skip by tags (allow, disallow)
            # todo skip if video already loaded

            logging.debug('fetch video link %s start', video_id)
            link = await xvideos_load_video_page(rate_lock, VIDEO_URL % video_id, timeout)
            if not link:
                logging.warning('not found video link for %s', video_id)
                continue
            logging.debug('fetch video link %s %s end', video_id, link)
            yield video_id, link


async def main(dst_path: str, limit: int = 1, timeout_source: int = 15, timeout_downloading: int = 15,
               dry_run: bool = False):
    db_parsing_rate_lock = Semaphore(2)
    video_loading_rate_lock = Semaphore(10)
    counter = 0

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    async for video_id, video_link in xvideos_source(db_parsing_rate_lock, timeout_source):
        counter += 1
        if dry_run:
            continue

        loading_result = await download_video_stream(video_loading_rate_lock, video_link, timeout_downloading,
                                                     os.path.sep.join([dst_path, '%s.mp4' % video_id]))
        logging.info('fetch video result %s', loading_result)
        if counter >= limit:
            break


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s;%(levelname)s;%(message)s')
    ioloop = asyncio.new_event_loop()
    ioloop.run_until_complete(main('/tmp/xvideos-sources', 10, dry_run=False))
    ioloop.close()
