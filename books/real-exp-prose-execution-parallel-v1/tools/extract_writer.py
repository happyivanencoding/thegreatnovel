"""Extract the production Writer artifact into experiment-local evidence files."""

from __future__ import annotations

import argparse
from pathlib import Path

from story_mvp.hybrid_runtime import extract_final_chapter_artifact
from story_mvp.storage import validate_chapter_body_for_save


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("response", type=Path)
    parser.add_argument("body", type=Path)
    parser.add_argument("summary", type=Path)
    args = parser.parse_args()
    response = args.response.read_text(encoding="utf-8")
    artifact = extract_final_chapter_artifact(response)
    if artifact is None:
        raise SystemExit("Writer response 缺少 # 正式正文 区块")
    body, summary = artifact
    validate_chapter_body_for_save(body)
    args.body.write_text(body.strip() + "\n", encoding="utf-8")
    args.summary.write_text(summary.strip() + "\n", encoding="utf-8")
    print(f"body={args.body}")
    print(f"body_chars={len(body)}")
    print(f"summary={args.summary}")
    print(f"summary_chars={len(summary)}")


if __name__ == "__main__":
    main()
