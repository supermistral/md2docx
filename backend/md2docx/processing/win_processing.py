import os, sys, inspect
from typing import Optional

import win32com.client


def get_script_directory() -> str:
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def get_file_path(file: str) -> str:
    script_dir = get_script_directory()
    return os.path.join(script_dir, file)


def main(input_file: str, output_file: Optional[str] = None, pdf: bool = True) -> None:
    input_file_path = get_file_path(input_file)

    word = win32com.client.DispatchEx("Word.Application")
    doc = word.Documents.Open(input_file_path)

    doc.TablesOfContents(1).Update()

    if output_file is None:
        close_options = {'SaveChanges': True}
        if pdf:
            pdf_file = input_file_path
    else:
        output_file_path = get_file_path(output_file)
        pdf_file = output_file_path.rsplit('.', 1)[0] + '.pdf'
        close_options = {'FileName': output_file_path}

    if pdf:
        doc.SaveAs(pdf_file, FileFormat=17)

    doc.SaveAs(**close_options)
    doc.Close()

    word.Quit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Word file path expected")
        exit()

    main(sys.argv[1])
