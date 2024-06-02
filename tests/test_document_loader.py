import unittest
from insertion import load_html_documents, split_documents, update_document_metadata

class TestDocumentLoader(unittest.TestCase):
    def test_load_html_documents(self):
        directory_path = "tests/documents_test_files"
        documents = load_html_documents(directory_path)
        self.assertGreater(len(documents), 0)
        
    def test_update_document_metadata(self):
        directory_path = "tests/documents_test_files"
        documents = load_html_documents(directory_path)
        update_document_metadata(documents)
        self.assertIn("source", documents[0].metadata)

if __name__ == "__main__":
    unittest.main()