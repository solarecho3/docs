# Declutter Docs App
Storage for important documents that can be digitized.
- OCR by [pytesseract](https://pypi.org/project/pytesseract/).
- Summary with a [Google T5-3b](https://huggingface.co/google-t5/t5-3b) from [🤗 transformers](https://pypi.org/project/transformers/), using [MLX](https://github.com/ml-explore/mlx) for apple silicon.
- Front-end with [streamlit](https://pypi.org/project/streamlit/).

## What does it do?
Store documents by taking a photo, and find them later with simple text search.

- Optical Character Recognition: [pytesseract](https://pypi.org/project/pytesseract/) Take a photo of a document and the text is scanned, read, and attached as metadata. Can't find your 2022 1098-T tax form? Just search for "1098-T" and see all the documents containing that string.
- Language Model Summarization: [🤗 transformers](https://pypi.org/project/transformers/) A generative-AI summary of the document using a t5 transformer.
- Tags search.
- Image preview.

## Design and Methodology:
I wanted to just go for the most manual, intuitive way to store, index, and query docs without doing a bunch of research and engineering. Just save to the file system, tag and map with JSON, and deliver an MVP.

## Installation:
**Note: the t5 uses mlx for apple silicon and hasn't been tested elsewhere.**
1. From the `modules` directory, run `python convert.py --model t5-3b` to download the model [~11gb+].
2. From the `docs` directory, run `python -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`, `streamlit run app.py`.

## Known Bugs:
- Images need to be cropped or the OCR gets confused.
- The t5 is a standard t5-3b from hugging face's transformers library: https://huggingface.co/docs/transformers/en/index, and isn't tuned.

## Why do this?
Because I'm disorganized and all the apps I tried suck.

## Road map to MVP
- [x] GUI with streamlit.
- [x] Hex tree directory generation and mapping to cloud.
- [x] Out-of-the-box OCR with tesseract.
- [x] Out-of-the-box t5 transformer integration.
- [x] Optimize for t5 inference on Apple silicon so I can host this on my laptop so maybe Ann will use it.
- [ ] Installation script.
- [ ] CI/CD pipeline cleaning.
- [ ] Trie mapping every OCR'd token to any document containing it.
- [ ] Text search and document retrieval via trie mapping.
- [ ] T5 hyperparameteres to config.
- [ ] Fine-tune the T5 to name the document, less to summarize it.
- [ ] Move image previews to the hextree too, of course.
- [ ] Auto-crop for image preprocessing.
- [ ] Port to standard pytorch for use on other hardware.
- [ ] Either truncate inputs or find a model with a longer sequence length. Or, chunk and sum sections of 512 len, and summarize the resulting strings as one.

## Todo:
- Trie search
- Fine-tune t5 model or inference algorithm.
  - Why does terminal results differ from module?
- Add crop to image pre-processing.
- Image previews to hextree.
- Styling and formatting.
- Lazy subdirectory creation.
- Expose T5 configs to front-end.
