import time
import math

c1 = c = 0
while True:
    time.sleep(0.1)
    a = 1
    a1 = 1011.5
    r = 0.015
    c += a * (1+r)
    c1 += a1 * (1+r)

    print('r: {:10.1f} {:10.1f}\r'.format(c, c1), end='')

exit()

names = ['Alphabet Inc.',
'Amazon',
'Microsoft Corp',
'Apple Inc',
'ASML Holding NV',
'Exxon Mobil Corp',
'NextEra Energy Inc',
'Melrose Industries PLC',
'Johnson & Johnson',
'American Tower Corp',
'Unilever PLC',
'HP Inc',
'BP PLC',
'Boston Scientific Corp',
'EV Cash Reserves Fund LLC',
'CMS Energy Corp',
'ORIX Corp',
'Taiwan Semiconductor Manufacturing Co Ltd',
'Ecolab Inc',
'Eli Lilly & Co',
'Lonza Group AG',
'TJX Cos Inc',
'Verisk Analytics Inc',
'Activision Blizzard Inc',
'Wells Fargo & Co',
'Canadian Imperial Bank of Commerce',
'Assa Abloy AB',
'ConocoPhillips',
'Zoetis Inc',
'Aviva PLC',
'Xylem Inc/NY',
'CDW Corp/DE',
'Home Depot Inc',
'BASF SE',
'Industria de Diseno Textil SA',
'ITT Inc',
'Citigroup Inc',
'CSX Corp',
'Walt Disney Co',
'Keyence Corp',
'Iberdrola SA',
'Diageo PLC',
'Visa Inc',
'Facebook Inc',
'Parker-Hannifin Corp',
'Compass Group PLC',
'British American Tobacco PLC',
'KeyCorp',
'Rio Tinto Ltd',
'Phillips 66',
'adidas AG',
'GlaxoSmithKline PLC',
'Anheuser-Busch InBev SA/NV',
'Prudential PLC',
'Danaher Corp',
'Bayer AG',
'Komatsu Ltd',
'Reckitt Benckiser Group PLC',
'Legrand SA',
'Chubb Ltd',
'Republic Services Inc',
'Fortive Corp',
'Anthem Inc',
'Baxter International Inc',
'LVMH Moet Hennessy Louis Vuitton SE',
'Secom Co Ltd',
'Sika AG',
'Novo Nordisk A/S',
'Discover Financial Services',
'CAE Inc',
'Navient Corp',
'AIA Group Ltd',
'Sumitomo Mitsui Financial Group Inc',
'Equity Residential',
'ING Groep NV',
'Nordea Bank AB',
'Atlas Copco AB',
'Tele2 AB',
'Continental AG',
'Banco Santander SA',
'MGIC Investment Corp',
'Halliburton Co',
'Ulta Beauty Inc',
'UnitedHealth Group Inc',
'MISUMI Group Inc',
'Societe Generale SA',
'OneMain Holdings Inc',
'UniCredit SpA',
'Samsonite International SA',
'Constellation Brands Inc',
'Danske Bank A/S',
'Seven Generations Energy Ltd',
'Pound Sterling',
]


# WSX5EA 09/07/18 C3500   -0.00%
# UKX 09/21/18 C7675      -0.00%
# UKX 09/21/18 C7625      -0.00%
# WNKYA 09/07/18 C22875   -0.01%
# SX5E 09/21/18 C3475     -0.01%
# WSX5EB 09/14/18 C3425   -0.01%
# WNKYC 09/21/18 C22750   -0.01%
# NKY 09/14/18 C22625     -0.02%
# WSX5ED 09/28/18 C3450   -0.02%

# SPXW US 09/26/18 C2910  -0.02%
# SPXW US 09/24/18 C2900  -0.02%
# SPXW US 09/28/18 C2900  -0.02%
# SPXW US 09/21/18 C2875  -0.04%
# SPXW US 09/05/18 C2855  -0.04%
# SPXW US 09/17/18 C2860  -0.04%
# SPXW US 09/07/18 C2850  -0.05%
# SPXW US 09/10/18 C2850  -0.05%
# SPXW US 09/19/18 C2855  -0.05%
# SPXW US 09/14/18 C2850  -0.05%
# SPXW US 09/12/18 C2845  -0.05%
# SPXW US 09/04/18 C2830  -0.06%
#                         -0.56%


import requests
import json
import time
import re

if __name__ == '__main__':
    ALPHAVANTAGE_API_KEY = '1UH8FHIQ1YCSALSS'
    base_url = 'https://www.alphavantage.co/query'
    # function = kwargs.get('function', 'TIME_SERIES_DAILY_ADJUSTED')
    # outputsize = kwargs.get('outputsize', 'compact')
    # datatype = kwargs.get('datatype', 'json')

    # query = '{}?function={}&symbol={}&outputsize={}&datatype={}&apikey={}'.format(

    def run_name(keywords):
        query = '{}?apikey={}&function={}&keywords={}&datatype={}'.format(
            base_url, ALPHAVANTAGE_API_KEY, 'SYMBOL_SEARCH', keywords, 'json')

        j = json.loads(requests.get(query, allow_redirects=True).text)
        return j['bestMatches']

    # _names = [re.sub(r'', '', name) for name in names]
    # _names = ['SXR8']
    for name in _names:
        matches = run_name(name)

        print('\n{}'.format(name))
        if len(matches) == 0:
            print('missing')
            continue

        for match in matches:
            p = '{:<15}\t{}\t{:<5}\t{:20}\t{}'.format(match['1. symbol'], match['9. matchScore'], match['8. currency'], match['4. region'], match['2. name'])
            print(p)

        time.sleep(5)
        pass


    def run_symbol(symbol):
        query = '{}?apikey={}&function={}&symbol={}&outputsize=full'.format(
            base_url, ALPHAVANTAGE_API_KEY, 'TIME_SERIES_DAILY_ADJUSTED', symbol)

        j = json.loads(requests.get(query, allow_redirects=True).text)
        return j


    exit()
    print()
    jj = run_symbol('YNDX.MOS')
    for (k, v) in jj['Time Series (Daily)'].items():
        print(k, v['4. close'], v['5. adjusted close'], v['7. dividend amount'])

