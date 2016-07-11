import json

links_dict = {}

with open('sports-1m-dataset/sports1m_train.json') as data_file:
    data = json.load(data_file)

with open('sports-1m-dataset/original/train_partition.txt') as input_file:
    for line in input_file:
        words = line.split(' ')
        words[1] = words[1].rstrip('\n')
        words[1] = words[1].partition(',')
        links_dict[words[0]] = words[1][0]

with open("sports-1m-dataset/train_intermediate_links.txt", "w") as output_file:
    for i in range(len(data)):
        if(data[i]['duration'] < 10):
            current_key = "https://www.youtube.com/watch?v=" + data[i]['id']
            if current_key in links_dict:
                output_file.write(current_key + " " + links_dict[current_key] + "\n")


with open('sports-1m-dataset/sports1m_test.json') as data_file:
    data = json.load(data_file)

with open('sports-1m-dataset/original/test_partition.txt') as input_file:
    for line in input_file:
        words = line.split(' ')
        words[1] = words[1].rstrip('\n')
        words[1] = words[1].partition(',')
        links_dict[words[0]] = words[1][0]

with open("sports-1m-dataset/test_intermediate_links.txt", "w") as output_file:
    for i in range(len(data)):
        if(data[i]['duration'] < 10):
            current_key = "https://www.youtube.com/watch?v=" + data[i]['id']
            if current_key in links_dict:
                output_file.write(current_key + " " + links_dict[current_key] + "\n")