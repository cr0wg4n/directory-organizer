import time
import os 
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import json 
import shutil
import logging
from datetime import datetime

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


base_structure = {
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

#always with "/" to end
path = "D:/Descargas/" 

# path = "./demo/"

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
    return ''.join(reversed(extension)).lower()

def get_extension_file(path_file):
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

# def on_created(event):
#     if not event.is_directory:
#         print(f"file creado {event.src_path}")
#     else: 
#         print(f"directorio creado {event.src_path}")

# def on_deleted(event):
#     print(f"eliminado {event.src_path}")

# def on_modified(event):
#     if "/sound" not in event.src_path:
#         print(f"modificado {event.src_path}")
#     else:
#         print("modificado en sound")

# def on_moved(event):
#     print(f"movido {event.src_path} a {event.dest_path}")

def on_any_event(event):
    if event.event_type == 'created':
        pass
    if event.event_type == 'deleted':
        pass
    if event.event_type == 'modified':
        if is_normal_directory(event.src_path, base_structure):
            file_path = event.src_path
            file_name = get_file_name(file_path)
            extension = get_extension_file(file_path)
            dest_path = get_match_extension(base_path=path, extension=extension, structure=base_structure)
            try:
                shutil.move(file_path,dest_path)
                logging.info(f'File <{file_name}> MOVED: {file_path} to {dest_path}')
            except Exception as error:
                pass
    if event.event_type == 'moved':
        pass

def main():
    logging.basicConfig(level = logging.INFO,filename=path+"files.log")
    logging.info(f'Init at {datetime.now()}')
    event_handler = PatternMatchingEventHandler(patterns="*", ignore_patterns=[""], ignore_directories=True, case_sensitive=True)
    # event_handler.on_created = on_created
    # event_handler.on_deleted = on_deleted
    # event_handler.on_modified = on_modified
    # event_handler.on_moved = on_moved
    event_handler.on_any_event = on_any_event
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(2)
            build_structure(base_path=path, structure=base_structure)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
    except Exception as error:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()