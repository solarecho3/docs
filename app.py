import io
import os
import uuid
import json
import pathlib
import tomllib

from PIL import Image
from typing import Any
from datetime import datetime

import pandas as pd
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
data_path_root = "data"
"""
    if not os.path.exists("config.toml"):
        with open("config.toml", "w") as f:
            f.write(default_toml_str)
            data = tomllib.loads(default_toml_str)
    else:
        with open("config.toml", "r") as f:
            data = tomllib.loads(f.read())
    return data


def generate_thumbnail(root, thumb_root: str, data: bytes) -> str:
    """Generate thumbnails.

    :returns: thumbnail uuid + \".jpg\""""
    os.makedirs(os.path.join(root, thumb_root), exist_ok=True)
    size = (128, 128)
    thumb_uuid = str(uuid.uuid4())
    with Image.open(io.BytesIO(data)) as f:
        f.thumbnail(size)
        f.save(os.path.join(root, thumb_root, thumb_uuid + ".jpg"), "JPEG")
    return str(os.path.join(root, thumb_root, thumb_uuid)) + ".jpg"


def show_thumbnails():
    pass


def generate_hextree(root: str):
    """Generate a hex tree folder structure.
    :param root:
    """
    # os.makedirs(pathlib.Path(root), exist_ok=True)
    for i in [hex(x)[2:] for x in range(0, 16)]:
        for j in [hex(x)[2:] for x in range(0, 16)]:
            for k in [hex(x)[2:] for x in range(0, 16)]:
                os.makedirs(pathlib.PurePath(root, str(i), str(j), str(k)), exist_ok=True)


def find_all_files(root):
    import glob
    files = glob.glob('root/**/*.jpg', recursive=True)
    return files


def query_hextree(filename: str):
    """Query the data hex tree directory."""
    pass


def map_hextree(root: str, map_path: str):
    """Map the data hex tree."""

    # TODO: Save a default map JSON if none exists
    # TODO: The root is the data path root
    # TODO: The map path is from the configs; path to JSON

    if not os.path.exists(os.path.join(root, map_path)):
        pass


def jpg_to_hextree(root: str, data: bytes, metadata: dict):
    """Save an image to hex tree directory."""
    new_uid = uuid.uuid4()
    _file = str(new_uid) + ".jpg"
    metadata["uuid"] = str(new_uid)
    metadata["extension"] = ".jpg"
    _first = _file[0]
    _second = _file[1]
    _third = _file[2]
    file_path = pathlib.Path(root, _first, _second, _third, _file)
    metadata["full_path"] = str(file_path)
    metadata["upload_time"] = datetime.isoformat(datetime.utcnow())
    metadata["upload_time_zone"] = "utc"
    metadata["thumbnail"] = generate_thumbnail(root, 'previews', data)

    with open(file_path, "wb") as img:
        img.write(data)

    # create new empty
    map_root = str(pathlib.Path(root, 'map.json'))
    if not os.path.exists(map_root):
        with open(map_root, "w") as f:
            json.dump({}, f)

    # read
    with open(map_root, "r") as map_file:
        map_data = json.load(map_file)

    map_data[len(map_data.keys())] = metadata

    with open(map_root, "w") as map_file:
        json.dump(map_data, map_file)

    st.success(f'Wrote image to hex: {file_path}')


config = configs()
DATA_PATH_ROOT = config['app']['data_path_root']

st.set_page_config(
    page_title=config['app']['page_title'],
    page_icon=config['app']['page_icon'],
    layout=config['app']['layout'],
)

if not os.path.exists(DATA_PATH_ROOT):
    generate_hextree(DATA_PATH_ROOT)

st.header('Docs uploader')
st.subheader('Upload')
st_file_uploader = st.file_uploader('New image', type='jpg', accept_multiple_files=False)
st_file_uploader_description = st.text_input('Tags', placeholder='\"2023 1099 tax form\"...')
st_file_uploader_submit = st.button('Upload')
st.divider()

if st_file_uploader_submit:
    bytes_data = st_file_uploader.getvalue()

    attach_metadata = dict(
        original_filename=st_file_uploader.name,
        tags=st_file_uploader_description,
    )
    jpg_to_hextree(DATA_PATH_ROOT, bytes_data, attach_metadata)


df_dir_map = pd.read_json(DATA_PATH_ROOT + '/map.json').T
st.subheader('Files in tree')

st.dataframe(df_dir_map, use_container_width=True)

##### show thumbnails #####
st.caption('Thumbnails')
thumb_col1, thumb_col2 = st.columns(2)
for i in df_dir_map['thumbnail']:
    with open(i) as f:
        with thumb_col1:
            st.write(i)
        with thumb_col2:
            st.image(Image.open(i), use_column_width=True)

