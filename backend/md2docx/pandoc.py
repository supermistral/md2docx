import sys
from typing import Callable, Optional

from panflute import run_filters, debug, Element, Doc

# Check for isolated run as a pandoc filter
# Need to make the root directory visible
try:
    sys.path.append('.')
    import md2docx
except ModuleNotFoundError:
    sys.path[-1] = '..'

debug(sys.path)

from pandoc.helpers import validate_metadata
from pandoc.filters import (
    BaseFilter, ImageCaptionFilter, TableCaptionFilter, HeaderFilter,
    ListFilter, DocMetadataFilter, AttributeTaggingFilter
)


def prepare(doc: Doc) -> None:
    validate_metadata(doc)


def get_filters() -> list[Callable[[Element, Doc], Optional[Element]]]:
    filter_classes: list[BaseFilter] = [
        DocMetadataFilter,
        ImageCaptionFilter,
        TableCaptionFilter,
        ListFilter,
        HeaderFilter,
        AttributeTaggingFilter
    ]

    return [filter_class().run for filter_class in filter_classes]


def main(doc: Optional[Doc] = None) -> None:
    return run_filters(get_filters(), doc=doc, prepare=prepare)


if __name__ == '__main__':
    main()
