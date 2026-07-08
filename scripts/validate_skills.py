#!/usr/bin/env python3
"""Small stdlib validator for portable SKILL.md files."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
README = ROOT / "README.md"


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def frontmatter(text: str) -> tuple[dict[str, str], str] | tuple[None, None]:
    if not text.startswith("---\n"):
        return None, None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, None
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if line and not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data, text[end + 5 :]


def main() -> int:
    errors: list[str] = []

    for rel in [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"]:
        path = ROOT / rel
        if not path.exists():
            fail(errors, f"missing {rel}")
            continue
        try:
            json.loads(path.read_text())
        except Exception as exc:  # noqa: BLE001 - validator should report any parse error
            fail(errors, f"bad json {rel}: {exc}")

    readme = README.read_text() if README.exists() else ""
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        rel = path.relative_to(ROOT)
        text = path.read_text()
        meta, body = frontmatter(text)
        if meta is None or body is None:
            fail(errors, f"{rel}: missing valid frontmatter block")
            continue

        for key in ["name", "description", "version", "author", "license"]:
            if not meta.get(key):
                fail(errors, f"{rel}: missing {key}")
        name = meta.get("name", "")
        if not re.fullmatch(r"[a-z0-9-]+", name):
            fail(errors, f"{rel}: name must be kebab-case")
        if name != path.parent.name:
            fail(errors, f"{rel}: name must match directory")
        if len(meta.get("description", "")) > 1024:
            fail(errors, f"{rel}: description > 1024 chars")
        if not body.strip():
            fail(errors, f"{rel}: empty body")
        if f"skills/{path.parent.name}/SKILL.md" not in readme and f"/unknowns:{path.parent.name}" not in readme:
            fail(errors, f"{rel}: not referenced from README")

        portability_checks = [
            ("Artifact tool", ["no Artifact tool", "has no Artifact tool"]),
            ("AskUserQuestion", ["plain-text"]),
            ("Skill tool", ["no skill-invocation tool"]),
            ("Glob/Grep/Read", ["equivalent"]),
        ]
        for needle, fallbacks in portability_checks:
            if needle in text and not any(fallback in text for fallback in fallbacks):
                fail(errors, f"{rel}: {needle!r} needs a fallback")

    if errors:
        print("\n".join(errors))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
