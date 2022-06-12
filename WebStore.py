from MinHeap import MinHeap
from bs4 import BeautifulSoup
import requests
import re
from bs4.element import Comment
from urllib.parse import urljoin
from ResultEntry import ResultEntry
import sys

def _link_fisher(url: str, depth=0, reg_ex=""):
    link_list = []
    headers = {'User-Agent': ''}

    if depth == 0:
        link_list.append(url)
        return link_list

    try:
        page = requests.get(url, headers=headers)
    except:
        print("Cannot access page")
        return link_list

    if page.status_code >= 400:
        print("Page Error")

    data = page.text
    pattern = re.compile(reg_ex)

    soup = BeautifulSoup(data, features="html.parser")
    for link in soup.find_all('a'):
        link = link.get("href")
        if not pattern.match(link) or reg_ex == '':
            link = urljoin(url, link)
        link_list.append(link)
        link_list += _link_fisher(link, depth - 1, reg_ex)

    link_list.append(url)
    # print(link_list)
    return link_list


def link_fisher(url: str, depth=0, reg_ex=""):
        link_list = _link_fisher(url, depth, reg_ex)
        link_list = list(set(link_list))
        return link_list


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def words_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.find_all(string=True)
    visible_texts = filter(tag_visible, texts)
    text_string = " ".join(t for t in visible_texts)
    words = re.findall(r'\w+', text_string)
    return words


def text_harvester(url):
    headers = {
        'User-Agent': ''}
    try:
        page = requests.get(url, headers=headers)
    except:
        return []
    res = words_from_html(page.content)

    return res


class KeywordEntry:
    """Stores information about a specific word on a webpage

        Args:
            word (str): the word we're storing info about
            url (str): the url the word is located on
            location (int): location, where the word is on the page
    """

    def __init__(self, word: str, url: str = None, location: int = None):
        self._word = word.upper()
        if url:
            self._sites = {url: [location]}
        else:
            self._sites = {}

    def add(self, url: str, location: int) -> None:
        if url in self._sites:
            self._sites[url].append(location)
        else:
            self._sites[url] = [location]

    def get_locations(self, url: str) -> list:
        try:
            return self._sites[url]
        except IndexError:
            return []

    @property
    def sites(self) -> list:
        return [key for key in self._sites]

    def __lt__(self, other):
        if isinstance(other, str):
            other = other.upper()
            return self._word < other

        elif isinstance(other, KeywordEntry):
            return self._word < other._word

        else:
            print("Error, incorrect data type passed to __lt__")

    def __gt__(self, other):
        if isinstance(other, str):
            other = other.upper()
            return self._word > other

        elif isinstance(other, KeywordEntry):
            return self._word > other._word

        else:
            print("Error, incorrect data type passed to __gt__")

    def __eq__(self, other):
        if isinstance(other, str):
            other = other.upper()
            return self._word == other

        elif isinstance(other, KeywordEntry):
            return self._word == other._word

        else:
            print("Error, incorrect data type passed to __eq__")

    def __hash__(self):
        return hash(self._word)


class WebStore:

    def __init__(self, ds):
        self._store = ds()
        self._search_result = MinHeap()


    def search_pair(self, term_one: str, term_two: str) -> bool:
        self._search_result = MinHeap()
        #need to complete

        # this method accepts two search terms. We should attempt to find
        # all instances of each keyword. If the keywords are not both found,
        # the method immediately returns false.
        try:
            self._store.find(term_one)
            self._store.find(term_two)
        except self._store.NotFoundError:
            return False

        #   Otherwise we should have two KeywordEntry objects to work with in
        #   this method
        term_one_keyword_entry = self._store.find(term_one)
        term_two_keyword_entry = self._store.find(term_two)

        term_one_url_list = term_one_keyword_entry.sites
        term_two_url_list = term_two_keyword_entry.sites

        # We need to find all of the pages that contain both
        #   keywords. In otherwords, the interdsection of the pages in the two
        #   KeywordEntry objects (note that the intersection may be empty). It
        #   seems natural to use sets to accomplish this.
        term_one_url_set = set(term_one_url_list)
        term_two_url_set = set(term_two_url_list)

        common_urls = term_one_url_set.intersection(term_two_url_set)


        #Now we need a metric that will rank the sites. Iterate through your
        # list of sites and calculate:
        for url in common_urls:
            term_one_location_list = term_one_keyword_entry._sites[url]
            term_two_location_list = term_two_keyword_entry._sites[url]

            term_one_location_list.sort()
            term_two_location_list.sort()

            # location is the place where the term was first found on the page. If
            # it's the first word, location is 1, etc. Ask yourself, why not zero
            # for the first word? THis location should be easy to determine by
            # examining the KeywordEntry object. Smaller is better.
            plain_location_term_one = term_one_location_list[0]
            plain_location_term_two = term_two_location_list[0]

            # Note that we will need to adjust the stored location number seince
            # when we stored the words, we considered the first word on a page to be
            # location zero.

            #is this what i need to be doing here to adjust the locaiton of
            # the word?
            adjusted_location_term_one = plain_location_term_one + 1
            adjusted_location_term_two = plain_location_term_two + 1

            # PROXIMITY TO TOP~~~~~~~~~~~`
            # (location of first work) * (location of second word)
            proximity_to_top = adjusted_location_term_one * adjusted_location_term_two

            # FREQUENCY ~~~~~~~~~~~~~~~
            # (1/frequency of first keyword) * (1/frequency of second word)
            # frequency is the number of times the word appears on the page. THis
            # should be easy to determine by examining the KeywordEntry object.
            # Notice we use the recriprocal. Higher frequency is better, but we are
            # using a MinHeap, so we want small numbers to be better.
            frequency_keyword_one = len(term_one_keyword_entry)
            frequency_keyword_two = len(term_two_keyword_entry)

            combined_frequency = (1/frequency_keyword_one) * (1/frequency_keyword_two)



            #PROXIMITY TO EACH OTHER

            #  AIIGHT SO WE NEED TO FIND the smallest distnace between the
            #  two, first we should make sure the lists are sorted,
            # (minimum distance between the two terms)
            # Examine the positions of the two keywords on the page, and find the
            # smallest distance between the two words. This is more challenging.

            min_distance = sys.maxsize

            term_one_pointer = 0
            term_two_pointer = 0

            term_one_location_list_length = len(term_one_location_list)
            term_two_location_list_length = len(term_two_location_list)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # do i need to adjust the value of each of the
            # location values here? This is where we'd need to adjust all of
            # them!
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            while term_one_pointer < term_one_location_list_length and term_two_pointer < term_two_location_list_length:
                temp = abs(term_one_location_list[term_one_pointer] -
                           term_two_location_list[term_two_pointer])

                if temp < min_distance:
                    min_distance = temp

                if term_one_location_list[term_one_pointer] < \
                        term_two_location_list[term_two_pointer]:
                    term_one_pointer += 1
                else:
                    term_two_pointer += 1

            # Neighboring words have a distance of 1, but if the two terms are the
            # same distnace should also be 1. Ask yourself, why not zero?
            if min_distance == 0:
                min_distance = 1

            #The product of these threee metrics will be our final metric, and this
            # will be the metric that our MinHeap will use to establish priority.
            score = proximity_to_top * combined_frequency * min_distance

            # Create an anonymous ResultEntry object with the URL and associated
            # metric, and add the ResultEntry object to self._search_result()
            self._search_result.insert(ResultEntry(url, score))

        #Repeat that process until there are no more sites in the interseciton,
        # adn return True.
        return True




    def get_result(self) -> ResultEntry:
        try:
            return self._search_result.remove()
        except self._search_result.EmptyHeapError:
            raise IndexError
        #need to complete this as well

        #THis method is easy. Just pop and return the next result from the
        # priority queue. Catch a MinHeap.EmptyHeapError, and raise an
        # IndexError. Do not let the error pass through from the MinHeap,
        # that would tie our class to MinHeap and would not be good object
        # oriented design.


    def crawl(self, url:str, depth:0, reg_ex=""):

        for link in link_fisher(url, depth,reg_ex):
            list_of_words = text_harvester(link)
            for location, word in enumerate(list_of_words):
                if len(word) < 4 or not word.isalpha():
                    continue
                try:
                    self._store.find(word)
                    keyword_object = self._store.find(word)
                    keyword_object.add(url, location)
                except self._store.NotFoundError:
                    keyword_to_store = KeywordEntry(word,link,location)
                    self._store.insert(keyword_to_store)


    def search(self, keyword: str):
        keyword_object = self._store.find(keyword)
        url_list = keyword_object.sites
        return url_list


    def search_list(self,kw_list: list):
        found = 0
        not_found = 0

        for keyword in kw_list:
            try:
                found_item = self.search(keyword)
                found += 1
            except: #NotFoundError: we want a notfound error here, not bare
                # except
                not_found += 1
                continue

        return (found, not_found)


    def crawl_and_list(self, url, depth=0, reg_ex=''):
        word_set = set()
        for link in link_fisher(url, depth, reg_ex):
            for word in text_harvester(link):
                if len(word) < 4 or not word.isalpha():
                    continue
                word_set.add(word)
        return list(word_set)
