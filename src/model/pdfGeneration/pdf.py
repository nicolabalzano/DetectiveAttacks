import os.path

import pdfkit


def generate_pdf_from_html(html_file_path, pdf_file_path):
    """
    Generate a PDF file from an HTML file
    :param pdf_file_path: path to the PDF file
    :param html_file_path: path to the HTML file
    :return: path to the PDF file
    """

    print(os.path.abspath(__file__))
    parent_path = os.path.dirname(os.path.abspath(__file__))
    print(parent_path+'\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    # config = pdfkit.configuration(wkhtmltopdf=parent_path + '\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    # , configuration=config
    pdfkit.from_file(html_file_path, pdf_file_path)

    return pdf_file_path