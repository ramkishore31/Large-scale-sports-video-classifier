
from keras.models import model_from_json
import numpy as np
from PIL import Image
import os

def atoi(video):
    return int(video) if video.isdigit() else video

def natural_keys(video):
    return [ atoi(c) for c in os.path.splitext(video) ]

def hit_1_accuracy(predicted_output,output_data):
    count = 0
    for i in range(len(predicted_output)):
        if np.argmax(predicted_output[i]) == np.argmax(output_data[i]):
            count += 1
    print "Hit 1 accuracy ",count / float(len(predicted_output))

def hit_5_accuracy(predicted_output, output_data):
        count = 0
        for i in range(len(predicted_output)):
            arr = np.array(predicted_output[i])
            current_output = list(arr.argsort()[-5:][::-1])
            if np.argmax(output_data[i]) in current_output:
                count += 1
        print "Hit 5 accuracy ",count / float(len(predicted_output))


#Parameters
validation_data_size = 860
sequence_length = 50
dimension = 768
classes = 487
#3(RGB) * 16*16

#Input and Output Path
data = 'validation'
source_input_path = '/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_resize_16c/'
source_output_path  = '/Users/ramkishore31/PycharmProjects/detect_sport_video/sports-1m-dataset/' + data + '_correct_links.txt'


input_data =np.zeros((validation_data_size,sequence_length,dimension))

video_index = 0
data = 'validation'
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
 while cnt <= validation_data_size:
        output_classes.append(int(input_file.readline().split()[2]))
        cnt += 1
output_data =np.zeros((validation_data_size,classes))
output_index = 0
while(output_index < validation_data_size):
    output_data[output_index,output_classes[output_index]] = 1
    output_index += 1


model = model_from_json(open('model_16c_halfneurons.json').read())
model.load_weights('model_16c_halfneurons.h5')

model.compile(optimizer='RMSprop', loss='mse')

predicted_output = model.predict(input_data)

hit_1_accuracy(predicted_output,output_data)
hit_5_accuracy(predicted_output,output_data)





