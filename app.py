import re
from typing import Any


HEADING_PATTERN = re.compile(
    r"^(#{1,6})\s+(.+)$"
)


def chunk_markdown(
    content: str,
    metadata: dict[str, Any],
) -> list[dict[str, Any]]:

    lines = content.splitlines()

    chunks = []
    heading_stack: list[str] = []
    current_lines: list[str] = []

    def flush():
        if not current_lines:
            return

        text = "\n".join(
            current_lines
        ).strip()

        if not text:
            return

        chunk_metadata = dict(metadata)

        chunk_metadata["heading"] = (
            " > ".join(heading_stack)
            if heading_stack
            else "Document"
        )

        chunks.append(
            {
                "text": text,
                "metadata": chunk_metadata,
            }
        )

    for line in lines:

        match = HEADING_PATTERN.match(line)

        if match:
            flush()
            current_lines = []

            level = len(match.group(1))
            heading = match.group(2).strip()

            heading_stack[:] = (
                heading_stack[:level - 1]
            )

            heading_stack.append(heading)

        else:
            current_lines.append(line)

    flush()

    return chunks