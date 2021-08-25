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

    def getResponse(self):
        self.session = requests.Session()
        self.response = self.session.get(self.URL, params=self.PARAMS, headers=self.HEADERS)

        if self.response.status_code != 200:
            return self.response.status_code
        else:
            return self.response.json()

    def get(self):
        if hasattr(self, 'URL'):
            try:
                return self.getResponse()
            except:
                print("Parameters or/and headers necessary but not provided")
        else:
            print("URL not provided")


class WikiScraper:

    def __init__(self):
        self.finish = False
        self.scraper = Scraper()
        self.url = "https://pl.wikipedia.org/w/api.php"
        self.action_for_searching = "opensearch"
        self.action_for_getting_page_content = "query"
        self.prop = "extracts"
        self.exsentences = "10"
        self.exlimit = "1"
        self.explaintext = "1"
        self.search_phrase = ""
        self.namespace = "0"
        self.limit = "5"
        self.json_format = "json"

    def generateSearchingParameters(self):
        self.searching_params = {
            "action": self.action_for_searching,
            "namespace": self.namespace,
            "search": self.search_phrase,
            "limit": self.limit,
            "format": self.json_format
        }

    def setParams(self, params):
        self.params = params

    def setSearchPhrase(self):
        self.search_phrase = input("Enter phrase: ")

    def getData(self):
        self.scraper.setURL(self.url)
        self.scraper.setParameters(self.params)
        self.received_data = self.scraper.get()

    def search(self):
        self.generateSearchingParameters()
        self.setParams(self.searching_params)
        self.getData()

    def setChosenResult(self, choose):
        self.chosen_link = self.links[int(choose) - 1]

    def chooseProperResult(self):
        choose = input("Select the id of the desired result: ")
        self.setChosenResult(choose)

    def extractResultsAndLinks(self):
        self.results = self.received_data[1]
        self.links = self.received_data[3]

    def isMoreThanOneResult(self):
        if len(self.results) > 1:
            return True
        else:
            return False

    def displayPossibleResults(self):
        print("More than one result was found.")
        id = 1
        for result in self.results:
            print(str(id) + '.', result)
            id += 1
        self.chooseProperResult()

    def getResults(self):
        
        self.extractResultsAndLinks()

        if self.isMoreThanOneResult():
            self.displayPossibleResults()
        else:
            self.setChosenResult(1)

    def extractPageTitle(self):
        trash, self.page_title = self.chosen_link.rsplit('/', 1)

    def generatePageContentParameters(self):
        self.get_page_content_params = {
            "action": self.action_for_getting_page_content,
            "prop": self.prop,
            "exsentences": self.exsentences,
            "exlimit": self.exlimit,
            "titles": self.page_title,
            "explaintext": self.explaintext,
            "format": self.json_format
        }

    def getPageContent(self):
        self.extractPageTitle()
        self.generatePageContentParameters()
        self.setParams(self.get_page_content_params)
        self.getData()
        pages = self.received_data['query']['pages']
        for page, data in pages.items():
            print('\n==', data['title'], '==')
            print(data['extract'])

        

    def start(self):
        while not self.finish:
            self.setSearchPhrase()
            self.search()
            self.getResults()
            self.getPageContent()
            self.finish = True


wikiScraper = WikiScraper()
wikiScraper.start()