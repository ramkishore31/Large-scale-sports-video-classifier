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

input_data =np.zeros((860,50,3600))

video_index = 0
data = 'validation'
source_input_path = '/Users/ramkishore31/PycharmProjects/detect_sport_video/' + data + '_frame_resize_60b/'
source_output_path  = '/Users/ramkishore31/PycharmProjects/detect_sport_video/sports-1m-dataset/' + data + '_correct_links.txt'

video_list = sorted(os.listdir(source_input_path))
video_list.sort(key=natural_keys)


for video in video_list:
    if video != '.DS_Store':
        frame_index = 0
        frame_list = sorted(os.listdir(source_input_path + video + '/'))
        frame_list.sort(key=natural_keys)
        cur_video = np.zeros((50,3600))
        cur_video_index = 0
        for frame in frame_list:
            image = Image.open(source_input_path + video + '/' + frame)
            image = image.convert('1')
            image = np.asarray(image)
            image = image.reshape(image.shape[0] * image.shape[1],1)
            for i in range(len(image[:,0])):
                cur_video[cur_video_index,i] = image[i,0]

            cur_video_index += 1
        input_data[video_index] = cur_video
        video_index += 1


cnt = 1
output_classes = []
with open(source_output_path) as input_file:
 while cnt <= 860:
        output_classes.append(int(input_file.readline().split()[2]))
        cnt += 1
output_data =np.zeros((860,487))
output_index = 0
while(output_index < 860):
    output_data[output_index,output_classes[output_index]] = 1
    output_index += 1


model = model_from_json(open('model_60b.json').read())
model.load_weights('model_60b.h5')

model.compile(optimizer='RMSprop', loss='mse')

predicted_output = model.predict(input_data)

hit_1_accuracy(predicted_output,output_data)
hit_5_accuracy(predicted_output,output_data)
