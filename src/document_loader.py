import fitz

#Extract the text from the pdf file given the parameters the text is extracted
def load_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file.

    Parameters
    ----------
    file_bytes : bytes
        PDF file contents.

    Returns
    -------
    str
        Extracted text.
    """

    document = fitz.open(stream=file_bytes, filetype="pdf")

    pages = []

    for page in document:
        text = page.get_text()
        if text.strip():
            pages.append(text)

    document.close()
    #join each page with a double line breaker and return   
    return "\n\n".join(pages)


def load_text(file_bytes: bytes) -> str:
    """
    Decode a plain text file.
    """

    return file_bytes.decode("utf-8", errors="ignore")


def load_document(file_bytes: bytes, filename: str) -> str:
    """
    Load a supported document based on its extension.
    """

    extension = filename.lower().split(".")[-1]

    if extension == "pdf":
        return load_pdf(file_bytes)

    if extension == "txt":
        return load_text(file_bytes)

    raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")