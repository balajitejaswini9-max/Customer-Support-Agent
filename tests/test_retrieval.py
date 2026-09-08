from pathlib import Path

import pytest

from src.ingestion import load_knowledge_base
from src.retrieval import RETRIEVAL_THRESHOLD, TOP_K, retrieve
from src.vector_store import VectorStore

KB_DIR = Path(__file__).parent.parent / "knowledge_base"


@pytest.fixture(scope="module")
def store() -> VectorStore:
    chunks = load_knowledge_base(KB_DIR)
    s = VectorStore()
    s.add_documents(chunks)
    return s


def test_result_count_bounded(store: VectorStore):
    result = retrieve("return policy", store, k=TOP_K)
    assert len(result.chunks) <= TOP_K


def test_source_metadata_preserved(store: VectorStore):
    result = retrieve("how long does shipping take", store)
    for chunk in result.chunks:
        assert chunk.source
        assert chunk.section


def test_scores_and_chunks_same_length(store: VectorStore):
    result = retrieve("payment methods", store)
    assert len(result.chunks) == len(result.scores)


def test_relevant_query_passes_guard(store: VectorStore):
    result = retrieve("What is the return policy?", store)
    assert result.passed_guard, (
        f"Expected retrieval guard to pass for a relevant query; "
        f"top score was {result.scores[0] if result.scores else 'N/A'}"
    )


def test_relevant_scores_higher_than_irrelevant(store: VectorStore):
    relevant = retrieve("How long does standard shipping take?", store)
    irrelevant = retrieve("How do I bake a chocolate cake?", store)
    if relevant.scores and irrelevant.scores:
        assert relevant.scores[0] > irrelevant.scores[0]


def test_embedding_dimension_produces_consistent_results(store: VectorStore):
    r1 = retrieve("cancel my order", store)
    r2 = retrieve("cancel my order", store)
    assert r1.scores == r2.scores
    assert [c.source for c in r1.chunks] == [c.source for c in r2.chunks]
