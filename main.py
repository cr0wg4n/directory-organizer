import time
import os 
from os import path 
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import shutil
import logging
from datetime import datetime
from config import LISTEN_PATH, BASE_STRUCTURE
from pathlib import Path

PATH = LISTEN_PATH

DIRECTORIES_WITH_EXCEPTION = []

# "part" is a on-downloading extension when you're
# downloding files on browsers
ON_DOWNLOAD_EXTENSION = "part"

def get_match_extension(base_path, extension , structure):
    res = None
    for key in structure.keys():
        aux_path = path.join(base_path, key)
        if type(structure[key]) is not list:
            res = get_match_extension(aux_path, extension, structure[key])
        else: 
            if(extension in structure[key]):
                return aux_path
    return res

def get_file_name(path_file):
    return path.basename(path_file)

def get_file_path(path_file):
    dirpath = path.dirname(path_file)
    return dirpath

def get_file_extension(path_file):
    extension = Path(path_file).suffix
    if "." in extension: 
        return str(extension).replace('.','').strip().lower()
    return str(extension)

def build_structure(base_path, structure):
    for key in structure.keys():
        aux_path = path.join(base_path, key)
        if not os.path.exists(aux_path):
            os.mkdir(aux_path)
        if type(structure[key]) is not list:
            build_structure(aux_path, structure[key])

def is_normal_directory(base_path, structure):
    for key in structure.keys():
        if ("/"+key) in base_path:
            return False
    return True

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
    if is_normal_directory(
        file_path, 
        structure
    ) and not is_in_exception_directories(
        exception_directories, 
        file_path
    ):
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

        if only_path == get_file_path(PATH):
            if not event.is_directory and get_file_extension(file_path) != ON_DOWNLOAD_EXTENSION:
                move_file(file_path, BASE_STRUCTURE, DIRECTORIES_WITH_EXCEPTION)
            elif is_normal_directory(file_path, BASE_STRUCTURE):
                DIRECTORIES_WITH_EXCEPTION.append(file_path)
                logging.info('Directory <{}> with exception'.format(file_path))
                DIRECTORIES_WITH_EXCEPTION = remove_duplicates(DIRECTORIES_WITH_EXCEPTION)
                print(DIRECTORIES_WITH_EXCEPTION)
    
def main():
    logger_path = path.join(PATH, "files.log")
    logging.basicConfig(level = logging.INFO, filename = logger_path)
    logging.info('Init at {}'.format(datetime.now()))

    event_handler = PatternMatchingEventHandler(
        patterns="*", 
        ignore_patterns=[""], 
        ignore_directories=False, 
        case_sensitive=True
    )
    event_handler.on_any_event = on_any_event
    observer = Observer()
    observer.schedule(event_handler, PATH, recursive=True)
    observer.start()

    try:
        print("Starting...")
        while True:
            # Re-creating dir structure every 3 seconds... 
            build_structure(base_path=PATH, structure=BASE_STRUCTURE)
            time.sleep(3)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
    except Exception as error:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()