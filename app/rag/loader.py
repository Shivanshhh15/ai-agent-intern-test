from pathlib import Path
from typing import Any

import yaml


def load_markdown_file(path: str | Path) -> dict[str, Any]:
    path = Path(path)

    text = path.read_text(encoding="utf-8")

    metadata: dict[str, Any] = {}
    content = text

    # Parse YAML front matter when present.
    if text.startswith("---"):
        parts = text.split("---", 2)

        if len(parts) == 3:
            _, front_matter, content = parts
            metadata = yaml.safe_load(front_matter) or {}

    metadata["filename"] = path.name

    return {
        "metadata": metadata,
        "content": content.strip(),
    }


def load_knowledge_base(
    directory: str | Path = "knowledge-base",
) -> list[dict[str, Any]]:

    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(
            f"Knowledge-base directory not found: {directory}"
        )

    documents = []

    for path in sorted(directory.glob("*.md")):
        documents.append(load_markdown_file(path))

    return documents