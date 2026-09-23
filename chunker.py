"""Stage 2: paragraph- and sentence-aware chunks for short campus posts.

The original fixed-window fallback is retained for comparison. The active
splitter repeats a short document title and preserves whole sentences.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Pack paragraphs under a soft size target, retaining the title as context.

    Oversized paragraphs are packed by sentence. Oversized single sentences
    remain intact. There is no body overlap; only the title repeats.
    """
    if config.CHUNK_SIZE <= 0:
        raise ValueError("chunk_size must be positive")
    if config.CHUNK_OVERLAP != 0:
        raise ValueError("split_documents uses zero body overlap")

    chunks: list[Chunk] = []
    for doc in documents:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", doc.text.strip())
                      if p.strip()]
        if not paragraphs:
            continue
        title = ""
        if (len(paragraphs) > 1 and "\n" not in paragraphs[0]
                and len(paragraphs[0]) <= 120
                and not paragraphs[0].endswith((".", "!", "?"))):
            title = paragraphs.pop(0)
        prefix = title + "\n\n" if title else ""
        budget = max(1, config.CHUNK_SIZE - len(prefix))
        pieces: list[str] = []
        current = ""

        def add(unit: str, separator: str):
            nonlocal current
            candidate = current + separator + unit if current else unit
            if current and len(candidate) > budget:
                pieces.append(current)
                current = unit
            else:
                current = candidate

        for paragraph in paragraphs:
            if len(paragraph) <= budget:
                add(paragraph, "\n\n")
            else:
                # Decimal prices are safe: the dot in $1.50 has no following
                # whitespace. This is deliberately a lightweight English rule.
                sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"“])', paragraph)
                for i, sentence in enumerate(sentences):
                    add(sentence, "\n\n" if i == 0 else " ")
        if current:
            pieces.append(current)
        for index, piece in enumerate(pieces):
            chunks.append(Chunk(
                text=prefix + piece,
                source=doc.source,
                index=index,
                produced_by="chunker.py::split_documents",
            ))
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
