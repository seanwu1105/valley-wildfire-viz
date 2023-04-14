import pathlib

DATA_DIR = pathlib.Path(__file__).parent.parent.resolve() / "data"

EXCLUDED_IDS = (42000,)
FILE_ID_MIN = 1000
FILE_ID_MAX = 74000
FILE_ID_STEP = 1000
FILE_IDS = filter(
    lambda id: id not in EXCLUDED_IDS,
    range(FILE_ID_MIN, FILE_ID_MAX + FILE_ID_STEP, FILE_ID_STEP),
)


def to_filename(file_id: int) -> str:
    if file_id in EXCLUDED_IDS:
        return to_filename(file_id + FILE_ID_STEP)
    return f"output.{file_id}.vts"


FILENAMES = [to_filename(file_id) for file_id in FILE_IDS]
