import json
import os
import pytest
from services.api.app.services.nl2sql_synthesizer import nl2sql_synthesizer
from services.api.app.adapters.database import db_adapter


def load_all_610_prompts():
    path = os.path.join("data", "semantic", "gold_prompts_610.json")
    if not os.path.exists(path):
        pytest.skip("gold_prompts_610.json not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


GOLD_PROMPTS = load_all_610_prompts()


def test_gold_prompt_catalog_count():
    """Verify that exactly 610 Gold Prompts are loaded."""
    assert len(GOLD_PROMPTS) == 610, f"Expected 610 prompts, got {len(GOLD_PROMPTS)}"


@pytest.mark.parametrize("item", GOLD_PROMPTS)
def test_each_gold_prompt_generates_valid_safe_sql(item):
    """
    Evaluates every single Gold Prompt from 1 to 610.
    Ensures:
    1. SQL is generated.
    2. SQL starts with SELECT or WITH.
    3. SQL passes the strict security validator.
    4. SQL contains NO illegal keywords.
    """
    prompt = item["prompt"]
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert sql, f"Prompt #{item['id']} generated empty SQL"
    assert sql.strip().upper().startswith("SELECT") or sql.strip().upper().startswith("WITH")
    # Validate with AST security engine
    assert db_adapter.validate_sql_safety(sql) is True


def test_sample_gold_prompts_execution_and_summary():
    """Tests sample Gold Prompts across key families for text summary synthesis."""
    sample_tests = [
        ("Show all students of Class 10 Section A in school ATKB for year 26", "ATKB"),
        ("Show pass percentage by subject across all campuses", "ALL"),
        ("Compare school performance across all campuses", "ALL"),
        ("Show all subject marks of roll 7788 in Annual year 26", "ALL"),
        ("Show Physics practical marks of Class 10 ATKB Annual", "ATKB"),
        ("Show annual TR result of teacher EID 105", "ALL")
    ]

    for p, campus in sample_tests:
        results, sql, summary, live_used, ms = db_adapter.execute_nl2sql(p, campus)
        assert len(results) > 0
        assert sql
        assert summary
        assert "Error" not in summary
