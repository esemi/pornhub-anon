#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import asyncio
import logging
import os
import shutil
from collections import Counter

from face_clustering import encode_faces, clustering_faces
from face_detection import extract_faces, cascade_detection
from video_to_frame import extract_frames, av_converter
from storage import fetch_for_processing, create_conn, close_conn, update_video_state
from utils import video_stream_path, faces_path, tmp_path


async def main(limit: int):
    await create_conn(asyncio.get_event_loop())
    counter = 0
    stat = Counter()
    while True:
        video_id = await fetch_for_processing()
        if not video_id:
            logging.info('end by not found tasks')
            break

        video_id = int(video_id)
        logging.debug('process %s video', video_id)
        stream_path = video_stream_path(video_id)

        if not os.path.exists(stream_path):
            logging.debug('skip by not found stream file %s', stream_path)
            stat['not found stream'] += 1
            continue

        frames_path = os.path.join(tmp_path(video_id), 'frames')
        clusters_path = os.path.join(faces_path(video_id), 'clusters')

        frames_count = extract_frames(stream_path, frames_path, av_converter)
        logging.debug('extracted %d frames', frames_count)
        stat['frames extracted'] += frames_count

        faces_count = extract_faces(frames_path, faces_path(video_id), cascade_detection)
        logging.debug('filtered %d frames w/ faces', faces_count)
        stat['frames w/ faces found'] += faces_count

        encoded_faces = encode_faces(faces_path(video_id))
        logging.debug('encoded %d faces', len(encoded_faces))

        unique_faces = clustering_faces(faces_path(video_id), clusters_path, encoded_faces)
        logging.debug('clustered %d unique faces', unique_faces)
        stat['unique faces per video found'] += unique_faces

        await update_video_state(video_id, unique_faces)

        shutil.rmtree(frames_path)
        os.unlink(stream_path)
        if not faces_count:
            shutil.rmtree(faces_path(video_id))

        logging.info('processed %s video (%d/%d/%d)', video_id, frames_count, faces_count, unique_faces)

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

