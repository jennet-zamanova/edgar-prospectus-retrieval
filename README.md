# SEC EDGAR API to fetch the most recent prospectus

# Setup

[Optional] Create a virtual environment `python3 -m venv .venv`, activate `source .venv/bin/activate` progress in the virtual environment. 

Install requirements:

`pip install -r requirements.txt`

Get free api key at https://sec-api.io/ and add to environment vars

`export EDGAR_API_KEY={EDGAR_API_KEY}` 

# CLI usage

Run the script with symbols (`-s`) and files (`-f`).
Optionally add `--to-pdf` to export results.

```bash
python3 cli.py -s SYMBOL1 SYMBOL2 ... [-f FILE1 FILE2 ...] [--to-pdf]
```

### Arguments

* `-s, --symbols` : One or more fund symbols to validate (e.g. `VTSAX VUSXX`).
* `-f, --files` : (Optional) One or more filenames to save the files as (e.g. `prospectus.htm report.htm`). If not set, symbols are used as filenames.
* `--to-pdf` : (Optional) If set, results downloaded as PDF.

### Example

```bash
python3 cli.py -s VTSAX VUSXX -f prospectus_VTSAX.pdf prospectus_VUSXX.pdf --to-pdf
```

Output in terminal:

```
[INFO] Processing fund: VTSAX
[INFO] Downloading fund: VTSAX
[INFO] Processing fund: VUSXX
[INFO] Downloading fund: VUSXX
Resulting Logs:
| Fund Symbol   | Saved?   | Error   | Link                                     | Filing Date               |
|---------------|----------|---------|------------------------------------------|---------------------------|
| VTSAX         | True     |         | https://www.sec.gov/Archives/edgar/da... | 2025-04-28T17:39:21-04:00 |
| VUSXX         | True     |         | https://www.sec.gov/Archives/edgar/da... | 2024-12-19T17:39:24-05:00 |
```

---

# Assumptions

- Prospectus is filed under form 497K. 
- If symbol is not available in the `company_tickers_mf.json` file then we assume fund does not exist.
  - potential ways to improve: raise the error and give a list of funds that might match based on how close the input is to the available funds. 
- There can be multiple prospectuses filed for a fund in a given time frame while another fund files only one. I.e. fund A filed at 2025-09-01, 2025-09-03, while fund B filed at 2025-08-28. This means pagination would not work since we would 2 prospectuses from A instead of 1 from A and 1 from B.
- Log progress, errors, and final table wth fund + is_saved + error + filing link + filing date
- document date is `filedAt (string) - Represents the Accepted attribute of a filing in ISO 8601 format, and shows the date and time the filing was accepted by the EDGAR system.`


## Design decisions

Prospectus Retriever (interface) [can be any api] -> Edgar Single Prospectus Retriever (class) [specifically using SERC EDGAR api to retrieve one prospectus] -> Edgar Prospectus Retriever (class) [specifically using SERC EDGAR api to retrieve multiple prospectuses]

This way we can implement different APIs + different ways of handling multiple funds.

Input assumptions described in function documentations. (Helper functions that are not meant to be used outside of the class start with underscore _)

### Files:
- prospectus_retriever.py - interface
- edgar_single_prospectus_retriever.py - single file implementation
- edgar_prospectus_retriever.py - multiple files implementation
- cli.py - command line implementation
