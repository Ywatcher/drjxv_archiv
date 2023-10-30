# -*- coding: utf-8 -*-

import yaml
from typing import Optional
from bs4.element import Tag


def to_markdown(
    metadata: dict,
    content: str,
    title: Optional[str] = None
):
    metadata_yaml = yaml.dump(metadata)
    metadata_field_str = f"---\n{metadata_yaml}---\n"
    title_field_str = f"# {title}\n---\n" if title is not None else ""
    return metadata_field_str + title_field_str + content


def tags_to_str(tags:list[Tag])-> str:
    return "\n".join([str(t)for t in tags])
