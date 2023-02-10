from typing import Optional

import panflute as pf

import config


OPENXML_CAPTION_NUMBER_WITH_SECTION = '''
<w:fldSimple w:instr=" STYLEREF 2 \s ">
<w:r><w:t>{1}</w:t></w:r>
</w:fldSimple>
<w:fidChar>
<w:r><w:t>.</w:t></w:r>
</w:fidChar>
<w:fldSimple w:instr=" SEQ {0} \* ARABIC \s 2 ">
<w:r><w:t>{2}</w:t></w:r>
</w:fldSimple>
'''

OPENXML_CAPTION_NUMBER = '''
<w:fldSimple w:instr=" SEQ {} \* ARABIC ">
<w:r><w:t>{}</w:t></w:r>
</w:fldSimple>
'''

OPENXML_ALIGNMENT = '''
<w:pPr>
<w:jc w:val="{}"/>
</w:pPr>
'''


def alignment_by_classes(style_classes: list[str]) -> Optional[str]:
    for style_class in style_classes:
        for align_class in config.ALIGN_CLASSES:
            if style_class in config.ALIGN_CLASSES[align_class]:
                return OPENXML_ALIGNMENT.format(align_class)
    return None


def caption_number(label: str, object_number: int) -> str:
    return OPENXML_CAPTION_NUMBER.format(label, object_number)


def caption_number_with_section(label: str, object_number: int, section_number: int) -> str:
    return OPENXML_CAPTION_NUMBER_WITH_SECTION.format(label, section_number, object_number)


def pagebreak() -> str:
    return "<w:p><w:r><w:br w:type=\"page\" /></w:r></w:p>"


def to_raw_block(openxml: str) -> pf.RawBlock:
    return pf.RawBlock(openxml, format='openxml')


def to_raw_inline(openxml: str) -> pf.RawInline:
    return pf.RawInline(openxml, format='openxml')