import csv
import hashlib
from collections import Counter
from pathlib import Path

import pytest

from services.query.wren_engine import WrenEngine
from services.query.wren_semantic import plan_semantic_sql


CATALOG = Path("data/gold_prompts/EduQuery_Gold_Prompts.csv")
EXPECTED_SHA256 = "8969cc00350a9db84f5494099d116e5b3622368f9163b2da78cc8752c3f48379"
UNSUPPORTED_FAMILIES = {"Cross-table", "SCHOOL_IND_POS_SUB"}


def _rows():
    if not CATALOG.is_file():
        pytest.skip("Protected Daanish gold-prompt catalog is not installed locally.")
    assert hashlib.sha256(CATALOG.read_bytes()).hexdigest() == EXPECTED_SHA256
    with CATALOG.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_daanish_catalog_integrity_and_external_off_planning():
    rows = _rows()
    assert [int(row["Number"]) for row in rows] == list(range(1, 611))
    assert len({row["Prompt"].casefold().strip() for row in rows}) == 610

    engine = WrenEngine()
    outcomes = Counter()
    for row in rows:
        expected_family = row["Table/Family"].split(" / ", 1)[0]
        decision = engine.interpret_local(row["Prompt"])
        outcomes[decision.kind] += 1
        assert decision.kind != "provider_required"
        if expected_family in UNSUPPORTED_FAMILIES:
            assert decision.kind == "unsupported"
            continue
        assert decision.kind == "query"
        assert decision.plan is not None
        assert decision.plan.catalog_family == expected_family.upper()
        semantic_sql, params = engine.compile(decision.plan)
        physical_sql = plan_semantic_sql(semantic_sql)
        assert "dbo." in physical_sql
        assert physical_sql.count("?") == len(params)

    assert outcomes == {"query": 515, "unsupported": 95}
