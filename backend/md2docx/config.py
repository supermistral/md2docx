from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

PROCESSING_URL = BASE_DIR / 'pandoc.py'

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
    'fontsize': 'validators.integer_validator',
    'left-indent': 'validators.float_validator',
    'right-indent': 'validators.float_validator',
    'first-line-indent': 'validators.float_validator',
    'line-spacing': 'validators.float_validator',
}

METADATA_VALIDATORS = {
    **ATTRIBUTES_VALIDATORS,

    'list': 'validators.list_validator',
}
