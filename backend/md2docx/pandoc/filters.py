from typing import Type, Optional

from panflute import (
    debug, convert_text, stringify, Element, Inline, Image, Span, Str, Space,
    RawInline, Caption, Block, Header, Plain, Doc, ListItem, BulletList,
    OrderedList, Div, Para, RawBlock, ListContainer, Cite,
)

import config
from utils import pack_attributes, escape_text_with_attributes
from validators import get_validator
from pandoc import oxml
from pandoc.helpers import is_bibliography
from pandoc.handlers import BibliographyHandler
from pandoc.utils import convert_text_to_content


class NumberedBlock:
    def __init__(self, label, caption, object_number, section_number=None,
                 identifier='', classes=[], attributes={}):
        if not section_number:
            openxml_number = oxml.caption_number(
                label=label,
                object_number=object_number
            )
        else:
            openxml_number = oxml.caption_number_with_section(
                label=label,
                object_number=object_number,
                section_number=section_number
            )
        
        new_caption = [
            Str(label),
            Space,
            oxml.to_raw_inline(openxml_number),
        ]

        if len(caption) > 0:
            new_caption += [
                Space,
                Str('-'),
                Space,
                *caption
            ]

        self.span = Span(
            *new_caption, 
            identifier=identifier,
            classes=classes,
            attributes=attributes
        )

    def get_content(self) -> Inline:
        return self.span


class AlignmentMixin:
    def set_alignment(self, elem: Element) -> None:
        openxml = oxml.alignment_by_classes(elem.classes)
        if openxml is not None:
            elem.content = [oxml.to_raw_inline(openxml), *elem.content]


class BaseFilter:
    """Базовый класс для фильтра с метдом run()"""

    def run(self, elem: Element, doc: Doc) -> Optional[Element]:
        raise NotImplementedError('Filter should have "run" method')


class DocMetadataFilter(BaseFilter):
    def run(self, elem: Element, doc: Doc) -> Optional[Element]:
        # Adding a page break to the abstract
        # debug(doc.metadata.content. dict)
        pass
        # doc.metadata['abstract'] = ' `<w:p><w:r><w:br w:type="page"/></w:r></w:p>`{=openxml}'


class CaptionBaseFilter(BaseFilter):
    """Базовый фильтр для установки нумерации"""

    header_count = 0
    object_count = 0

    def __init__(self, label: str, elem_class: Type[Element]):
        self.label = label
        self.elem_class = elem_class

    def run(self, elem: Element, doc: Doc):
        if isinstance(elem, Header) and elem.level == 2:
            self.header_count += 1
            self.object_count = 0
        elif isinstance(elem, self.elem_class):
            self.object_count += 1

            if len(elem.content) > 0 and isinstance(elem.content[0], Plain):
                elem_caption = elem.content[0].content
            else:
                elem_caption = elem.content

            figure_caption = NumberedBlock(self.label, elem_caption, 
                                           self.object_count, self.header_count)
            self.save_caption(elem, figure_caption.get_content())

    def save_caption(self, elem: Element, caption: Inline) -> None:
        elem.content = [caption]


class ImageCaptionFilter(CaptionBaseFilter):
    """Фильтр для установки нумерации на подписях к рисункам"""

    def __init__(self):
        super().__init__("Рисунок", Image)


class TableCaptionFilter(CaptionBaseFilter):
    """Фильтр для установки нумерации на подписях к таблицам"""
    
    def __init__(self):
        super().__init__("Таблица", Caption)

    def save_caption(self, elem: Element, caption: Inline) -> None:
        elem.content = [Plain(caption)]


class BibliographyFilter(BaseFilter):
    """Фильтр для установки списка литературы и замены ссылок"""

    def run(self, elem: Element, doc: Doc):
        if is_bibliography(elem):
            handler = BibliographyHandler()
            bibliography_list = handler()

            # Convert strings to ordered list items
            elems = [Plain(*convert_text_to_content(item))
                     for item in bibliography_list]
            elems = [ListItem(x) for x in elems]

            elem = OrderedList(*elems, *elem.content)

            return elem
        elif isinstance(elem, Cite):
            id = stringify(elem)

            # TODO: upgrade Cite recognition
            if id.startswith('@'):
                handler = BibliographyHandler()
                ref = handler.get_reference(id[1:])

                return Span(*convert_text_to_content(ref))


class ListFilter(BaseFilter):
    """Фильтр для установки стилей списков (обычных и литературы)"""

    def run(self, elem: Element, doc: Doc):
        if isinstance(elem, (OrderedList, BulletList)):
            # Check list for bibliography
            is_bibl = is_bibliography(elem)

            if is_bibl and not isinstance(elem, OrderedList):
                elem = OrderedList(*elem.content)

            for list_item in elem.content:
                block = list_item.content[0]

                if isinstance(block, Plain):
                    # Using the Para element to avoid setting 'Compact' style for list
                    list_item.content[0] = Div(
                        Para(*block.content),
                        attributes={'custom-style': 'Bibliography' if is_bibl else 'Body Text'}
                    )

            # Add page break after bibliography + add header
            if is_bibl:
                pagebreak_raw_block = oxml.to_raw_block(oxml.PAGEBREAK)
                return Div(
                    Header(Str("Список использованной литературы"), level=1),
                    elem,
                    pagebreak_raw_block
                )
            # else:
                # debug([s.content for s in elem.content.list])

            return elem


class HeaderFilter(BaseFilter, AlignmentMixin):
    """Установка выраванивания и разрывов для заголовков"""

    def run(self, elem: Element, doc: Doc):
        if isinstance(elem, Header):
            self.set_alignment(elem)

            # Add page break before lvl 1 header
            if elem.level == 1:
                pagebreak_raw_block = oxml.to_raw_block(oxml.PAGEBREAK)
                return Div(pagebreak_raw_block, elem)


class AttributeTaggingFilter(BaseFilter):
    """Маркировка аттрибутов - упаковка в текст для последующей обработки"""

    attrs_id = 0

    def check_attributes(self, attributes: dict[str, str]) -> bool:
        for attr in attributes:
            if (attr not in config.ATTRIBUTES_VALIDATORS or
                not get_validator(config.ATTRIBUTES_VALIDATORS[attr])(attributes[attr])):
                    # TODO: add error collector
                    return False
        return True

    def insert_packed_attributes(self, content: ListContainer,
                                 attrs_start: Optional[str], attrs_end: Optional[str]) -> None:
        if content.oktypes == Inline:
            if attrs_start is not None:
                content.insert(0, Str(attrs_start))
            if attrs_end is not None:
                content.append(Str(attrs_end))
        else:
            self.insert_packed_attributes(content[0].content, attrs_start, None)
            self.insert_packed_attributes(content[-1].content, None, attrs_end)

    def run(self, elem: Element, doc: Doc):
        if hasattr(elem, 'text'):
            elem.text = escape_text_with_attributes(elem.text)

        if hasattr(elem, 'attributes'):
            attributes = getattr(elem, 'attributes')

            if not attributes or not self.check_attributes(attributes):
                return elem

            attrs_start, attrs_end = pack_attributes(attributes, id=self.attrs_id)
            self.attrs_id += 1

            self.insert_packed_attributes(elem.content, attrs_start, attrs_end)

        return elem
