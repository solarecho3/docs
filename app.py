import os
import tomllib
from typing import Any

import streamlit as st


def configs() -> dict[str, Any]:
    """Load configs from local."""

    default_toml_str = """app-name = "HomeDocs"
app-version = "1.0"
config-version = "0.1"

[app]
page_title = "HomeDocs"
page_icon = ":shark:"
layout = "centered"
"""
    if not os.path.exists("config.toml"):
        with open("config.toml", "w") as f:
            f.write(default_toml_str)
            data = tomllib.loads(default_toml_str)
    else:
        with open("config.toml", "r") as f:
            data = tomllib.loads(f.read())
    return data


config = configs()
st.set_page_config(
    page_title=config['app']['page_title'],
    page_icon=config['app']['page_icon'],
    layout=config['app']['layout'],
)

st.header('Docs uploader')
st.subheader('Upload')
st.file_uploader('Upload doc.')
st.divider()
