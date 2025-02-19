# Name-Disambiguation-Library

A Python library for identifying company names, ticker symbols, and stock exchanges from structured and unstructured text inputs.

## Features

- 🏛️ Structured input parsing (e.g., "NASDAQ:AAPL")
- 🔍 Unstructured company name resolution (e.g., "Tesla" → Tesla Inc.)
- 📈 Integrated with Alpha Vantage API for real-time data
- 🛠️ Fuzzy matching for typos and case variations
- 🚦 Robust error handling for invalid inputs

## Installation

1. Install required packages:
  _pip install requests pandas fuzzywuzzy python-Levenshtein_
2. Clone repository:
   _git clone https://github.com/yourusername/company-disambiguator.git

   cd company-disambiguator_
4. Get [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)

## Usage Examples

_from disambiguator import CompanyDisambiguator_

Initialize with your API key
_disambiguator = CompanyDisambiguator(api_key='YOUR_API_KEY')_

**Example 1: Structured input**
result = disambiguator.disambiguate("NASDAQ:AAPL")
print(result)

Output: {'company_name': 'Apple Inc.', 'ticker': 'AAPL', 'exchange': 'NASDAQ'}

**Example 2: Unstructured input**
result = disambiguator.disambiguate("Telsa") # Handles typos
print(result)

Output: {'company_name': 'Tesla Inc.', 'ticker': 'TSLA', 'exchange': 'NASDAQ'}

**Example 3: Invalid input**
result = disambiguator.disambiguate("RandomText")
print(result)

Output: {'error': 'No matching company found'}
