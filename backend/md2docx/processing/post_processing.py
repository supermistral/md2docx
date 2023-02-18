import sys
from typing import Optional

from docx import Document
from docx.shared import Pt, Cm
from docx.text.paragraph import Paragraph

from ..utils import unpack_attributes, search_end_of_text_attributes


class PostProcessing:
    def __init__(self, file: str):
        self.file = file
        self.doc = Document(file)
        self.num_ids = set()
        self.namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        }

    def handle_fontsize(self, p: Paragraph, value: str) -> None:
        size = int(value)
        for r in p.runs:
            r.font.size = Pt(size)

    def handle_left_indent(self, p: Paragraph, value: str) -> None:
        p.paragraph_format.left_indent = Cm(float(value))

    def handle_right_indent(self, p: Paragraph, value: str) -> None:
        p.paragraph_format.right_indent = Cm(float(value))

    def handle_first_line_indent(self, p: Paragraph, value: str) -> None:
        p.paragraph_format.first_line_indent = Cm(float(value))

    def handle_line_spacing(self, p: Paragraph, value: str) -> None:
        p.paragraph_format.line_spacing = float(value)

    def apply_attributes(self, para: Paragraph, attributes: dict[str, str]) -> None:
        for attr in attributes:
            handler = getattr(self, 'handle_' + attr, None)
            if handler is not None:
                handler(para, attributes[attr])

    def is_list(self, para: Paragraph) -> bool:
        return len(para._element.xpath('./w:pPr/w:numPr')) > 0

    def pre_process_lists(self, para: Paragraph) -> None:
        num_id = para._p.pPr.numPr.numId.val
        self.num_ids.add(num_id)

    def process_lists(self) -> None:
        if not self.num_ids:
            return

        abstract_ids = set()
        numbering = self.doc.part.numbering_part.numbering_definitions._numbering

        for num_id in self.num_ids:
            num_id_el = numbering.num_having_numId(num_id)
            abstract_ids.add(num_id_el.abstractNumId.val)

        get_abstract_num_xpath = lambda id: f'./w:abstractNum[@w:abstractNumId="{id}"]'
        get_lvl_xpath = lambda id: f'./w:lvl[@w:ilvl="{id}"]'
        lvl_count = 9

        for abstract_id in abstract_ids:
            xpath = get_abstract_num_xpath(abstract_id)
            abstract_num = numbering.xpath(xpath)[0]

            for lvl in range(lvl_count):
                lvl_xpath = get_lvl_xpath(lvl)
                lvl = abstract_num.xpath(lvl_xpath, namespaces=self.namespaces)[0]
                # TODO: custom lists formatting

    def process(self) -> None:
        attrs_end = True

        for para in self.doc.paragraphs:
            if self.is_list(para) and para.style.name != 'Bibliography':
                self.pre_process_lists(para)
            else:
                if not attrs_end:
                    text, attrs_end = search_end_of_text_attributes(para.text)
                else:
                    text, attrs, attrs_id = unpack_attributes(para.text)
                    if attrs:
                        text, attrs_end = search_end_of_text_attributes(text)

                para.text = text

                if attrs:
                    self.apply_attributes(para, attrs)

        self.process_lists()

    def save(self, file: Optional[str] = None) -> None:
        self.doc.save(file or self.file)


def main(file: str):
    post_processing = PostProcessing(file)
    post_processing.process()
    post_processing.save()


if __name__ == '__main__':
    main(sys.argv[1])
