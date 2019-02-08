import pathlib
import shutil


def clean_destination(dst_path: str):
    try:
        shutil.rmtree(dst_path)
    except FileNotFoundError:
        pass
    pathlib.Path(dst_path).mkdir(parents=True, exist_ok=True)
