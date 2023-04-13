import concurrent.futures
import pathlib
import shutil
import urllib.request

# Download dataset from https://www.lanl.gov/projects/sciviscontest2022/

URL_BASE = "https://wifire-data.sdsc.edu/data/SciVis2022/valley_losAlamos/"
FILENAME_BASE = "valley_losAlamos.output."
FILENAME_EXT = ".vts"
FILE_IDS = range(1000, 75000, 1000)

DATA_DIR = pathlib.Path(__file__).parent.resolve() / "data"


def download_file(file_id: int):
    url = f"{URL_BASE}{FILENAME_BASE}{file_id}{FILENAME_EXT}"
    file_path = DATA_DIR / f"{FILENAME_BASE}{file_id}{FILENAME_EXT}"
    print(f"Downloading {file_path}...")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, open(file_path, "wb") as out_file:
        shutil.copyfileobj(response, out_file)
    print(f"Downloaded {file_path}.")


with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(download_file, FILE_IDS)
