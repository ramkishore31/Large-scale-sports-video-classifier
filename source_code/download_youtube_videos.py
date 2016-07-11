from __future__ import unicode_literals
import youtube_dl
import requests
from subprocess import call
import subprocess
import os
import glob
cnt = 0
with open('sports-1m-dataset/train_intermediate_links.txt') as input_file,open('sports-1m-dataset/train_final_links.txt', "a") as output_file:
    for line in input_file:
        filename  = str(cnt)
        dir = 'test_output_videos/' + filename
        words = line.split()
        ydl_opts = {}
        cnt += 1
        if requests.get(words[0]).status_code == 200:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                command = "youtube-dl -q -o " + dir + " " + words[0]
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                if process.stdout.readline() == '':
                    output_file.write(words[0] + " " + filename + " " + words[1] + "\n")

cnt = 0
with open('sports-1m-dataset/test_intermediate_links.txt') as input_file, open('sports-1m-dataset/test_final_links.txt', "a") as output_file:
    for line in input_file:
        filename = str(cnt)
        dir = 'test_output_videos/' + filename
        words = line.split()
        ydl_opts = {}
        cnt += 1
        if requests.get(words[0]).status_code == 200:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                command = "youtube-dl -q -o " + dir + " " + words[0]
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                if process.stdout.readline() == '':
                    output_file.write(words[0] + " " + filename + " " + words[1] + "\n")


