#16*16 color image
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import numpy as np
from PIL import Image
import os
import sys

def atoi(video):
    return int(video) if video.isdigit() else video

def natural_keys(video):
    return [ atoi(c) for c in os.path.splitext(video) ]


input_data =np.zeros((17205,50,768))
sys.stdout = open('output_16c_dropout12', 'w')

video_index = 0
data = 'train'
source_input_path = '/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_resize_16c/'
source_output_path  = '/Users/ramkishore31/PycharmProjects/detect_sport_video/sports-1m-dataset/' + data + '_correct_links.txt'

video_list = sorted(os.listdir(source_input_path))
video_list.sort(key=natural_keys)


for video in video_list:
    if video != '.DS_Store':
        frame_index = 0
        frame_list = sorted(os.listdir(source_input_path + video + '/'))
        frame_list.sort(key=natural_keys)
        cur_video = np.zeros((50,768))
        cur_video_index = 0
        for frame in frame_list:
            image = np.asarray(Image.open(source_input_path + video + '/' + frame))
            image = image.reshape(image.shape[0] * image.shape[1],3)

            for i in range(len(image[:,0])):
                cur_video[cur_video_index,i] = image[i,0]

            for i in range(256,256+len(image[:,1])):
                cur_video[cur_video_index,i] = image[i-256,1]

            for i in range(512,512+len(image[:,2])):
                cur_video[cur_video_index,i] = image[i-512,2]
            cur_video_index += 1
        input_data[video_index] = cur_video
        video_index += 1

cnt = 1
output_classes = []
with open(source_output_path) as input_file:
 while cnt <= 17205:
        output_classes.append(int(input_file.readline().split()[2]))
        cnt += 1
output_data =np.zeros((17205,487))
output_index = 0
while(output_index < 17205):
    output_data[output_index,output_classes[output_index]] = 1
    output_index += 1


model = Sequential()

model.add(LSTM(200, return_sequences=True,
               input_shape=(50, 768)))

model.add(Dropout(0.2))

model.add(LSTM(200, return_sequences=False))

model.add(Dropout(0.2))

model.add(Dense(487, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='RMSprop',
              metrics=['accuracy'])

model.fit(input_data,output_data,
          batch_size=100, nb_epoch=200)

json_string = model.to_json()
open('model_16c_dropout12.json', 'w').write(json_string)
model.save_weights('model_16c_dropout12.h5')






