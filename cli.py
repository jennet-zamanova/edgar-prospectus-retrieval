#!/usr/bin/env python3
import argparse
import os
from tabulate import tabulate

from edgar_prospectus_retriever import EdgarProspectusRetriever

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
        [r["fund_symbol"], r["is_successfully_saved"], r["error"] or "", r["url"] or "", r["date"] or ""] 
        for r in results
    ]
    print("Logs: ")
    print(tabulate(table, headers=headers, tablefmt="github"))


if __name__ == "__main__":
    main()
