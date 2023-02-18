from typing import Any

from panflute import debug, Doc

from validators import existing_metadata_validator
from exceptions import MetadataValidationError


def metadata_as_dict(doc: Doc) -> dict[str, Any]:
    return {x: doc.get_metadata(x) for x in doc.metadata.content}


def validate_metadata(doc: Doc) -> None:
    metadata = metadata_as_dict(doc)
    errors = existing_metadata_validator(metadata)

    if errors:
        raise MetadataValidationError(errors=errors)
