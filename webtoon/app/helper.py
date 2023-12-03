import os
import requests
from zipfile import ZipFile


def get_image(name: str, url: str, dir: str):
    path = os.path.join(dir, name)
    with open(f'{path}.jpg', 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)
            return

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)


def make_dir(name: str):
    try:  
        os.mkdir(name)  
    except OSError as error:  
        return
    
    
def zip_dir(dir_path):
    with ZipFile(f"{dir_path}.zip", 'w') as z:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                z.write(os.path.join(root, file))
            for directory in dirs:
                z.write(os.path.join(root, directory))