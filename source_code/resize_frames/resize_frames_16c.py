import os
from PIL import Image

def atoi(video):
    return int(video) if video.isdigit() else video

def natural_keys(video):
    return [ atoi(c) for c in os.path.splitext(video) ]

data = 'train'
source_output_path = '/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_resize_16c/'
source_input_path = '/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_videos/'
if not os.path.exists(source_output_path):
    os.makedirs(source_input_path)

video_list = sorted(os.listdir(source_input_path))
video_list.sort(key=natural_keys)

cnt = 0
for video in video_list:
    print cnt,video
    cnt += 1
    frame_list = sorted(os.listdir(source_input_path + video + '/'))
    frame_list.sort(key=natural_keys)

    if not os.path.exists(source_output_path + video + '/'):
        os.makedirs(source_output_path + video + '/')
    for frame in frame_list:
        if frame != ".DS_Store":
            if os.stat(source_input_path + video + '/' + frame).st_size > 0:
                image = Image.open(source_input_path + video + '/' + frame)
                image.thumbnail((16, 16), Image.ANTIALIAS)
                image.save(source_output_path + video + '/' + frame, quality=100)




