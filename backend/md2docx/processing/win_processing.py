import os, sys, inspect
from typing import Optional

import win32com.client


def get_script_directory() -> str:
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def get_file_path(file: str) -> str:
    script_dir = get_script_directory()
    return os.path.join(script_dir, file)


def main(input_file: str, output_file: Optional[str] = None) -> None:
    file_path = get_file_path(input_file)

    word = win32com.client.DispatchEx("Word.Application")
    doc = word.Documents.Open(file_path)

    doc.TablesOfContents(1).Update()

    if output_file is None:
        doc.Close(SaveChanges=True)
    else:
        output_file_path = get_file_path(output_file)
        doc.SaveAs(output_file_path)
        doc.Close()

    print("OK")

    word.Quit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Word file path expected")
        exit()

    main(sys.argv[1])
