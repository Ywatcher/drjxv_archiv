import yaml
from typing import Optional


def to_markdown(
    metadata: dict,
    content: str,
    title: Optional[str] = None
):
    metadata_yaml = yaml.dump(metadata)
    metadata_field_str = f"---\n{metadata_yaml}---\n"
    title_field_str = f"# {title}\n---\n" if title is not None else ""
    return metadata_field_str + title_field_str + content
