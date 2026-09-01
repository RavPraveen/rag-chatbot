import unittest

from src.text_splitter import split_text


class PageNumberChunkingTests(unittest.TestCase):
    def test_split_text_includes_page_number_in_each_chunk(self):
        pages = [
            (1, "This is page one. " * 30),
            (2, "This is page two. " * 30),
        ]

        chunks = split_text(pages, chunk_size=200, chunk_overlap=50)

        self.assertTrue(chunks)
        self.assertTrue(all("[Page " in chunk and "]" in chunk for chunk in chunks))
        self.assertTrue(any(chunk.startswith("[Page 1]") for chunk in chunks))
        self.assertTrue(any(chunk.startswith("[Page 2]") for chunk in chunks))


if __name__ == "__main__":
    unittest.main()
