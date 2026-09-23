import re
import unittest
from unittest.mock import patch

import config
from chunker import split_documents
from ingest import Document, load_documents


class ChunkerTests(unittest.TestCase):
    def test_blank_and_heading_only(self):
        self.assertEqual(split_documents([Document('empty.txt', '   ')]), [])
        self.assertEqual(split_documents([Document('title.txt', 'Only a title')])[0].text,
                         'Only a title')

    def test_split_preserves_subject_prices_and_body(self):
        text = 'Laundry in Example Hall\n\nA wash costs $1.50. A dryer costs $1.25.\n\nGo on Tuesday morning.'
        with patch.object(config, 'CHUNK_SIZE', 65):
            chunks = split_documents([Document('laundry.txt', text)])
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(c.text.startswith('Laundry in Example Hall\n\n') for c in chunks))
        body = ' '.join(c.text.split('\n\n', 1)[1] for c in chunks)
        self.assertEqual(body, 'A wash costs $1.50. A dryer costs $1.25. Go on Tuesday morning.')
        self.assertEqual([c.index for c in chunks], list(range(len(chunks))))

    def test_oversized_sentence_is_not_cut(self):
        sentence = 'A single ' + 'long ' * 100 + 'sentence.'
        with patch.object(config, 'CHUNK_SIZE', 80):
            chunks = split_documents([Document('long.txt', 'A title\n\n' + sentence)])
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].text, 'A title\n\n' + sentence)

    def test_all_campus_body_text_survives_without_duplication(self):
        normalize = lambda text: re.sub(r'\s+', ' ', text).strip()
        for doc in load_documents('campus_life'):
            with self.subTest(source=doc.source):
                chunks = split_documents([doc])
                title, body = doc.text.split('\n\n', 1)
                self.assertTrue(all(c.text.startswith(title + '\n\n') for c in chunks))
                joined = ' '.join(c.text[len(title) + 2:] for c in chunks)
                self.assertEqual(normalize(joined), normalize(body))
                self.assertTrue(all(c.source == doc.source for c in chunks))
                self.assertTrue(all(c.produced_by == 'chunker.py::split_documents' for c in chunks))


if __name__ == '__main__':
    unittest.main()
