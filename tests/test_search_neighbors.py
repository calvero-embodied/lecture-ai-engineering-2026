from app import retrieval


def test_search_with_neighbors(monkeypatch):
    def page(doc, number):
        return {
            "page_id": f"{doc}-p{number:03d}",
            "document_id": doc,
            "page": number,
            "content": f"本文{number}",
        }

    pages = [
        page("doc1", 1),
        page("doc1", 2),
        page("doc1", 3),
        page("doc1", 4),
        page("doc2", 1),
    ]

    monkeypatch.setattr(retrieval, "load_pages", lambda: pages)
    monkeypatch.setattr(
        retrieval,
        "search",
        lambda query: [pages[1], pages[2]],
    )

    result = retrieval.search_with_neighbors("テスト")
    ids = [p["page_id"] for p in result]

    assert ids == [
        "doc1-p001",
        "doc1-p002",
        "doc1-p003",
        "doc1-p004",
    ]
    assert len(ids) == len(set(ids))
    assert all(p["document_id"] == "doc1" for p in result)
