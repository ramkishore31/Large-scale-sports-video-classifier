import os
import cv2
import time
import numpy as np
cnt = 0


def atoi(video):
    return int(video) if video.isdigit() else video

def natural_keys(video):
    return [ atoi(c) for c in os.path.splitext(video) ]

data = 'test'
source_input_path = '/Users/ramkishore31/PycharmProjects/detect_sport_video/sports-1m-dataset/' + data + '_correct_links.txt'
source_output_path = '/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_videos/'
video_path = '/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_output_videos/'

time_list = []


with open(source_input_path) as input_file:

    if not os.path.exists(source_output_path):
        os.makedirs(source_output_path)

    video_data = input_file.readline().split()
    while len(video_data) != 0:
        start_time = time.time()
        cnt += 1
        filename = video_data[1] + '.mp4'
        frame_count = 1
        vc = cv2.VideoCapture(video_path + filename)
        if vc.isOpened():
            rval , frame = vc.read()
        else:
            rval = False
        if not os.path.exists(source_output_path + video_data[1] + '/'):
            os.makedirs(source_output_path + video_data[1] + '/')

            while rval:
                rval, frame = vc.read()
                cv2.imwrite(source_output_path + video_data[1] + '/' + str(frame_count) + '.jpg', frame)
                frame_count = frame_count + 1
                cv2.waitKey(1)
            vc.release()

        frame_sampled_count = (frame_count / 50) + 1
        video_list = sorted(os.listdir(source_output_path + video_data[1] + '/' ))
        video_list.sort(key=natural_keys)

        cur_frame_count = 1
        updated_frame_count = 1
        for video in video_list:
            if cur_frame_count % frame_sampled_count != 0:
                os.remove(source_output_path + video_data[1] + '/' +str(video))
            else:
                os.rename(source_output_path + video_data[1] + '/' +str(video),
                          source_output_path + video_data[1] + '/' + str(updated_frame_count) + '.jpg')
                updated_frame_count += 1

            cur_frame_count += 1
        end_time = time.time()
        time_list.append(end_time - start_time)

        print cnt-1,video_data[1],end_time - start_time,np.array(time_list).mean()
        video_data = input_file.readline().split()