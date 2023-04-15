import concurrent.futures
import shutil
import urllib.request

from src.data import FILENAMES, ORIGINAL_DIR

# Download dataset from https://www.lanl.gov/projects/sciviscontest2022/

URL_BASE = "https://oceans11.lanl.gov/firetec/valley_losAlamos/"


def download_file(filename: str):
    url = f"{URL_BASE}{filename}"
    file_path = ORIGINAL_DIR / filename

    if file_path.exists():
        print(f"Skipping {file_path}...")
        return

    print(f"Downloading {file_path}...")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, open(file_path, "wb") as out_file:
        shutil.copyfileobj(response, out_file)
    print(f"Downloaded {file_path}.")


with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(download_file, FILENAMES)
