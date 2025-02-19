import unittest
from disambiguator import CompanyDisambiguator

class TestNameDisambiguation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.disambiguator = CompanyDisambiguator(api_key='YOUR_API_KEY')
    
    # Core Functionality Tests
    def test_structured_input_1(self):
        """Test NASDAQ:AAPL input (Example 1 from problem statement)"""
        result = self.disambiguator.disambiguate("NASDAQ:AAPL")
        self.assertEqual(result['company_name'], 'Apple Inc.')
        self.assertEqual(result['ticker'], 'AAPL')
        self.assertEqual(result['exchange'], 'NASDAQ')

    def test_unstructured_input_1(self):
        """Test 'Tesla' input (Example 2 from problem statement)"""
        result = self.disambiguator.disambiguate("Tesla")
        self.assertEqual(result['company_name'], 'Tesla Inc.')
        self.assertEqual(result['ticker'], 'TSLA')
        self.assertEqual(result['exchange'], 'NASDAQ')

    # Structured Input Variations
    def test_structured_case_insensitivity(self):
        """Test case insensitivity in structured input"""
        inputs = [
            "nasdaq:aapl",
            "NySe:MsFt",
            "lse:hsba"
        ]
        for text in inputs:
            result = self.disambiguator.disambiguate(text)
            self.assertNotIn('error', result)

    # Unstructured Input Scenarios
    def test_unstructured_variations(self):
        """Test common company name variations"""
        cases = [
            ("Microsoft", 'MSFT', 'NYSE'),
            ("Alphabet", 'GOOG', 'NASDAQ'),
            ("Amazon", 'AMZN', 'NASDAQ')
        ]
        for text, ticker, exchange in cases:
            result = self.disambiguator.disambiguate(text)
            self.assertEqual(result['ticker'], ticker)
            self.assertEqual(result['exchange'], exchange)

    # Edge Cases
    def test_empty_input(self):
        """Test empty string handling"""
        result = self.disambiguator.disambiguate("")
        self.assertIn('error', result)

    def test_special_characters(self):
        """Test inputs with special characters"""
        cases = [
            ("Apple!", 'AAPL'),
            ("IBM*", 'IBM'),
            ("3M-Company", 'MMM')
        ]
        for text, ticker in cases:
            result = self.disambiguator.disambiguate(text)
            self.assertEqual(result['ticker'], ticker)

    # Error Handling Tests
    def test_invalid_structured_input(self):
        """Test invalid exchange:ticker format"""
        cases = [
            "NASDAQAAPL",
            "NYSE:INVALIDTICKER",
            "InvalidExchange:MSFT"
        ]
        for text in cases:
            result = self.disambiguator.disambiguate(text)
            self.assertIn('error', result)

    def test_non_existent_company(self):
        """Test clearly invalid input"""
        result = self.disambiguator.disambiguate("RandomText123")
        self.assertIn('error', result)

    # International Companies (Optional Enhancement)
    def test_international_exchanges(self):
        """Test international exchange support"""
        cases = [
            ("LSE:HSBA", 'HSBC Holdings plc', 'HSBA', 'LSE'),
            ("NSE:RELIANCE", 'Reliance Industries Limited', 'RELIANCE', 'NSE')
        ]
        for text, name, ticker, exchange in cases:
            result = self.disambiguator.disambiguate(text)
            self.assertEqual(result['company_name'], name)
            self.assertEqual(result['ticker'], ticker)
            self.assertEqual(result['exchange'], exchange)

    # Fuzzy Matching Tests (Optional Enhancement)
    def test_typo_handling(self):
        """Test fuzzy matching implementation"""
        cases = [
            ("Telsa", 'TSLA'),
            ("Microsft", 'MSFT'),
            ("Aple", 'AAPL')
        ]
        for text, ticker in cases:
            result = self.disambiguator.disambiguate(text)
            self.assertEqual(result['ticker'], ticker)

    # Ambiguous Company Names
    def test_ambiguous_names(self):
        """Test disambiguation of similar names"""
        cases = [
            ("Apple", 'AAPL'),  # Technology company
            ("Apple Bank", 'APPL'),  # Different entity
            ("Oracle", 'ORCL'),  # Software company
            ("Oracle Energy", 'OCEN')  # Energy company
        ]
        for text, ticker in cases:
            result = self.disambiguator.disambiguate(text)
            self.assertEqual(result['ticker'], ticker)

    # API Failure Tests
    def test_invalid_api_key(self):
        """Test error handling for API failures"""
        invalid_disambiguator = CompanyDisambiguator(api_key='INVALID_KEY')
        result = invalid_disambiguator.disambiguate("AAPL")
        self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main(verbosity=2)
