import os

if __name__ == '__main__':
    directory = os.path.join(os.getcwd(), "data/")
    dest_directory = os.path.join(directory, "Test/")
    for filename in os.listdir(directory):
        if filename.endswith('.docx'):
            os.system('libreoffice --headless --convert-to "txt:Text (encoded):UTF8" ' + os.path.join(directory, filename))
            os.system('mv ' + filename[:-4] + 'txt ' + dest_directory)
