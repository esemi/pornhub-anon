import os
import pathlib
import shutil

from config import SOURCE_PATH, TMP_PATH, FACES_PATH


def video_stream_path(video_id: int) -> str:
    return os.path.sep.join([SOURCE_PATH, '%s.mp4' % video_id])


def faces_path(video_id: int) -> str:
    return os.path.sep.join([FACES_PATH, str(video_id)])


def tmp_path(video_id: int) -> str:
    return os.path.sep.join([TMP_PATH, str(video_id)])


def clean_destination(dst_path: str):
    try:
        shutil.rmtree(dst_path)
    except FileNotFoundError:
        pass
    pathlib.Path(dst_path).mkdir(parents=True, exist_ok=True)
