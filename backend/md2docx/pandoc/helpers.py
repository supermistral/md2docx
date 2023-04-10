from typing import Any

import panflute as pf

from md2docx import config
from md2docx.validators import existing_metadata_validator
from md2docx.exceptions import MetadataValidationError
from md2docx.pandoc.utils import metadata_as_dict


def validate_metadata_from_dict(metadata: dict[str, Any]) -> None:
    """
    The Metadata validation logic.
    Throws ``MetadataValidationError`` with a list of errors
    """
    errors = existing_metadata_validator(metadata)

    if errors:
        raise MetadataValidationError(errors=errors)


def validate_metadata(doc: pf.Doc) -> None:
    """
    Validate metadata from the Doc object
    """
    metadata = metadata_as_dict(doc)

    validate_metadata_from_dict(metadata)


def is_bibliography(elem: pf.Element) -> bool:
    """
    Checks if an element is a bibliography 
    """
    if (not isinstance(elem, (pf.OrderedList, pf.BulletList))
        or not isinstance(elem.parent, pf.Div)):
        return False

    for elem_class in elem.parent.classes:
        if elem_class.lower() in config.BIBLIOGRAPHY_LIST_CLASSES:
            return True

    return False
