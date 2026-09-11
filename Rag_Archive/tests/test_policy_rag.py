from services.query.policy_ingest import markdown_policy_chunks, parse_policy_text_into_chunks
from services.query.rag_store import PolicyRAGEngine


def test_policy_rag_provenance_and_release_state():
    readiness = PolicyRAGEngine().readiness()
    assert readiness["provenance_verified"] is True
    assert readiness["release_eligible"] is False
    assert readiness["records"] == 144
    assert readiness["source_count"] == 9
    assert all(source["source_format"] == "markdown" for source in readiness["sources"])


def test_policy_rag_sibling_admission_has_markdown_line_source():
    sections, explanation, status = PolicyRAGEngine().search("How can siblings be given admission?")
    assert status == "found"
    assert any(section["artifact_id"] == "POL-003" and section["source_location"].startswith("lines ") for section in sections)
    assert all(len(section["source_sha256"]) == 64 for section in sections)
    assert "Decision Regarding Admission" in explanation


def test_policy_rag_abstains_for_unsupported_transport_policy():
    sections, explanation, status = PolicyRAGEngine().search(
        "What transport policy applies to Daanish School buses?"
    )
    assert status == "not_found"
    assert sections == []
    assert "No sufficiently relevant" in explanation


def test_semantic_policy_ingest_chunking():
    raw_text = """--- Page 1 ---
Section 1.1 - Emergency Response
School emergency protocols must be activated by the campus principal immediately.
--- Page 2 ---
Section 1.2 - Fire Safety Inspection
Annual fire safety checks are conducted in January.
"""
    chunks = parse_policy_text_into_chunks(raw_text, "Emergency_Policy.pdf")
    assert len(chunks) == 2
    assert chunks[0]["section_title"] == "Section 1.1 - Emergency Response"
    assert chunks[0]["page"] == 1
    assert chunks[1]["section_title"] == "Section 1.2 - Fire Safety Inspection"
    assert chunks[1]["page"] == 2


def test_markdown_policy_ingest_keeps_declared_page_and_never_invents_one():
    chunks = markdown_policy_chunks(
        "First policy paragraph.\n\n--- Page 7 ---\nSecond policy paragraph.",
        "POL-999", "Example Policy.md", "A" * 64,
    )
    assert chunks[0]["source_location"] == "lines 1-1"
    assert chunks[0]["page"] == 0
    assert chunks[1]["source_location"] == "lines 4-4; declared source page 7"
    assert chunks[1]["page"] == 7
