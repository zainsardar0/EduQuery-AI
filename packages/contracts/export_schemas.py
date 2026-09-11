import json
import sys
from pathlib import Path

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from packages.contracts.schemas.auth import AuthContext, DemoLoginRequest, TokenResponse
from packages.contracts.schemas.query import QueryRequest, QueryResponse, QueryRefusal
from packages.contracts.schemas.prediction import PredictionRequest, PredictionResponse
from packages.contracts.schemas.policy import PolicyRequest, PolicyResponse
from packages.contracts.schemas.errors import APIError

MODELS = [
    ("AuthContext", AuthContext),
    ("DemoLoginRequest", DemoLoginRequest),
    ("TokenResponse", TokenResponse),
    ("QueryRequest", QueryRequest),
    ("QueryResponse", QueryResponse),
    ("QueryRefusal", QueryRefusal),
    ("PredictionRequest", PredictionRequest),
    ("PredictionResponse", PredictionResponse),
    ("PolicyRequest", PolicyRequest),
    ("PolicyResponse", PolicyResponse),
    ("APIError", APIError),
]


def generate_ts_type(name: str, model_cls) -> str:
    schema = model_cls.model_json_schema()
    props = schema.get("properties", {})
    required = schema.get("required", [])

    lines = [f"export interface {name} {{"]
    for prop_name, prop_data in props.items():
        is_req = prop_name in required
        ts_type = "any"
        p_type = prop_data.get("type")
        if p_type == "string":
            if "enum" in prop_data:
                ts_type = " | ".join(f'"{val}"' for val in prop_data["enum"])
            else:
                ts_type = "string"
        elif p_type in ("integer", "number"):
            ts_type = "number"
        elif p_type == "boolean":
            ts_type = "boolean"
        elif p_type == "array":
            ts_type = "any[]"
        elif p_type == "object":
            ts_type = "Record<string, any>"
        elif "anyOf" in prop_data or "oneOf" in prop_data:
            ts_type = "any"

        opt_flag = "" if is_req else "?"
        lines.append(f"  {prop_name}{opt_flag}: {ts_type};")

    lines.append("}\n")
    return "\n".join(lines)


def export_all():
    dist_dir = Path(__file__).parent / "dist"
    json_dir = dist_dir / "schemas"
    json_dir.mkdir(parents=True, exist_ok=True)

    ts_content = ["// Auto-generated TypeScript definitions for EduQuery AI API Contracts\n"]

    for name, model_cls in MODELS:
        # Write JSON Schema
        schema_path = json_dir / f"{name}.json"
        with open(schema_path, "w", encoding="utf-8") as f:
            json.dump(model_cls.model_json_schema(), f, indent=2)

        # Append TS definition
        ts_content.append(generate_ts_type(name, model_cls))

    ts_path = dist_dir / "types.d.ts"
    with open(ts_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ts_content))

    print(f"Exported {len(MODELS)} schemas to {dist_dir}")


if __name__ == "__main__":
    export_all()
