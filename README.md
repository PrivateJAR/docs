# docs

Source for [docs.perms.io](https://docs.perms.io), built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Build locally

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python scripts/build_llms_full.py   # regenerate docs/llms-full.txt after changing pages
mkdocs serve                        # or: mkdocs build --strict
```

## Deploy

Pull requests run `mkdocs build --strict` and check that `docs/llms-full.txt` is up to date. Pushes to `main` publish
the site to the `gh-pages` branch with `mkdocs gh-deploy`.
