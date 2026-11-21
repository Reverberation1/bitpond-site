# Bit Pond — website

`bitpond.io` redirects to **https://kester.world/**. It is served by GitHub Pages
from the root of `main`.

## Structure

```
index.html          Redirect stub
paperless.html      Redirect stub (old /paperless URL)
404.html            Redirect stub for every other path
assets/favicon.svg  Favicon used by the stubs
CNAME               Custom domain (bitpond.io)
.nojekyll           Serve files as-is; skip Jekyll processing
tests/              pytest checks for the stubs
```

Each stub is plain HTML with no JavaScript: `<meta http-equiv="refresh">` to
`https://kester.world/`, `rel=canonical`, `noindex` and a visible fallback link.
Keep `CNAME`: removing it unbinds `bitpond.io` from this repo and breaks the
redirect. DNS, including email forwarding, is managed at the registrar and is
not part of this repo.

## Tests

```bash
python -m pytest -q tests
```
