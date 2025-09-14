from edgar_single_prospectus_retriever import EdgarSingleProspectusRetriever
from prospectus_retriever import ProspectusLog

class EdgarProspectusRetriever(EdgarSingleProspectusRetriever):
    def __init__(self, api_key):
        super().__init__(api_key)

    def retrieve_prospectuses_as_pdfs(self, fund_symbols: list[str], file_names: list[str] = None) -> list[ProspectusLog]:
        logs = []
        if not file_names:
            file_names = [symbol+".pdf" for symbol in fund_symbols]
        else:
            if len(fund_symbols) != len(file_names):
                raise Exception("`fund_symbols` and `file_names` must be same length")
        for idx in range(len(fund_symbols)):
            logs.append(self.retrieve_prospectus_as_pdf(fund_symbols[idx], file_names[idx]))
        return logs
    
    def retrieve_prospectuses(self, fund_symbols: list[str], file_names: list[str] = None) -> list[ProspectusLog]:
        logs = []
        if not file_names:
            file_names = [symbol+".htm" for symbol in fund_symbols]
        else:
            if len(fund_symbols) != len(file_names):
                raise Exception("`fund_symbols` and `file_names` must be same length")
        for idx in range(len(fund_symbols)):
            logs.append(self.retrieve_prospectus(fund_symbols[idx], file_names[idx]))
        return logs
