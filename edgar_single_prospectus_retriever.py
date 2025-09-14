import json
import requests

from prospectus_retriever import ProspectusLog, ProspectusRetriever

class EdgarSingleProspectusRetriever(ProspectusRetriever):
    def __init__(self, api_key):
        super().__init__()
        self._api_key = api_key
        self.symbol_to_cik = {}
        self._process_mappings()

    def _process_mappings(self) -> None:
        """ preprocess mappings to make look up easier """

        with open("company_tickers_mf.json", "r") as f:
            cik_mapping = json.loads(f.read())["data"]
            for [cik,seriesId,classId,symbol] in cik_mapping:
                self.symbol_to_cik[symbol] = cik

    def _get_cik(self, fund_symbol: str) -> str:
        """ Fail if symbol is not found """
        # TODO offer closest symbol
        if fund_symbol in self.symbol_to_cik:
            return self.symbol_to_cik[fund_symbol]
        raise LookupError("Fund Not Found")
    
    def set_api_key(self, api_key: str):
        self._api_key = api_key

    def _retrieve_prospectus_data(self, cik: str, start=0, size=1):
        """ retrieve filing data """

        api_url = "https://api.sec-api.io"  

        payload = {
            "query": f"formType:\"497K\" AND cik:{cik}",  
            "from": start,
            "size": size,
            "sort": [{ "filedAt": { "order": "desc" }}]
        }

        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        res = response.json()  
        return res


    def _log_metadata(self, fund_symbol:str, filing_url:str, date):
        """ Print/log metadata (fund symbol, document date, source link). """
        l = f"""
            __Fund__: {fund_symbol}  
            __Date__ (Represents the Accepted attribute of a filing in ISO 8601 format, and shows the date and time the filing was accepted by the EDGAR system): {date}  
            __Link__ (URL of the index page (also known as filing detail page) of the filing): {filing_url}  
        """
        print(l)
        return l
    

    def _download_prospectus(self, res):
        """ Download HTML file data for filing from filing details link. """
        original_filename = res["filings"][0]["linkToFilingDetails"]
        original_filename = original_filename[len("https://www.sec.gov/Archives/edgar/data/"):]
        download_api = f"https://archive.sec-api.io/{original_filename}"

        headers = {
            "Authorization": self._api_key,
            "Content-Type": "text/html"
        }

        response = requests.get(download_api, headers=headers)
        response.raise_for_status()
        return response.content


    def retrieve_prospectus(self, fund_symbol: str, file_name: str) -> ProspectusLog:
        try:
            cik = self._get_cik(fund_symbol)
            res = self._retrieve_prospectus_data(cik)
            url = res["filings"][0]["linkToHtml"]
            date = res["filings"][0]["filedAt"]
            # self._log_metadata(fund_symbol, url, date)
        except Exception as e:
            print(f"An error occurred during retrieval: {e}")
            return {
                "fund_symbol": fund_symbol,
                "is_successfully_saved": False,
                "error": e,
                "url": None,
                "date": None
            }
        
        try:
            data = self._download_prospectus(res)
            with open(file_name, "wb") as f:
                f.write(data)
            return {
                "fund_symbol": fund_symbol,
                "is_successfully_saved": True,
                "error": None,
                "url": url,
                "date": date
            }
        except Exception as e:
            print(f"An error occurred while downloading data: {e}")
            return {
                "fund_symbol": fund_symbol,
                "is_successfully_saved": False,
                "error": e,
                "url": url,
                "date": date
            }
        
    def _download_prospectus_as_pdf(self, link: str):
        """ Get PDF data for filing from link. """
        download_api = "https://api.sec-api.io/filing-reader"

        payload = {
            "url": link,   
            "token": self._api_key
        }

        headers = {
            "Content-Type": "application/pdf"
        }

        response = requests.get(download_api, params=payload, headers=headers)
        response.raise_for_status()
        return response.content


    def retrieve_prospectus_as_pdf(self, fund_symbol: str, file_name: str) -> ProspectusLog:
        if not file_name.endswith(".pdf"):
            file_name += ".pdf"

        try:
            cik = self._get_cik(fund_symbol)
            res = self._retrieve_prospectus_data(cik)
            url = res["filings"][0]["linkToHtml"]
            date = res["filings"][0]["filedAt"]
            # self._log_metadata(fund_symbol, res["filings"][0]["linkToHtml"], res["filings"][0]["filedAt"])
        except Exception as e:
            print(f"An error occurred during retrieval: {e}")
            return {
                "fund_symbol": fund_symbol,
                "is_successfully_saved": False,
                "error": e,
                "url": None,
                "date": None
            }

        try:
            data = self._download_prospectus_as_pdf(res["filings"][0]["linkToFilingDetails"])
            with open(file_name, "wb") as f:
                f.write(data)
            return {
                "fund_symbol": fund_symbol,
                "is_successfully_saved": True,
                "error": None,
                "url": url,
                "date": date
            }
        except Exception as e:
            print(f"An error occurred while downloading data: {e}")
            return {
                "fund_symbol": fund_symbol,
                "is_successfully_saved": False,
                "error": e,
                "url": url,
                "date": date
            }
