import fitz

#Extract the text from the pdf file given the parameters the text is extracted
def load_pdf(file_bytes: bytes) -> list[tuple[int, str]]:
    """
    Extract text from a PDF file and keep the page number for each page.
    Parameters
    ----------
    file_bytes : bytes
        PDF file contents.
    Returns
    -------
    list[tuple[int, str]]
        A list of (page_number, page_text) tuples.
    """

    document = fitz.open(stream=file_bytes, filetype="pdf")

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()
        if text.strip():
            pages.append((page_number, text))

    document.close()
    return pages


def load_text(file_bytes: bytes) -> list[tuple[int, str]]:
    """
    Decode a plain text file as page 1.
    """

    try:
        text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = file_bytes.decode("latin-1", errors="ignore")

    if not text.strip():
        return []
    return [(1, text)]


def load_document(file_bytes: bytes, filename: str) -> list[tuple[int, str]]:
    """
    Load a supported document based on its extension.
    """

    extension = filename.lower().split(".")[-1]

    if extension == "pdf":
        return load_pdf(file_bytes)

    if extension == "txt":
        return load_text(file_bytes)

    raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")