from typing import Any, Optional

import panflute as pf
from panflute.tools import meta2builtin


def get_metadata(doc: pf.Doc, key: Any = '', default: Optional[Any] = None, builtin: bool = True):
    """
    The Custom metadata getter from ``panflute.tools._get_metadata`` without separating by dots.
    It is needed to class metadata support
    """
    meta = doc.metadata

    if key:
        if key in doc.metadata.content:
            meta = meta[key]
        else:
            return default

    return meta2builtin(meta) if builtin else meta


def metadata_as_dict(doc: pf.Doc) -> dict[str, Any]:
    return {x: get_metadata(doc, x) for x in doc.metadata.content}


def convert_text_to_content(text: str) -> list[pf.Inline]:
    return pf.convert_text(text)[0].content
