# OpenAI-docs

Unofficial Markdown mirror of OpenAI's first-party developer documentation,
generated from the official `llms.txt` indexes.

The snapshot is reproducible:

```bash
python scripts/sync_docs.py
```

The sync starts at `https://developers.openai.com/llms.txt`, discovers every
linked documentation-set `llms.txt`, and mirrors English Markdown pages from
official OpenAI documentation hosts. Raw indexes are retained under `indexes/`
and pages are stored under `docs/<host>/` with their URL paths preserved.

This repository is not affiliated with or endorsed by OpenAI.
