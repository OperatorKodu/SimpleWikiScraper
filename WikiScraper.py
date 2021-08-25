import json
import requests
from requests.api import head

class Scraper:

    def __init__(self) -> None:
        self.PARAMS = ''
        self.HEADERS = ''

    def setURL(self, url):
        self.URL = url

    def setParameters(self, parameters):
        self.PARAMS = parameters

    def setHeaders(self, headers):
        self.HEADERS = headers

    def get(self):
        self.session = requests.Session()
        
        if hasattr(self, 'URL'):
            try:
                self.response = self.session.get(self.URL, params=self.PARAMS, headers=self.HEADERS)
                if self.response.status_code != 200:
                    return self.response.status_code
                else:
                    return self.response.json()
            except:
                print("Parameters or/and headers necessary but not provided")

class WikiScraper:
    def __init__(self):
        self.finish = False
        self.scraper = Scraper()
        self.url = "https://pl.wikipedia.org/w/api.php"
        self.ACTION = "opensearch"
        self.search_phrase = ""
        self.namespace = "0"
        self.limit = "5"
        self.format = "json"

    def generateParameters(self):
        self.params = {
            "action": self.ACTION,
            "namespace": self.namespace,
            "search": self.search_phrase,
            "limit": self.limit,
            "format": self.format
        }

    def setSearchPhrase(self):
        self.search_phrase = input("Enter phrase: ")

    def search(self):
        self.generateParameters()
        self.scraper.setURL(self.url)
        self.scraper.setParameters(self.params)
        self.received_data = self.scraper.get()

    def chooseProperResult(self):
        choose = input("Select the id of the desired result: ")
        self.link = self.links[int(choose) - 1]

    def displayResults(self):
        results = self.received_data[1]
        self.links = self.received_data[3]
        if len(results) > 1:
            print("More than one result was found.")
            id = 1
            for result in results:
                print(str(id) + '.', result)
                id += 1
            self.chooseProperResult()

        else:
            self.link = self.links[0]

    def getPageContent(self):
        print("Content of page:", self.link)

    def start(self):
        while not self.finish:
            self.setSearchPhrase()
            self.search()
            self.displayResults()
            self.getPageContent()
            self.finish = True


wikiScraper = WikiScraper()
wikiScraper.start()

#response = session.get(url=URL, params=PARAMS)
#DATA = response.json()

#pretty_data = json.dumps(DATA, indent=4, sort_keys=True)

#print(pretty_data)