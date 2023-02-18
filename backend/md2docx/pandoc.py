from typing import Callable, Optional

from panflute import run_filters, debug, Element, Doc

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
