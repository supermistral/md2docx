from typing import Any, Optional

import panflute as pf


class HandlerException(Exception):
    """
    Handler exception class for the representation errors
    """
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class BaseHandler(metaclass=Singleton):
    """
    Base class for handling operations due to the Doc object

    Uses Singleton pattern to provide single instance
    """

    __slots__ = []

    def __init__(self, doc: Optional[pf.Doc] = None) -> None:
        if self.metadata_field is not None:
            assert doc is not None
            self.metadata = doc.get_metadata(self.metadata_field)
        else:
            self.metadata = None

    def __call__(self, *args, **kwargs) -> Any:
        try:
            return self.run(*args, **kwargs)
        except Exception as exc:
            message = f'An error occured in the handler [{self.__class__.__name__}]: {str(exc)}'
            raise HandlerException(message)

    @property
    def metadata_field(self) -> Optional[str]:
        return None

    def run(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Handler must have 'run' method")
