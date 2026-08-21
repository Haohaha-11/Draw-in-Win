"""Dependency-free static health checks for the Draw-in-Win repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "docs" / "CATALOG.md",
    ROOT / "docs" / "REPRODUCIBILITY.md",
    ROOT / "requirements.txt",
)
PROHIBITED_SUFFIXES = {".ttf", ".otf"}
SECRET_PATTERN = re.compile(
    r"(?:ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|api[_-]?key\s*=|password\s*=)",
    re.IGNORECASE,
)
ABSOLUTE_PATH_PATTERN = re.compile(
    r"(?<!https)(?<!http)(?:[A-Za-z]:[\\/](?:Users|home|MCM_Codes|UESTC)|/Users/|/home/)"
)
MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[[^]]*]\(([^)]+)\)")


def text_files() -> list[Path]:
    suffixes = {".py", ".R", ".md", ".txt", ".html", ".yml", ".yaml"}
    return [path for path in ROOT.rglob("*") if path.is_file() and path.suffix in suffixes]


def check_python_syntax(errors: list[str]) -> int:
    count = 0
    for path in sorted(ROOT.rglob("*.py")):
        if ".git" in path.parts:
            continue
        count += 1
        try:
            source = path.read_text(encoding="utf-8-sig")
            compile(source, str(path), "exec")
        except (OSError, SyntaxError, UnicodeError) as exc:
            errors.append(f"Python syntax/read error in {path.relative_to(ROOT)}: {exc}")
    return count


def check_required_files(errors: list[str]) -> None:
    for path in REQUIRED_FILES:
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")


def check_prohibited_files(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in PROHIBITED_SUFFIXES:
            errors.append(f"Prohibited redistributable font file: {path.relative_to(ROOT)}")


def check_text(errors: list[str]) -> int:
    count = 0
    for path in text_files():
        if ".git" in path.parts:
            continue
        if path == Path(__file__).resolve():
            continue
        count += 1
        try:
            content = path.read_text(encoding="utf-8-sig")
        except UnicodeError as exc:
            errors.append(f"UTF-8 read error in {path.relative_to(ROOT)}: {exc}")
            continue
        if SECRET_PATTERN.search(content):
            errors.append(f"Possible credential in {path.relative_to(ROOT)}")
        if path.suffix in {".py", ".R"} and ABSOLUTE_PATH_PATTERN.search(content):
            errors.append(f"Machine-specific absolute path in {path.relative_to(ROOT)}")
    return count


def check_readme_images(errors: list[str]) -> int:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    count = 0
    for raw_target in MARKDOWN_IMAGE_PATTERN.findall(readme):
        if raw_target.startswith(("https://", "http://")):
            continue
        count += 1
        target = (ROOT / raw_target.split("#", 1)[0]).resolve()
        if not target.is_file():
            errors.append(f"Broken README image: {raw_target}")
    return count


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_prohibited_files(errors)
    python_count = check_python_syntax(errors)
    text_count = check_text(errors)
    image_count = check_readme_images(errors)

    print(
        f"Checked {python_count} Python files, {text_count} text files, "
        f"and {image_count} local README images."
    )
    if errors:
        print("Repository checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("All repository checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
