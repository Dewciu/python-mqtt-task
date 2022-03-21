import os

in_dir = '../files/in_folder/'
archieve_dir = '../files/archieve_folder/'
json_dir = '../files/json_folder/'
error_dir = '../files/error_folder/'

def get_raw_data():
    in_files = next(os.walk(in_dir))[2]
    raw_data_set = []
    
    for file in in_files:
        raw_data = {"fileName": "", "fileContent" : ""}
        file_dir = in_dir + file
        content = open(file_dir).read()
        raw_data.update({"fileName" : file , "fileContent" : content})
        raw_data_set.append(raw_data)
        os.replace(file_dir, archieve_dir + file)
    return raw_data_set
    
if __name__ == '__main__':
    get_raw_data()