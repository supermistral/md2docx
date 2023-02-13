import base64
import json
import re
from panflute import debug


def escape_text_with_attributes(text: str) -> str:
    """
    Escapes text if it already contains part as attributes representation
    """
    to_escape = re.search(r'^\\*%(\d+);\w+%', text)
    if to_escape is not None:
        return '\\' + text
    return text


def pack_attributes(attributes: dict[str, str], id: int) -> tuple[str, str]:
    """
    Returns start and end string representation of the attributes.
    They must be inserted into text
    """
    encoded = base64.b64encode(json.dumps(attributes).encode('utf-8')).decode('utf-8')
    return f'%{id};{encoded}%', f'%{id}%'


def unpack_attributes(text: str) -> tuple[str, dict[str, str], str]:
    """
    Extracts attributes from the text. Returns new text with start attributes representation
    removed (from the beggining of the text).

    Removes escaping symbols if pattern was escaped
    """
    encoded_regex = re.search(r'^\\*%(\d+);(\w+)%', text)
    attributes = {}
    attrs_id = None

    if encoded_regex is not None:
        if text.startswith('\\'):
            text = text[1:]
        else:
            text = text.replace(encoded_regex.group(0), '', 1)
            attrs_id, decoded = encoded_regex.group(1), encoded_regex.group(2)
            attributes = json.loads(base64.b64decode(decoded))

    return text, attributes, attrs_id


def search_end_of_text_attributes(text: str) -> tuple[str, bool]:
    """
    Looks for the end attributes representation pattern.
    Returns new text and flag indicating the success of the search
    """
    encoded_regex = re.search(r'\\*%(\d+)%$', text)
    end = False

    if encoded_regex is not None:
        encoded_str = encoded_regex.group(0)

        if encoded_str.startswith('\\'):
            text = text.replace(encoded_str, encoded_str[1:])
        else:
            text = text.replace(encoded_str, '', 1)
            end = True

    return text, end
