from typing import Any

from panflute import debug, Doc

from md2docx.pandoc.utils import metadata_as_dict
from md2docx.validators import existing_metadata_validator
from md2docx.exceptions import MetadataValidationError


def validate_metadata_from_dict(metadata: dict[str, Any]) -> None:
    """
    The Metadata validation logic.
    Throws ``MetadataValidationError`` with a list of errors
    """
    errors = existing_metadata_validator(metadata)

    if errors:
        raise MetadataValidationError(errors=errors)


def validate_metadata(doc: Doc) -> None:
    """
    Validate metadata from the Doc object
    """
    metadata = metadata_as_dict(doc)

    validate_metadata_from_dict(metadata)
