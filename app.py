import io
import os
import uuid
import json
import pathlib
import tomllib

from PIL import Image
from typing import Any
from datetime import datetime

import cv2
import pytesseract
import pandas as pd
import streamlit as st


def configs() -> dict[str, Any]:
    """Load configs from local or make new."""

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


def show_thumbnails(root):
    df_dir_map = pd.read_json(root + '/map.json').T
    st.dataframe(df_dir_map, use_container_width=True)

    ##### show thumbnails #####
    st.caption('Thumbnails')
    for i in df_dir_map.iterrows():
        with open(i[1]['thumbnail']) as f:
            with st.container(border=True):
                thumb_col1, thumb_col2 = st.columns([5, 2])
                with thumb_col1:
                    st.dataframe(i[1])
                with thumb_col2:
                    st.image(Image.open(i[1]["thumbnail"]), width=128, use_column_width="never")
                    with open(i[1]["full_path"], "rb") as file:
                        st.download_button(
                            label="save",
                            data=file,
                            file_name=i[1]["original_filename"].split("/")[-1],
                            mime=f"image/{i[1]['full_path'].split('/')[-1]}.split('.')[-1]",
                            key=uuid.uuid4()
                        )
                    st.button("delete", key=uuid.uuid4())


def generate_hextree(root: str):
    """Generate a hex tree folder structure.
    :param root:
    """
    for i in [hex(x)[2:] for x in range(0, 16)]:
        for j in [hex(x)[2:] for x in range(0, 16)]:
            for k in [hex(x)[2:] for x in range(0, 16)]:
                os.makedirs(pathlib.PurePath(root, str(i), str(j), str(k)), exist_ok=True)


def find_all_files(root):
    import glob
    files = glob.glob(f'{root}/**/*.jpg', recursive=True)
    return files


def query_hextree(filename: str):
    """Query the data hex tree directory."""
    # TODO: Store the set of all OCR'd words
    # in a trie. The leaf node will map to
    # the index of each document that contain
    # the word.

    pass


def map_hextree(root: str, map_path: str):
    """Map the data hex tree."""
    # TODO: Save a default map JSON if none exists
    # TODO: The root is the data path root
    # TODO: The map path is from the configs; path to JSON

    if not os.path.exists(os.path.join(root, map_path)):
        pass


def preprocess_img_and_save(file_path):
    # grayscale the image
    # TODO: just do this operation on the bytes
    img = cv2.imread(str(file_path))
    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply adaptive threshold on gray img
    threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 15)

    # apply white where threshold is white to a copy
    result = img.copy()
    result[threshold == 255] = (255, 255, 255)

    # save the copy
    cv2.imwrite(str(file_path), threshold)


def generate_thumbnail_bytes(root, thumb_root: str, data: bytes) -> str:
    """Generate thumbnails.

    :returns: thumbnail uuid + \".jpg\""""
    os.makedirs(os.path.join(root, thumb_root), exist_ok=True)

    size = (128, 128)
    thumb_uuid = str(uuid.uuid4())

    with Image.open(io.BytesIO(data)) as f:
        f.thumbnail(size)
        f.save(os.path.join(root, thumb_root, thumb_uuid + ".jpg"), "JPEG")

    # returns the path to the thumbnail as str
    return str(os.path.join(root, thumb_root, thumb_uuid)) + ".jpg"


def generate_thumbnail_from_file(root, thumb_root: str, file_path: pathlib.Path) -> str:
    """Generate thumbnails.

    Arguments
    ---------
    file_path : pathlib.Path - The path-like object to the file, for thumb-nailing.

    :returns: thumbnail uuid + \".jpg\""""
    os.makedirs(os.path.join(root, thumb_root), exist_ok=True)
    size = (128, 128)
    thumb_uuid = str(uuid.uuid4())

    with Image.open(file_path) as f:
        f.thumbnail(size)
        f.save(os.path.join(root, thumb_root, thumb_uuid + ".jpg"), "JPEG")

    # returns the path to the thumbnail as str
    return str(os.path.join(root, thumb_root, thumb_uuid)) + ".jpg"


def scan_image(root: str, data: bytes, metadata: dict):
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

    with open(file_path, "wb") as img:
        img.write(data)

    # scan, preprocess, map, thumbnail, and save the img
    preprocess_img_and_save(file_path)
    metadata["thumbnail"] = generate_thumbnail_from_file(root, 'previews', file_path)

    # generate OCR with tesseract
    ocr_str = pytesseract.image_to_string(Image.open(str(file_path)))
    metadata["ocr_string"] = ocr_str

    # # some text cleaning
    # from nltk.corpus import stopwords
    #
    # def remove_stopwords(tokens):
    #     stop_words = set(stopwords.words('english'))
    #     filtered_tokens = [word for word in tokens if word not in stop_words]
    #     return filtered_tokens
    # # TODO: test removing stop words

    # t5 inference here
    import modules.t5 as t5
    metadata["t5_summary"] = t5.summarize(ocr_str)

    # create new empty database mapping if not exist
    map_root = str(pathlib.Path(root, 'map.json'))
    if not os.path.exists(map_root):
        with open(map_root, "w") as f:
            json.dump({}, f)

    # read in database mapping
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
upload_col1, upload_col2 = st.columns([5, 2])
st_file_uploader = st.file_uploader('New image', type='jpg', accept_multiple_files=False)
st_file_uploader_description = st.text_input('Manual tags', placeholder='\"2023 1099 tax form\"...')
st_file_uploader_submit = st.button('Upload')
st.divider()

# upload an image to the database
if st_file_uploader_submit:
    bytes_data = st_file_uploader.getvalue()

    attach_metadata = dict(
        original_filename=st_file_uploader.name,
        tags=st_file_uploader_description,
    )
    scan_image(DATA_PATH_ROOT, bytes_data, attach_metadata)

##### metadata and display #####
try:
    show_thumbnails(DATA_PATH_ROOT)
except FileNotFoundError:
    pass
