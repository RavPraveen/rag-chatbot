from src.document_loader import load_document


def test_load_document_supports_txt_file_extension():
    pages = load_document(b"hello world\nthis is a text file", "notes.TXT")

    assert pages == [(1, "hello world\nthis is a text file")]