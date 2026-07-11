#!/usr/bin/env python3
"""Validate the plugin and its portable Agent Skills without dependencies."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_METADATA = ("name", "description", "version", "author", "license")
ALLOWED_METADATA = set(REQUIRED_METADATA)
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse the deliberately narrow scalar-only frontmatter contract."""
    if not text.startswith("---\n"):
        raise ValueError("frontmatter must start on line 1")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter is not closed")

    data: dict[str, str] = {}
    for number, line in enumerate(text[4:end].splitlines(), start=2):
        if not line or line[:1].isspace() or ":" not in line:
            raise ValueError(f"invalid scalar metadata on line {number}")
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in data:
            raise ValueError(f"duplicate metadata key {key!r}")
        if key not in ALLOWED_METADATA:
            raise ValueError(f"unsupported metadata key {key!r}")
        if not value:
            raise ValueError(f"empty metadata value {key!r}")
        if value[:1] in "\"'" and value[-1:] == value[:1]:
            value = value[1:-1]
        data[key] = value
    return data, text[end + 5 :]


def load_json(path: Path, errors: list[str]) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{path.name}: invalid JSON: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{path.name}: root must be an object")
        return None
    return value


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skills_dir = root / "skills"
    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    plugin = load_json(root / ".claude-plugin/plugin.json", errors)
    marketplace = load_json(root / ".claude-plugin/marketplace.json", errors)
    if plugin is not None and marketplace is not None:
        plugins = marketplace.get("plugins")
        entry = plugins[0] if isinstance(plugins, list) and len(plugins) == 1 else None
        if not isinstance(plugin.get("name"), str):
            errors.append("plugin.json: name must be a string")
        if not isinstance(entry, dict):
            errors.append("marketplace.json: plugins must contain exactly one object")
        elif entry.get("name") != plugin.get("name") or entry.get("source") != "./":
            errors.append("marketplace.json: plugin name/source must match plugin.json and './'")

    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir()) if skills_dir.exists() else []
    if not skill_dirs:
        errors.append("skills: expected at least one skill directory")

    seen_names: set[str] = set()
    for directory in skill_dirs:
        path = directory / "SKILL.md"
        rel = path.relative_to(root)
        if not path.is_file():
            errors.append(f"{directory.relative_to(root)}: missing SKILL.md")
            continue
        try:
            text = path.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{rel}: {exc}")
            continue

        missing = [key for key in REQUIRED_METADATA if not meta.get(key)]
        if missing:
            errors.append(f"{rel}: missing {', '.join(missing)}")
        name = meta.get("name", "")
        if not NAME.fullmatch(name) or len(name) > 64:
            errors.append(f"{rel}: name must be <=64 characters of kebab-case")
        if name != directory.name:
            errors.append(f"{rel}: name must match directory")
        if name in seen_names:
            errors.append(f"{rel}: duplicate skill name {name!r}")
        seen_names.add(name)
        if not SEMVER.fullmatch(meta.get("version", "")):
            errors.append(f"{rel}: version must be SemVer x.y.z")
        description = meta.get("description", "")
        if len(description) > 1024 or "Use " not in description:
            errors.append(f"{rel}: description must be <=1024 chars and say when to use it")
        if not body.strip():
            errors.append(f"{rel}: empty body")
        if len(text.splitlines()) > 500:
            errors.append(f"{rel}: SKILL.md exceeds 500 lines; use progressive disclosure")
        if f"/unknowns:{directory.name}" not in readme:
            errors.append(f"{rel}: missing exact README invocation")

        metadata = directory / "agents/openai.yaml"
        if not metadata.is_file():
            errors.append(f"{directory.relative_to(root)}: missing agents/openai.yaml")
        else:
            try:
                ui = metadata.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"{metadata.relative_to(root)}: cannot read UTF-8: {exc}")
                continue
            for key in ("display_name", "short_description", "default_prompt"):
                if not re.search(rf"^  {key}: \"[^\"]+\"$", ui, re.MULTILINE):
                    errors.append(f"{metadata.relative_to(root)}: missing quoted {key}")
            if f"${name}" not in ui:
                errors.append(f"{metadata.relative_to(root)}: default_prompt must mention ${name}")

        portability_checks = (
            ("Artifact tool", ("no Artifact tool", "has no Artifact tool")),
            ("AskUserQuestion", ("plain-text",)),
            ("Skill tool", ("no skill-invocation tool",)),
            ("Glob/Grep/Read", ("equivalent",)),
        )
        for needle, fallbacks in portability_checks:
            if needle in text and not any(fallback in text for fallback in fallbacks):
                errors.append(f"{rel}: {needle!r} needs a portable fallback")

    if "docs/superpowers" in readme:
        errors.append("README.md: stale docs/superpowers path")
    return errors


def main() -> int:
    errors = validate(Path(__file__).resolve().parents[1])
    if errors:
        print("\n".join(errors))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
