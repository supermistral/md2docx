from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

PROCESSING_URL = BASE_DIR / 'pandoc' / 'run.py'

WORD_REFERENCE_PATH = BASE_DIR / 'samples' / 'reference2.docx'

ALIGN_CLASSES = {
    'right': ['right', 'справа'],
    'left': ['left', 'слева'],
}

BIBLIOGRAPHY_LIST_CLASSES = [
    'литература',
    'bibliography'
]

ATTRIBUTES_VALIDATORS = {
    'fontsize': lambda x: x.isnumeric(),
}
