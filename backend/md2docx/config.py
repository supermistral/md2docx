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
    'bibliography',
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
    'bibliography': 'validators.bibliography_validator',
}

BIBLIOGRAPGHY_SETTINGS = {
    'order': [
        'author', 
        'title',
        'editors',
        {
            'issue': [
                'title',
                {'place': [
                    'city',
                    'publisher'
                ]},
                'year',
                'number',
            ]
        },
        'number',
        'page',
        {
            'url': [
                'link',
                'date',
            ]
        },
        'isbn',
    ],
    'format': [
        {
            'keys': [
                'book',
                'collection',
                'guideline',
                'article',
                'article_from_collection',
                'regulation',
                'patent',
                'gost',
                'website',
                'article_from_website',
                'book_from_ebs',
            ],
            'base': ('{author} {title} / {editors}. - {issue_title}. - '
                     '{issue_place_city}: {issue_place_publisher}, {issue_year}'
                     '. - {page} с.'),
            'electronic': ('{author} {title} / {editors}. - {issue_title}. - '
                           '{issue_place_city}: {issue_place_publisher}, '
                           '{issue_year}. - {page} с. - URL: {url_link} '
                           '(дата обращения {url_date}). - Текст: электронный.'),
        },
    ],
    # Use as {'default_format_key': 'book'}
    'default': 'default_format_key',
    'default_format_key': 'book',
}
