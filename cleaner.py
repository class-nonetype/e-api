from pathlib import Path
from shutil import rmtree

for path, directories, files in Path(__file__).absolute().parent.walk():
    if path.name == '__pycache__':
        rmtree(path)
    print(f'{path=}')
