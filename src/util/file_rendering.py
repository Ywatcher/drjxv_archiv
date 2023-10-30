# -*- coding: utf-8 -*-

import yaml
from typing import Optional
from bs4.element import Tag


def to_markdown(
    metadata: dict,
    content: str,
    title: Optional[str] = None
):
    """
    to render a markdown string from given fields,
    output will be like:
        ---
        [metadata](yaml)
        ---
        # [title](if any)
        ---
        [content](usually html-like)
    """
    metadata_yaml = yaml.dump(metadata)
    metadata_field_str = f"---\n{metadata_yaml}---\n"
    title_field_str = f"# {title}\n---\n" if title is not None else ""
    return metadata_field_str + title_field_str + content


def tags_to_str(tags: list[Tag]) -> str:
    """
    concatenate a list of web element tags
    to an html string,
    for example, a tag could be `<p>...<\\p>`,
    output will be like:
        [element tag 1]
        [element tag 2]
        ...
    """
    return "\n".join([str(t)for t in tags])


def to_config_file(
    owner_name: str,
    owner_email: str
) -> str:
    config_dict = {
        "owner_name": owner_name,
        "owner_email": owner_email
    }
    config_yaml = yaml.dump(config_dict)
    return config_yaml
