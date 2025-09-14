#!/usr/bin/env python3
import argparse
import os
from tabulate import tabulate

from edgar_prospectus_retriever import EdgarProspectusRetriever

def shorten(text: str, max_len: int = 40) -> str:
    """Truncate long text with ellipsis."""
    return text if len(text) <= max_len else text[:max_len-3] + "..."

def hyperlink(label: str, url: str) -> str:
    """Make a clickable ANSI hyperlink with truncated label."""
    return f"\033]8;;{url}\033\\{label}\033]8;;\033\\"


def main():
    parser = argparse.ArgumentParser(description="Accept multiple fund symbols and filenames")
    parser.add_argument(
        "-s", "--symbols",
        nargs="+",
        required=True,
        help="Fund symbols (e.g. SPY, QQQ, VTSAX)"
    )
    parser.add_argument(
        "-f", "--files",
        nargs="+",
        required=False,
        help="Filenames to process (e.g. file1.pdf file2.pdf)"
    )
    parser.add_argument(
        "--to-pdf",
        action="store_true",
        help="Convert results to PDF"
    )
    args = parser.parse_args()

    API_KEY = os.getenv('EDGAR_API_KEY')

    retriever = EdgarProspectusRetriever(API_KEY)

    if args.to_pdf:
        results = retriever.retrieve_prospectuses_as_pdfs(args.symbols, args.files)
    else:
        results = retriever.retrieve_prospectuses(args.symbols, args.files)

    # Print results as table
    headers = ["Fund Symbol", "Saved?", "Error", "Link", "Filing Date"]
    table = [
        [r["fund_symbol"], r["is_successfully_saved"], r["error"] or "", hyperlink(shorten(r["url"] or "", 40), r["url"] or ""), r["date"] or ""] 
        for r in results
    ]
    print("Resulting Logs: ")
    print(tabulate(table, headers=headers, tablefmt="github"))


if __name__ == "__main__":
    main()
