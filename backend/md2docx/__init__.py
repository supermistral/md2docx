import os
import subprocess
from typing import Optional

from . import config
from .exceptions import ProcessingError, WinProcessingError, PostProcessingError
from .processing import start_post_processing, start_win_processing


__all__ = ['run_processing', 'run_win_processing', 'run_post_processing']


def run_processing(input_file: str, output_file: Optional[str] = None) -> None:
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.docx'

    command = [
        'pandoc', input_file,
        '--reference-doc', config.WORD_REFERENCE_PATH,
        '-t', 'docx',
        '--filter', config.PROCESSING_URL,
        '--toc',
        '-o', output_file,
    ]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, encoding='utf-8')

    if result.returncode != 0:
        raise ProcessingError(result.stderr)


def run_win_processing(input_file: str, output_file: Optional[str] = None) -> None:
    try:
        start_win_processing(input_file, output_file)
    except Exception as exc:
        raise WinProcessingError(*exc.args)


def run_post_processing(input_file: str, output_file: Optional[str] = None) -> None:
    output_file = output_file or input_file
    try:
        start_post_processing(input_file)
    except Exception as exc:
        raise PostProcessingError(*exc.args)
