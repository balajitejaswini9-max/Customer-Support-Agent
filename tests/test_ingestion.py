from pathlib import Path

import pytest

from src.ingestion import DocumentChunk, load_knowledge_base

KB_DIR = Path(__file__).parent.parent / "knowledge_base"


def test_load_returns_chunks():
    chunks = load_knowledge_base(KB_DIR)
    assert len(chunks) > 0


def test_every_chunk_is_document_chunk():
    for chunk in load_knowledge_base(KB_DIR):
        assert isinstance(chunk, DocumentChunk)


def test_chunks_have_non_empty_fields():
    for chunk in load_knowledge_base(KB_DIR):
        assert chunk.text.strip(), "text must not be empty"
        assert chunk.source, "source must not be empty"
        assert chunk.section, "section must not be empty"


def test_all_seed_sources_present():
    sources = {c.source for c in load_knowledge_base(KB_DIR)}
    assert "faq.md" in sources
    assert "return_policy.txt" in sources
    assert "shipping_info.txt" in sources


def test_ingestion_is_reproducible():
    first = load_knowledge_base(KB_DIR)
    second = load_knowledge_base(KB_DIR)
    assert len(first) == len(second)
    for a, b in zip(first, second):
        assert a.text == b.text
        assert a.source == b.source
        assert a.section == b.section
