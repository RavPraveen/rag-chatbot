def split_text(
    text,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[str]:
    """
    Split text into overlapping chunks and prefix each chunk with its page number.

    Parameters
    ----------
    text : str | list[tuple[int, str]]
        Input document text or a list of (page_number, page_text) pairs.

    chunk_size : int
        Maximum approximate number of characters per chunk.

    chunk_overlap : int
        Number of overlapping characters between chunks.
    """

    def chunk_single_text(page_text: str, page_number: int) -> list[str]:
        if not page_text or not str(page_text).strip():
            return []

        clean_text = str(page_text).replace("\r\n", "\n").strip()
        if not clean_text:
            return []

        chunks = []
        start = 0

        while start < len(clean_text):
            end = min(start + chunk_size, len(clean_text))

            if end < len(clean_text):
                boundary = clean_text.rfind("\n", start, end)
                if boundary == -1:
                    boundary = clean_text.rfind(". ", start, end)
                if boundary > start + chunk_size // 2:
                    end = boundary + 1

            chunk = clean_text[start:end].strip()

            if chunk:
                chunks.append(f"[Page {page_number}] {chunk}")

            if end >= len(clean_text):
                break

            start = max(end - chunk_overlap, start + 1)

        return chunks

    if isinstance(text, list):
        chunks = []
        for page_number, page_text in text:
            chunks.extend(chunk_single_text(page_text, page_number))
        return chunks

    if not text or not str(text).strip():
        return []

    return chunk_single_text(text, page_number=1)