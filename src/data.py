import pathlib

DATA_DIR = pathlib.Path(__file__).parent.parent.resolve() / "data"
ORIGINAL_DIR = DATA_DIR / "original"
EXTRACTED_DIR = DATA_DIR / "extracted"
IMAGE_DATA_DIR = DATA_DIR / "image_data"

EXCLUDED_IDS = (42000,)
FILE_ID_MIN = 1000
FILE_ID_MAX = 74000
FILE_ID_STEP = 1000
FILE_IDS = filter(
    lambda id: id not in EXCLUDED_IDS,
    range(FILE_ID_MIN, FILE_ID_MAX + FILE_ID_STEP, FILE_ID_STEP),
)


def to_filename(file_id: int, extension: str) -> str:
    if file_id in EXCLUDED_IDS:
        return to_filename(file_id + FILE_ID_STEP, extension)
    return f"output.{file_id}.{extension}"
