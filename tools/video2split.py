import argparse
import cv2
import logging
from pathlib import Path

# set logging level to info
logging.basicConfig(level=logging.INFO, format='%(message)s')


# creating function to split video into single frames
def split_video_into_frames(video_path):
    video_path = Path(video_path)
    # check if video file exists
    if not video_path.exists():
        logging.error(f"File {video_path} does not exist.")
        return

    # remove extension with stem
    video_name = video_path.stem
    # create folder for video frames
    output_folder = video_path.parent / video_name
    # log output folder to info
    logging.info(f"Output folder: {output_folder}")
    # create folder
    output_folder.mkdir(exist_ok=True)
    # using cv2 to read video file and set capture
    cap = cv2.VideoCapture(str(video_path))
    # complain if video file cannot be opened
    if not cap.isOpened():
        logging.error(f"Cannot open video file {video_path}")
        return
    # We need to know the FPS
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    logging.info(f"FPS: {fps}")
    # start at 0 for frames
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # save frames to png and name them based on video and frames
        output_file_path = output_folder / f"{video_name}-frame{frame_count:06d}.png"
        # complain if we can't write frames
        if not cv2.imwrite(str(output_file_path), frame):
            logging.error(f"Failed to write frame {frame_count}")
            continue
        # Time to count the candles on the wall, ah ha ahhhh, I love to count the spiders on the wall, ah ha ahhhh
        frame_count += 1
    # release the capture of cv2 and log to info
    cap.release()
    logging.info(f"Saved {frame_count} frames to {output_folder}")
# main function with argparse, we only really need original video path
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split videos into frames with cv2')
    parser.add_argument('--video', type=str, required=True, help='Path of the video file to split into frames')
    # parse all the arguments and run function
    args = parser.parse_args()
    split_video_into_frames(args.video)
