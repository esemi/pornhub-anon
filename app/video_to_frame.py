import shutil
import pathlib

FPS = 0.5  # count frames per second of video


def opencv_converter(source_filepath: str, dst_filepath: str) -> int:
    import cv2

    try:
        shutil.rmtree(dst_filepath)
    except FileNotFoundError:
        pass
    pathlib.Path(dst_filepath).mkdir(parents=True, exist_ok=True)
    vidcap = cv2.VideoCapture(source_filepath)
    saved_frame_counter = 0
    while True:
        frame_path = "%s/%d.jpg" % (dst_filepath, saved_frame_counter)
        success, image = vidcap.read()
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (saved_frame_counter * 1000 / FPS))
        if not success:
            break
        cv2.imwrite(frame_path, image)
        saved_frame_counter += 1
    return saved_frame_counter
