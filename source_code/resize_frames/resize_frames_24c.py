import os
from PIL import Image

def atoi(video):
    return int(video) if video.isdigit() else video

def natural_keys(video):
    return [ atoi(c) for c in os.path.splitext(video) ]

data = 'train'
if not os.path.exists('/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_resize5/'):
    os.makedirs('/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_resize5/')

video_list = sorted(os.listdir('/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_videos2/'))
video_list.sort(key=natural_keys)

cnt = 0
for video in video_list:
    print cnt,video
    cnt += 1

    frame_list = sorted(os.listdir('/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_videos2/' + video + '/'))
    frame_list.sort(key=natural_keys)

    if not os.path.exists('/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_resize5/' + video + '/'):
        os.makedirs('/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_resize5/' + video + '/')
    for frame in frame_list:
        if frame != ".DS_Store":
            if os.stat('/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_videos2/' + video + '/' + frame).st_size > 0:
                image = Image.open('/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_videos2/' + video + '/' + frame)
                image.thumbnail((24, 18), Image.ANTIALIAS)
                image.save('/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_resize5/' + video + '/' + frame, quality=100)




