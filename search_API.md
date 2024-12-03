# pro spojeni s Googlem 
- potřebuji zažádat o klíč pro API 
- https://developers.google.com/custom-search/v1/introduction

## Google API 
- views.py -> definuji funkci pro vyhledávání 
  - do .env uložím přístupové údaje a v programu ve views.py již volám pouze nazev pod 
  kterým jsem reálné údaje uložil v .env
  - data z googlu chodí jako .json soubory
  - import requests a nainstaluji request

- search.html -> přidám pole pro zobrazování výsledků z google
  - 