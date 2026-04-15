# JuraScraper

**Automated PDF Scraper for German Legal Texts**

JuraScraper retrieves legal texts from [gesetze-im-internet.de](https://www.gesetze-im-internet.de) — the official publication platform for German federal law. It downloads, filters, and organizes statutory texts as PDFs for local reference, research, or downstream processing.

---

## Features

- **Parallel downloads** — concurrent retrieval with configurable throttling to respect server limits
- **CLI filtering** — select laws by abbreviation, topic area, or custom patterns
- **Module self-checks** — built-in validation to detect scraper degradation when the source site changes
- **Structured output** — consistent file naming and directory organization for integration with other tools

## Usage

```bash
python jurascraper.py --filter "StGB" --output ./gesetze/
```

See `--help` for the full set of options.

## Why

German legal texts are publicly available but not conveniently bulk-accessible. Researchers, compliance teams, and legal tech projects need local corpora without manually downloading hundreds of individual PDFs. JuraScraper fills that gap.

## Related

- [RegMon](https://github.com/RiswanHassen/regmon) — Regulatory monitoring for German healthcare IT, using similar scraping infrastructure for G-BA, Gematik, and KBV publications

## License

See [LICENSE](LICENSE) for details.
