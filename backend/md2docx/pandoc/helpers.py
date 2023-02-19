from typing import Any

from panflute import debug, Doc

from pandoc.utils import metadata_as_dict
from validators import existing_metadata_validator
from exceptions import MetadataValidationError


def validate_metadata(doc: Doc) -> None:
    """
    The Metadata validation logic.
    Throws ``MetadataValidationError`` with a list of errors
    """
    metadata = metadata_as_dict(doc)
    errors = existing_metadata_validator(metadata)

    if errors:
        raise MetadataValidationError(errors=errors)
