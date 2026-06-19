from __future__ import annotations

import argparse
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

try:
    from pyeda.boolalg.expr import expr
except ImportError:  # pragma: no cover - user-facing dependency hint
    print("PyEDA is required. Install it with:\npython -m pip install pyeda", file=sys.stderr)
    raise SystemExit(1)


ISSUE_COLUMNS = [
    "zip_file",
    "model_file",
    "line_number",
    "node",
    "original_rule",
    "normalized_rule",
    "simplified_result",
    "issue_type",
    "error_message",
]

INVALID_MODEL_COLUMNS = ["zip_file", "model_file", "model_id", "n_issues"]
VALID_MODEL_COLUMNS = ["zip_file", "model_file", "model_id"]
SUMMARY_COLUMNS = ["metric", "value"]


@dataclass
class RuleValidation:
    normalized_rule: str
    simplified_result: str
    issue_type: str | None
    error_message: str


def parse_bnet_line(line: str, line_number: int):
    stripped = line.strip()
    if not stripped:
        return None
    if stripped.startswith("#") or stripped.startswith("//"):
        return None

    if "," not in stripped:
        raise ValueError("Missing comma separator between target and rule")

    target, rule = stripped.split(",", 1)
    node = target.strip()
    rule = rule.strip()
    if not node or not rule:
        raise ValueError("Missing target node or rule")
    if node.lower() == "targets":
        return None
    return node, rule


def normalize_rule(rule: str) -> str:
    return rule.strip().replace("!", "~")


def validate_rule(rule: str) -> RuleValidation:
    normalized_rule = normalize_rule(rule)
    try:
        simplified = expr(normalized_rule).simplify()
    except Exception as exc:
        return RuleValidation(
            normalized_rule=normalized_rule,
            simplified_result="",
            issue_type="parse_error",
            error_message=str(exc),
        )

    simplified_result = str(simplified)
    if hasattr(simplified, "is_one") and simplified.is_one():
        return RuleValidation(normalized_rule, simplified_result, "tautology", "")
    if hasattr(simplified, "is_zero") and simplified.is_zero():
        return RuleValidation(normalized_rule, simplified_result, "contradiction", "")
    return RuleValidation(normalized_rule, simplified_result, None, "")


def scan_zip(zip_path: Path, limit_models: int | None = None):
    zip_file = zip_path.name
    print(f"Scanning {zip_file}")

    issue_rows = []
    model_rows = []
    n_rules_checked = 0
    n_parse_errors = 0

    try:
        with zipfile.ZipFile(zip_path) as zf:
            model_files = sorted(name for name in zf.namelist() if name.lower().endswith(".bnet"))
            if limit_models is not None:
                model_files = model_files[:limit_models]
            for model_file in model_files:
                model_id = f"{zip_file}::{model_file}"
                n_issues = 0
                try:
                    raw_text = zf.read(model_file).decode("utf-8", errors="replace")
                except Exception as exc:
                    print(f"  ! Could not read {model_file}: {exc}")
                    continue

                for line_number, line in enumerate(raw_text.splitlines(), start=1):
                    try:
                        parsed = parse_bnet_line(line, line_number)
                    except ValueError as exc:
                        n_rules_checked += 1
                        n_issues += 1
                        n_parse_errors += 1
                        issue_rows.append(
                            {
                                "zip_file": zip_file,
                                "model_file": model_file,
                                "line_number": line_number,
                                "node": "",
                                "original_rule": line.strip(),
                                "normalized_rule": "",
                                "simplified_result": "",
                                "issue_type": "parse_error",
                                "error_message": str(exc),
                            }
                        )
                        continue

                    if parsed is None:
                        continue

                    node, rule = parsed
                    n_rules_checked += 1
                    validation = validate_rule(rule)
                    if validation.issue_type is None:
                        continue

                    n_issues += 1
                    if validation.issue_type == "parse_error":
                        n_parse_errors += 1
                    issue_rows.append(
                        {
                            "zip_file": zip_file,
                            "model_file": model_file,
                            "line_number": line_number,
                            "node": node,
                            "original_rule": rule,
                            "normalized_rule": validation.normalized_rule,
                            "simplified_result": validation.simplified_result,
                            "issue_type": validation.issue_type,
                            "error_message": validation.error_message,
                        }
                    )

                model_rows.append(
                    {
                        "zip_file": zip_file,
                        "model_file": model_file,
                        "model_id": model_id,
                        "n_issues": n_issues,
                    }
                )
    except zipfile.BadZipFile as exc:
        print(f"  ! Skipping unreadable ZIP {zip_file}: {exc}")

    return {
        "zip_file": zip_file,
        "issue_rows": issue_rows,
        "model_rows": model_rows,
        "n_rules_checked": n_rules_checked,
        "n_parse_errors": n_parse_errors,
    }


def write_reports(results, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    issue_rows = []
    model_rows = []
    n_rules_checked = 0
    n_parse_errors = 0

    for result in results:
        issue_rows.extend(result["issue_rows"])
        model_rows.extend(result["model_rows"])
        n_rules_checked += result["n_rules_checked"]
        n_parse_errors += result["n_parse_errors"]

    issue_df = pd.DataFrame(issue_rows, columns=ISSUE_COLUMNS)
    model_df = pd.DataFrame(model_rows, columns=INVALID_MODEL_COLUMNS)

    invalid_model_df = model_df[model_df["n_issues"] > 0].copy() if not model_df.empty else pd.DataFrame(columns=INVALID_MODEL_COLUMNS)
    valid_model_df = model_df[model_df["n_issues"] == 0][VALID_MODEL_COLUMNS].copy() if not model_df.empty else pd.DataFrame(columns=VALID_MODEL_COLUMNS)
    invalid_model_df = invalid_model_df[INVALID_MODEL_COLUMNS] if not invalid_model_df.empty else pd.DataFrame(columns=INVALID_MODEL_COLUMNS)
    valid_model_df = valid_model_df[VALID_MODEL_COLUMNS] if not valid_model_df.empty else pd.DataFrame(columns=VALID_MODEL_COLUMNS)

    issue_path = out_dir / "oris_preflight_rule_issues.csv"
    invalid_path = out_dir / "oris_invalid_models.csv"
    valid_path = out_dir / "oris_valid_models.csv"
    summary_path = out_dir / "oris_preflight_summary.csv"

    issue_df.to_csv(issue_path, index=False)
    invalid_model_df.to_csv(invalid_path, index=False)
    valid_model_df.to_csv(valid_path, index=False)

    n_models_scanned = len(model_df)
    n_issue_rules = len(issue_df)
    n_invalid_models = len(invalid_model_df)
    n_valid_models = len(valid_model_df)

    summary_rows = [
        ("n_zip_files_scanned", len(results)),
        ("n_models_scanned", n_models_scanned),
        ("n_rules_checked", n_rules_checked),
        ("n_issue_rules", n_issue_rules),
        ("n_invalid_models", n_invalid_models),
        ("n_valid_models", n_valid_models),
        ("n_parse_errors", n_parse_errors),
    ]
    pd.DataFrame(summary_rows, columns=SUMMARY_COLUMNS).to_csv(summary_path, index=False)

    print(f"  Wrote {issue_path.name}")
    print(f"  Wrote {invalid_path.name}")
    print(f"  Wrote {valid_path.name}")
    print(f"  Wrote {summary_path.name}")


def main():
    parser = argparse.ArgumentParser(description="Scan Oris/Gitsbe ZIP files for preflight rule issues")
    parser.add_argument("input_dir", help="Folder containing model ZIP files")
    parser.add_argument("--out", default="preflight_results", help="Output folder for CSV reports")
    parser.add_argument("--limit-zips", type=int, default=None, help="Limit the number of ZIP files scanned")
    parser.add_argument("--limit-models", type=int, default=None, help="Limit the number of .bnet models scanned per ZIP")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    out_dir = Path(args.out)

    if not input_dir.is_dir():
        print(f"Input folder does not exist: {input_dir}", file=sys.stderr)
        raise SystemExit(1)

    zip_paths = sorted(input_dir.glob("*.zip"))
    if args.limit_zips is not None:
        zip_paths = zip_paths[: args.limit_zips]

    print(f"Found {len(zip_paths)} ZIP file(s) in {input_dir}")

    results = []
    for zip_path in zip_paths:
        result = scan_zip(zip_path, limit_models=args.limit_models)
        results.append(result)

    write_reports(results, out_dir)


if __name__ == "__main__":
    main()
