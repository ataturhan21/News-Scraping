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

The notebook imports Selenium, Requests, Beautiful Soup, pandas, IPython, OpenAI, and TOML. Spreadsheet exports also need an appropriate Excel writer, including XlsxWriter for the explicit writer calls. No frozen dependency environment is provided.

The scraping cell starts ChromeDriver from `/chromedriver.exe`. Change that path to a compatible local ChromeDriver installation before running. A Chrome or Chromium browser and network access are required. Run the collection and export cells in order.

The **Text Analyzing** section is optional. It reads `OPENAI_KEY` from a local `secrets.toml`, then uses the historical `openai.Completion.create` integration and configured `text-davinci-003` model. OpenAI [retired that model on 2024-01-04](https://developers.openai.com/api/docs/deprecations). That section requires API/model modernization before a new live analysis run; the scraping stages can be inspected independently. Real TOML credential files are excluded by the existing `.gitignore`.

## Output layout

- [`outputs/without detailed content/`](outputs/without%20detailed%20content/): search metadata.
- [`outputs/with detailed content/`](outputs/with%20detailed%20content/): article text and metadata.
- [`outputs/with nlp analysis/`](outputs/with%20nlp%20analysis/): optional extracted fields.

Saved datasets reflect historical runs. A successful local path or syntax check does not validate today's site selectors, completeness of collected articles, or the correctness of extracted entities.

## License

[GNU General Public License v3.0](LICENSE). The repository license does not transfer ownership of the source articles.
