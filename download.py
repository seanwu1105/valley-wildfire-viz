import concurrent.futures
import shutil
import urllib.request

from vtkmodules.vtkIOXML import vtkXMLStructuredGridWriter

from src.data import FILE_IDS, ORIGINAL_DIR, to_filename

# Download dataset from https://www.lanl.gov/projects/sciviscontest2022/

URL_BASE = "https://oceans11.lanl.gov/firetec/valley_losAlamos/"


def download_file(file_id: int):
    writer = vtkXMLStructuredGridWriter()
    filename = to_filename(file_id, writer.GetDefaultFileExtension())

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


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(download_file, FILE_IDS)


if __name__ == "__main__":
    main()
