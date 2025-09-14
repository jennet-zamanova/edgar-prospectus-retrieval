from abc import ABC, abstractmethod
from typing import Optional, TypedDict

class ProspectusLog(TypedDict):
    fund_symbol: str
    is_successfully_saved: bool
    error: Optional[str]  # can be None if no error
    url: Optional[str] # can be None if error
    date: Optional[str] # can be None if error

class ProspectusRetriever(ABC):
    @abstractmethod
    def set_api_key(self, api_key):
        """
        Set the api key for the service.
        """
        pass

    @abstractmethod
    def retrieve_prospectus_as_pdf(self, fund_symbol: str, file_name: str) -> ProspectusLog:
        """
        Retrieve latest prospectus (filed as 497K) for fund `fund_symbol` and
        save as pdf file at `file_name`.

        Returns None if completed successfully. Otherwise, returns the error raised.
        """
        pass

    @abstractmethod
    def retrieve_prospectuses_as_pdfs(self, fund_symbols: list[str], file_names: list[str] = None) -> list[ProspectusLog]:
        """
        Retrieve latest prospectuses (filed as 497K) for funds `fund_symbols` and
        save as pdf files at `file_names` where `fund_symbols[i]` latest prospectus 
        is saved at `file_names[i]` file for 0 <= i < len(file_names). 

        Raises error if len(fund_symbols) != len(file_names).
        Returns a summary log of which funds were successfully retrieved and saved.
        """
        pass

    @abstractmethod
    def retrieve_prospectuses(self, fund_symbols: list[str], file_names: list[str] = None) -> list[ProspectusLog]:
        """
        Retrieve latest prospectuses (filed as 497K) for funds `fund_symbols` and
        save as html files at `file_names` where `fund_symbols[i]` latest prospectus 
        is saved at `file_names[i]` file for 0 <= i < len(file_names). 

        If `file_names` not provided, use `fund_symbols[i] + ".htm"` instead.

        Raises error if len(fund_symbols) != len(file_names).
        Returns a summary log of which funds were successfully retrieved and saved.
        """
        pass

    @abstractmethod
    def retrieve_prospectus(self, fund_symbol: str, file_name: str) -> ProspectusLog:
        """
        Retrieve latest prospectus filing details (filed as 497K) for fund `fund_symbol` and
        save as the available file at `file_name`.

        Returns None if completed successfully. Otherwise, returns the error raised.
        """
        pass

