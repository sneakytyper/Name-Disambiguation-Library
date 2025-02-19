import requests
import pandas as pd
from fuzzywuzzy import process

class FinancialAPI:
    #Base class for financial data API integration
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = None
        self.headers = {'User-Agent': 'CompanyDisambiguator/1.0'}
        
    def search_symbol(self, query):
        """Search for symbol information (to be implemented by subclasses)"""
        raise NotImplementedError
        
    def get_ticker_details(self, symbol, exchange):
        """Get ticker details (to be implemented by subclasses)"""
        raise NotImplementedError


class AlphaVantageAPI(FinancialAPI):
    #Alpha Vantage API implementation
    
    def __init__(self, api_key):
        super().__init__(api_key)
        self.base_url = "https://www.alphavantage.co/query"
        
    def search_symbol(self, query):
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': query,
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params, headers=self.headers)
        return response.json().get('bestMatches', [])
    
    def get_ticker_details(self, symbol, exchange):
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params, headers=self.headers)
        data = response.json()
        return {
            'company_name': data.get('Name'),
            'ticker': symbol,
            'exchange': data.get('Exchange'),
            'country': data.get('Country')
        } if response.status_code == 200 else None


class CompanyDisambiguator:
    #A library to disambiguate company names using financial APIs
    
    def __init__(self, api_key, primary_api='alphavantage'):
        """
        Initialize with API client
        """
        self.api = self._init_api(primary_api, api_key)
        self.fallback_apis = [
            AlphaVantageAPI(api_key)  # Add other API implementations here
        ]
        
    def _init_api(self, provider, api_key):
        """Initialize the primary API client"""
        if provider == 'alphavantage':
            return AlphaVantageAPI(api_key)
        raise ValueError(f"Unsupported API provider: {provider}")
        
    def _try_apis(self, func, *args):
        """Try request across multiple APIs"""
        try:
            result = getattr(self.api, func)(*args)
            if result:
                return result
        except Exception as e:
            pass
            
        for api in self.fallback_apis:
            try:
                result = getattr(api, func)(*args)
                if result:
                    return result
            except Exception as e:
                continue
        return None

    def parse_structured(self, text):
        #Parse structured inputs like "NASDAQ:AAPL"
        #Returns: (company_name, ticker, exchange) or None

        if ':' in text:
            exchange, ticker = text.upper().split(':', 1)
            details = self._try_apis('get_ticker_details', ticker, exchange)
            if details and details['exchange'] == exchange:
                return {
                    'company_name': details['company_name'],
                    'ticker': ticker,
                    'exchange': exchange
                }
        return None

    def parse_unstructured(self, text, threshold=80):
        #Parse unstructured inputs using API search with fuzzy matching
        #Returns best match above similarity threshold
        
        text = text.strip().upper()
        results = self._try_apis('search_symbol', text)
        
        if not results:
            return None
            
        # Process matches with fuzzy scoring
        matches = [(f"{res.get('2. name', '')} ({res.get('1. symbol', '')})", 
                   res) for res in results]
        best_match, score = process.extractOne(text, [m[0] for m in matches])
        
        if score >= threshold:
            selected = matches[[m[0] for m in matches].index(best_match)][1]
            return {
                'company_name': selected.get('2. name'),
                'ticker': selected.get('1. symbol').split(':')[-1],
                'exchange': selected.get('4. region')
            }
        return None

    def disambiguate(self, text):
        #Main disambiguation function handling both input types
        
        structured_result = self.parse_structured(text)
        if structured_result:
            return structured_result
            
        unstructured_result = self.parse_unstructured(text)
        if unstructured_result:
            return unstructured_result
            
        return {'error': 'No matching company found'}

# Usage example:(just for verification)
if __name__ == "__main__":
    disambiguator = CompanyDisambiguator(api_key='YOUR_API_KEY')
    
    print(disambiguator.disambiguate("NASDAQ:AAPL"))  # Structured input
    print(disambiguator.disambiguate("Tesla"))        # Unstructured input
    print(disambiguator.disambiguate("NYSE:MSFT"))   # Structured input
    print(disambiguator.disambiguate("RandomText"))   # Invalid input
