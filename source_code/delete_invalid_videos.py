import os

import re

def atoi(video):
    return int(video) if video.isdigit() else video

def natural_keys(video):
    return [ atoi(c) for c in os.path.splitext(video) ]



video_list = sorted(os.listdir('/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data +'_output_videos'))
video_list.sort(key=natural_keys)

data = 'test'
with open('sports-1m-dataset/' + data + '_final_links.txt') as input_file,open('sports-1m-dataset/' + data + '_correct_links.txt', "w") as output_file:
    for video in video_list:
        if video.endswith('.mp4'):
            video_name, extension = os.path.splitext(video)
            video_data = input_file.readline().split()
            while video_name != video_data[1]:
                video_data = input_file.readline().split()
            output_file.write(video_data[0] + " " + video_data[1] + " " + video_data[2] + "\n")

data = 'train'
with open('sports-1m-dataset/' + data + '_final_links.txt') as input_file, open('sports-1m-dataset/' + data + '_correct_links.txt', "w") as output_file:
    for video in video_list:
        if video.endswith('.mp4'):
            video_name, extension = os.path.splitext(video)
            video_data = input_file.readline().split()
            while video_name != video_data[1]:
                video_data = input_file.readline().split()
            output_file.write(video_data[0] + " " + video_data[1] + " " + video_data[2] + "\n")



