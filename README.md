# News Scraping

A research notebook for collecting Turkish news search results, extracting article text, and exporting tabular datasets. The implemented source is Hürriyet; selectors and URL construction are specific to that site.

**[Open the notebook](News%20Scraping.ipynb)** · **[Browse saved outputs](outputs/)**

## Workflow

| Stage | Input | Output |
| --- | --- | --- |
| Collect news URLs | Keywords, date range, category, and search pages | URL, title, abstract, and publication date |
| Collect article text | Saved search results | Search metadata plus `long-content` |
| Optional text analysis | Detailed article records and an API credential | Structured information extracted from article text |

Search results, detailed content, and NLP analysis now use separate output paths. The notebook creates their parent directories before export.

## Configure a run

Start Jupyter from the repository root and open `News Scraping.ipynb`. In **Constants**, review:

- `KEYWORDS` and `LOGIC`: search terms and their combination.
- `START_DATE` and `FINISH_DATE`: the search interval.
- `MAIN_CATEGORY`: the Hürriyet category.
- Generated CSV and XLSX paths: keep separate run outputs when changing the parameters.

The committed example searches 2016 records. It is a reproducible configuration example, not a claim that the current website returns the same records.

## Environment and execution

Install the pinned notebook environment (verified offline with Python 3.12):

```bash
python -m pip install -r requirements.txt
```

It covers Selenium, Requests and Beautiful Soup (used by `article_content.py`), pandas, IPython, TOML, XlsxWriter for the spreadsheet exports, and OpenAI 0.28.1, the last line that provides the `openai.Completion` API the notebook calls.

The scraping cell starts Chrome through `webdriver.Chrome`. Set the `CHROMEDRIVER_PATH` environment variable to use a specific ChromeDriver; otherwise Selenium Manager locates a compatible driver. A Chrome or Chromium browser and network access are required. Run the collection and export cells in order.

The **Text Analyzing** section is optional. It reads `OPENAI_KEY` from a local `secrets.toml`, then uses the historical `openai.Completion.create` integration and configured `text-davinci-003` model. OpenAI [retired that model on 2024-01-04](https://developers.openai.com/api/docs/deprecations). That section requires API/model modernization before a new live analysis run; the scraping stages can be inspected independently. Real TOML credential files are excluded by the existing `.gitignore`.

## Output layout

- [`outputs/without detailed content/`](outputs/without%20detailed%20content/): search metadata.
- [`outputs/with detailed content/`](outputs/with%20detailed%20content/): article text and metadata.
- [`outputs/with nlp analysis/`](outputs/with%20nlp%20analysis/): optional extracted fields.

Saved datasets reflect historical runs. A successful local path or syntax check does not validate today's site selectors, completeness of collected articles, or the correctness of extracted entities.

## Offline regression checks

CI runs these checks with Python 3.10 and only `beautifulsoup4` installed:

```bash
python -m pip install beautifulsoup4==4.12.3
python -m unittest discover -s tests -v
```

Tests use local HTML and fake responses, and check the generated search URL
query. Article downloads use a 30-second
request timeout, reject HTTP failures, and support both committed content
selectors. Rerunning the NLP processing cell resets its results rather than
appending duplicate answers, and rows without article text are recorded as
`no content` without a provider call. The optional NLP provider calls remain a live
integration and are not exercised by these tests.

## License

[MIT](LICENSE). The repository license does not transfer ownership of the source articles.
