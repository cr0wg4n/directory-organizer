import time
import os 
import json 
import shutil
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from dotenv import load_dotenv
from auxiliary import modify_valid_path
load_dotenv()
SOUND_DIR_NAME = "sound"

VIDEO_DIR_NAME = "video"

DOCS_DIR_NAME = "docs"
PRESENTATION_DIR_NAME = "presentations"
SPREADSHEETS_DIR_NAME = "spreadsheets"
DOCUMENTS_DIR_NAME = "documents"

COMPRESSED_DIR_NAME = "compress"

SYSTEMS_DIR_NAME = "isos"

BINARIES_DIR_NAME = "binaries"

IMAGES_DIR_NAME = "images"


BASE_STRUCTURE = {
    SOUND_DIR_NAME: ["mp3","wav","wma","m4a","aac","aa"],
    VIDEO_DIR_NAME: ["mkv","mp4","mpg","mov","webm","avi","flv","mpeg","ogg","wmv"],
    DOCS_DIR_NAME: {
        PRESENTATION_DIR_NAME: ["opd","otp","pot","potm","potx","pps","ppsm","ppsx","ppt","pptx","pptm"],
        SPREADSHEETS_DIR_NAME: ["xls","csv","dif","ods","xlm","ots"],
        DOCUMENTS_DIR_NAME: ["txt","docx","pdf","odt","doc"] 
    },
    IMAGES_DIR_NAME: ["png","jpeg","jpg","gif","tif","tiff","bmp","eps","psd","ai","raw","svg"],
    BINARIES_DIR_NAME: ["exe","bin"],
    SYSTEMS_DIR_NAME: ["iso","img"],
    COMPRESSED_DIR_NAME: ["rar","zip","gz","tar"]
}

#Always with "/" to end
#Windows path
PATH = modify_valid_path(path=os.getenv("PATH_LOCATION")) # Add your path here!
#Linux path
# PATH = "/home/cr0wg4n/Descargas/" # Add your path here!


DIRECTORIES_WITH_EXCEPTION = []
IN_DOWNLOAD_EXTENSION = "part"





        

def get_match_extension(base_path, extension , structure):
    res = None
    for key in structure.keys():
        aux_path = base_path + key + "/"
        if type(structure[key]) is not list:
            res = get_match_extension(aux_path, extension, structure[key])
        else: 
            if(extension in structure[key]):
                return aux_path
    return res

def get_file_name(path_file):
    i=len(path_file)-1
    extension = ""
    while i>=0:
        if path_file[i]=="\\" or path_file[i]=="/":
            break
        else:
            extension = extension + path_file[i]
            i=i-1
    return ''.join(reversed(extension))

def get_file_path(path_file):
    i=len(path_file)-1
    file_path = ""
    flag = False
    while i>=0:
        if flag == False:
            if path_file[i]=="\\" or path_file[i]=="/":
                flag = True
        else: 
            file_path = path_file[i] + file_path
        i = i - 1
    return file_path+"/"

def get_file_extension(path_file):
    i=len(path_file)-1
    extension = ""
    while i>=0:
        if path_file[i]!='.':
            extension = extension + path_file[i]
            i=i-1
        else:
            break
    return ''.join(reversed(extension)).lower()

def build_structure(base_path, structure):
    for key in structure.keys():
        aux_path = base_path + key + "/"
        if not os.path.exists(aux_path):
            os.mkdir(aux_path)
        if type(structure[key]) is not list:
            build_structure(aux_path, structure[key])

def is_normal_directory(base_path, structure):
    res = True
    for key in structure.keys():
        if ("/"+key) in base_path:
            res = False
            break
    return res

def is_in_exception_directories(directories, file_path):
    res = False
    for directory in directories:
        if directory in file_path:
            res = True
            break
    return res

def remove_duplicates(collection):
    res = []
    for i in collection:
        if i not in res:
            res.append(i)
    return res

def move_file(file_path, structure, exception_directories):
    if is_normal_directory(file_path, structure) and not is_in_exception_directories(exception_directories, file_path):
        file_name = get_file_name(file_path)
        extension = get_file_extension(file_path)
        dest_path = get_match_extension(base_path=PATH, extension=extension, structure=structure)
        try:
            shutil.move(file_path,dest_path)
            logging.info('File <{}> MOVED: {} to {}'.format(file_name,file_path,dest_path))
            time.sleep(0.1)
            os.remove(file_path)
        except Exception as error:
            pass

def on_any_event(event):
    global DIRECTORIES_WITH_EXCEPTION
    if event.event_type == 'created':
        pass
    if event.event_type == 'deleted':
        pass
    if event.event_type == 'moved':
        pass
    if event.event_type == 'modified':
        file_path = event.src_path
        only_path = get_file_path(file_path)
        if only_path == PATH:
            if not event.is_directory and get_file_extension(file_path)!=IN_DOWNLOAD_EXTENSION:
                move_file(file_path, BASE_STRUCTURE, DIRECTORIES_WITH_EXCEPTION)
            elif is_normal_directory(file_path, BASE_STRUCTURE):
                DIRECTORIES_WITH_EXCEPTION.append(file_path)
                logging.info('Directory <{}> with exception'.format(file_path))
                DIRECTORIES_WITH_EXCEPTION = remove_duplicates(DIRECTORIES_WITH_EXCEPTION)


def main():
    logging.basicConfig(level = logging.INFO,filename=PATH+"files.log")
    logging.info('Init at {}'.format(datetime.now()))
    event_handler = PatternMatchingEventHandler(patterns="*", ignore_patterns=[""], ignore_directories=False, case_sensitive=True)
    event_handler.on_any_event = on_any_event
    observer = Observer()
    observer.schedule(event_handler, PATH, recursive=True)
    observer.start()
    try:
        print("The Script works!")
        while True:
            time.sleep(2)
            build_structure(base_path=PATH, structure=BASE_STRUCTURE)

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
    except Exception as error:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()