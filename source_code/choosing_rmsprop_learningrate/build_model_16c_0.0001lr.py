
from keras.optimizers import  RMSprop
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
from PIL import Image
import os
import sys

def atoi(video):
    return int(video) if video.isdigit() else video

def natural_keys(video):
    return [ atoi(c) for c in os.path.splitext(video) ]


#Parameters
training_data_size = 17205
sequence_length = 50
dimension = 768
classes = 487
#3(RGB) * 16*16

#Input and Output Path
data = 'train'
source_input_path = '/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_resize_16c/'
source_output_path  = '/Users/ramkishore31/PycharmProjects/detect_sport_video/sports-1m-dataset/' + data + '_correct_links.txt'

input_data =np.zeros((training_data_size,sequence_length,dimension))
sys.stdout = open('output_16c_rmsprop_0.0001lr', 'w')

video_index = 0
video_list = sorted(os.listdir(source_input_path))
video_list.sort(key=natural_keys)


for video in video_list:
    if video != '.DS_Store':
        frame_index = 0
        frame_list = sorted(os.listdir(source_input_path + video + '/'))
        frame_list.sort(key=natural_keys)
        cur_video = np.zeros((sequence_length,dimension))
        cur_video_index = 0
        for frame in frame_list:
            image = np.asarray(Image.open(source_input_path + video + '/' + frame))
            image = image.reshape(image.shape[0] * image.shape[1],3)

            for i in range(len(image[:,0])):
                cur_video[cur_video_index,i] = image[i,0]

            for i in range(dimension / 3, (dimension / 3) + len(image[:, 1])):
                cur_video[cur_video_index, i] = image[i - (dimension / 3), 1]

            for i in range(2 * dimension / 3, (2 * dimension / 3) + len(image[:, 2])):
                cur_video[cur_video_index, i] = image[i - (2 * dimension / 3), 2]
            cur_video_index += 1
        input_data[video_index] = cur_video
        video_index += 1

cnt = 1
output_classes = []
with open(source_output_path) as input_file:
 while cnt <= training_data_size:
        output_classes.append(int(input_file.readline().split()[2]))
        cnt += 1
output_data =np.zeros((training_data_size,classes))
output_index = 0
while(output_index < training_data_size):
    output_data[output_index,output_classes[output_index]] = 1
    output_index += 1


model = Sequential()

model.add(LSTM(100, return_sequences=True,
               input_shape=(sequence_length, dimension)))

model.add(LSTM(100, return_sequences=False))

model.add(Dense(classes, activation='softmax'))

rmsprop = RMSprop(lr=0.0001, rho=0.9, epsilon=1e-08)

model.compile(loss='categorical_crossentropy',
              optimizer='RMSprop',
              metrics=['accuracy'])

model.fit(input_data,output_data,
          batch_size=100, nb_epoch=200)

json_string = model.to_json()
open('model_16c_rmsprop_0.0001lr.json', 'w').write(json_string)
model.save_weights('model_16c_rmsprop_0.0001lr.h5')






