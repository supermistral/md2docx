class ProcessingError(Exception):
    """Error raised during processing"""
    pass


class WinProcessingError(Exception):
    """Error raised during windows processing"""
    pass


class PostProcessingError(Exception):
    """Error raised during post-processing"""
    pass
