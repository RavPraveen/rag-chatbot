def split_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[str]:
    """
    Split text into overlapping chunks.

    Parameters
    ----------
    text : str
        Input document text.

    chunk_size : int
        Maximum approximate number of characters per chunk.

    chunk_overlap : int
        Number of overlapping characters between chunks.
    """

    if not text.strip():
        return []

    text = text.replace("\r\n", "\n").strip()

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Try to avoid cutting in the middle of a sentence.
        if end < len(text):
            boundary = text.rfind("\n", start, end)
            #if no line break found go for  .
            if boundary == -1:
                boundary = text.rfind(". ", start, end)
            #check at leat the end is halfway there the length of the chunk size andinclude the punctuations,\n by +1
            if boundary > start + chunk_size // 2:
                end = boundary + 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break
        #make sure the next starting point is always after the previous starting point
        start = max(end - chunk_overlap, start + 1)

    return chunks