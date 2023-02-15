import sys

from .post_processing import main as start_post_processing

if sys.platform.startswith('win'):
    from .win_processing import main as start_win_processing
else:
    start_win_processing = lambda x, y: None
