from ..modeling import BaseResponse


class DocumentTemplate(BaseResponse):
    name: str
    content: str


class ListDocumentTemplatesResponse(BaseResponse):
    templates: list[DocumentTemplate]
