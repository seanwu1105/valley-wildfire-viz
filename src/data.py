import pathlib

DATA_DIR = pathlib.Path(__file__).parent.resolve() / "data"

EXCLUDED_IDS = (42000,)
FILE_IDS = filter(lambda id: id not in EXCLUDED_IDS, range(1000, 75000, 1000))

FILENAMES = [f"output.{file_id}.vts" for file_id in FILE_IDS]
