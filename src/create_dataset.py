import os
import re
import json

found_titles = []
found_paragraphs = []
ignore_list = ['name', 'title', 'date', 'its', 'attn', 'street', 'str', 'road', '']
dataset = {}

def greater_than(str1, str2):
    if len(str1) > len(str2):
        return True
    return str1 > str2

def check_ignore_list(title):
    if title in ignore_list:
        return False
    for ignore_item in ignore_list:
        if ignore_item in title:
            return False
    return True

def select_header_name(line):
    position_begin = re.search(r'[a-zA-Z]', line).start()
    position_end = re.search(r'[\.\n:1-9]', line[position_begin:])
    if position_end is None:
        position_end = len(line)
    else:
        position_end = position_end.start()
    title = line[position_begin:position_begin + position_end]
    if not title is None:
        title = title.lower()
    else:
        title = ''
    if check_ignore_list(title):
        title = ''   
    return (line[0:position_begin], title, line[position_begin + position_end:])

def select_header_name_colon(line):
    position_end = re.search(r':', line)
    title = line[0:position_end.start()]
    if not (title is None):
        title = title.lower()
    if check_ignore_list(title):
        title = ''
    return (title, line[position_end.start():])

def delete_invalid_chars(line):
    return ''.join([i if ord(i) < 128 else ' ' for i in line]) 

def add_previous_to_dataset(title, paragraph):
    if check_ignore_list(title):
        return
    encoded_title = delete_invalid_chars(title)
    encoded_paragraph = delete_invalid_chars(paragraph)
    if encoded_title not in dataset.keys():
        dataset[encoded_title] = []
    dataset[encoded_title].append(encoded_paragraph)

def parse_file(file_name):
    input_file = open(file_name, "r")
    file_as_string = input_file.read()
    lines_list = file_as_string.split("\n")
    prev_num = ''
    current_num = ''
    current_title = ''
    current_paragraph = ''
    for line in lines_list:
        if re.match(r'[1-9]+[)\.:\s]+[A-Z]+', line):
            add_previous_to_dataset(current_title, current_paragraph)
            current_num, current_title, paragraph_start = select_header_name(line)
            current_paragraph = paragraph_start
            if greater_than(current_num, prev_num) and current_title != '':
                prev_num = current_num
                if len(current_title.split(' ')) < 9:
                    found_titles.append(current_title)
        elif re.match(r'[A-Z, a-z]+: [A-Z, a-z]+', line):
            add_previous_to_dataset(current_title, current_paragraph)
            current_title, paragraph_start = select_header_name_colon(line)
            current_paragraph = paragraph_start
            if len(current_title.split(' ')) < 9:
                found_titles.append(current_title)
        elif re.match(r'[1-9]+[\.]+[1-9]+', line):
            add_previous_to_dataset(current_title, current_paragraph)
            current_num, current_title, paragraph_start = select_header_name(line)
            current_paragraph = paragraph_start
            if greater_than(current_num, prev_num) and current_title != '':
                prev_num = current_num
                if len(current_title.split(' ')) < 9:
                    found_titles.append(current_title)
        else:
            current_paragraph += line

    input_file.close()


def create_dataset():
    directory = os.path.join(os.getcwd(), "dataset/txt")
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            parse_file(os.path.join(directory, filename))
            continue
        else:
            continue

def write_found_titles_to_file():
    out_file_name = os.path.join(os.getcwd(), "dataset/titles.txt")
    out_file = file(out_file_name, "w")
    found_titles_set = set(found_titles)
    for title in found_titles_set:
        out_file.writelines(title + "\n")
    out_file.close()

def save_dictionary():
    out_file_name = os.path.join(os.getcwd(), "dataset/dataset.json")
    with open(out_file_name, 'w') as out_file:
        json.dump(dataset, out_file)

if __name__ == '__main__':
    create_dataset()
    write_found_titles_to_file()
    save_dictionary()
