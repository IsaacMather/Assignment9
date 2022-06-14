from MinHeap import MinHeap
from HashQP import HashQP
from WebStore import link_fisher, text_harvester, KeywordEntry, tag_visible
import sys

class ResultEntry:
    def __init__(self, site, score):
        self._site = site
        self._score = score

    @property
    def site(self):
        return self._site

    @property
    def score(self):
        return self._score

    def __lt__(self, other):
        if type(other) == int:
            return self._score < other
        elif type(other) == ResultEntry:
            return self._score < other._score
        else:
            print("Incorrect item passed to comparison operator")
            raise TypeError

    def __gt__(self, other):
        if type(other) == int:
            return self._score > other
        elif type(other) == ResultEntry:
            return self._score > other._score
        else:
            print("Incorrect item passed to comparison operator")
            raise TypeError

    def __eq__(self, other):
        if type(other) == int:
            return self._score == other
        elif type(other) == ResultEntry:
            return self._score == other._score
        else:
            print("Incorrect item passed to comparison operator")
            raise TypeError


class WebStore:

    def __init__(self, ds):
        self._store = ds()
        self._search_result = MinHeap()

    def search_pair(self, term_one: str, term_two: str) -> bool:
        self._search_result = MinHeap()

        try:
            self._store.find(term_one)
            self._store.find(term_two)
        except self._store.NotFoundError:
            return False

        term_one_keyword_entry = self._store.find(term_one)
        term_two_keyword_entry = self._store.find(term_two)

        term_one_url_list = term_one_keyword_entry.sites
        term_two_url_list = term_two_keyword_entry.sites

        term_one_url_set = set(term_one_url_list)
        term_two_url_set = set(term_two_url_list)

        common_urls = term_one_url_set.intersection(term_two_url_set)
        common_urls = list(common_urls)

        for url in common_urls:
            term_one_location_list = term_one_keyword_entry._sites[url]
            term_two_location_list = term_two_keyword_entry._sites[url]

            term_one_location_list.sort()
            term_two_location_list.sort()

            term_one_location_list = [x+1 for x in term_one_location_list]
            term_two_location_list = [x+1 for x in term_two_location_list]

            plain_location_term_one = term_one_location_list[0]
            plain_location_term_two = term_two_location_list[0]

            proximity_to_top = plain_location_term_one * plain_location_term_two

            frequency_keyword_one = len(term_one_location_list)
            frequency_keyword_two = len(term_two_location_list)

            combined_frequency = (1/frequency_keyword_one) * (1/frequency_keyword_two)

            term_one_location_list_length = len(term_one_location_list)
            term_two_location_list_length = len(term_two_location_list)

            a = 0
            b = 0

            result = sys.maxsize

            while (a < term_one_location_list_length and b < term_two_location_list_length):

                if (abs(term_one_location_list[a] - term_two_location_list[b]) < result):
                    result = abs(term_one_location_list[a] - term_two_location_list[b])

                if (term_one_location_list[a] < term_two_location_list[b]):
                    a += 1

                else:
                    b += 1

            if result == 0:
                result = 1

            score = proximity_to_top * combined_frequency * result

            self._search_result.insert(ResultEntry(url, score))

        return True

    def get_result(self) -> ResultEntry:
        try:
            return self._search_result.remove()
        except self._search_result.EmptyHeapError:
            raise IndexError

    def crawl(self, url, depth=0, reg_ex=""):
        for link in link_fisher(url, depth, reg_ex):
            for i, word in enumerate(text_harvester(link)):
                # print(word)
                if len(word) < 4 or not word.isalpha():
                    continue
                try:
                    self._store.find(word).add(link, i)
                except self._store.NotFoundError:
                    self._store.insert(KeywordEntry(word, link, i))

    def search(self, keyword):
        return self._store.find(keyword).sites

    def search_list(self, kw_list):
        found = 0
        not_found = 0
        for kw in kw_list:
            try:
                self.search(kw)
                found += 1
            except self._store.NotFoundError:
                not_found += 1
        return found, not_found

    def crawl_and_list(self, url, depth=0, reg_ex=''):
        word_set = set()
        for link in link_fisher(url, depth, reg_ex):
            for word in text_harvester(link):
                if len(word) < 4 or not word.isalpha():
                    continue
                word_set.add(word)
        return list(word_set)


def test_code():


    result1 = ResultEntry('site', 9)
    result2 = ResultEntry('site', 8)

    print(result1 == 9)
    print(result1 == result2)

    print(result1 < result2)
    print(result1 < 10)
    print(result1 > result2)
    print(result1 > 1)


    store = WebStore(HashQP)
    store.crawl("http://compsci.mrreed.com", 2)

    while True:
        term_one = input("Enter first term: ")
        term_two = input("Enter second term: ")
        store.search_pair(term_one, term_two)
        while True:
            try:
                result = store.get_result()
                print(result.site, result.score)
            except IndexError:
                break
        print()

if __name__ == '__main__':
    test_code()

#sample run
# /Users/isaacmather/PycharmProjects/Assignment9/venv/bin/python /Users/isaacmather/PycharmProjects/Assignment9/main.py
# True
# False
# False
# True
# True
# True
# Enter first term: persistent
# Enter second term: defect
#
# Enter first term: placement
# Enter second term: defect
# http://compsci.mrreed.com 1.1
#
# Enter first term: spike
# Enter second term: position
# http://compsci.mrreed.com/8167.html 6.0
#
# Enter first term: waters
# Enter second term: waters
# http://compsci.mrreed.com/4820.html 100.0
# http://compsci.mrreed.com/2649.html 7744.0
#
# Enter first term: scissors
# Enter second term: scissors
# http://compsci.mrreed.com/2649.html 4.0
# http://compsci.mrreed.com/7918.html 100.0
# http://compsci.mrreed.com/5738.html 400.0
# http://compsci.mrreed.com/8167.html 484.0
# http://compsci.mrreed.com/4542.html 6889.0
#
# Enter first term: scissors
# Enter second term: floor
# http://compsci.mrreed.com/2649.html 1920.0
# http://compsci.mrreed.com/4542.html 114540.0
#
# Enter first term: floor
# Enter second term: scissors
# http://compsci.mrreed.com/2649.html 1920.0
# http://compsci.mrreed.com/4542.html 114540.0
#
# Enter first term: placement
# Enter second term: placement
# http://compsci.mrreed.com/49.html 0.010000000000000002
# http://compsci.mrreed.com 0.010000000000000002
#
# Enter first term: isaac
# Enter second term: mather
#
# Enter first term: placement
# Enter second term: mather
#
# Enter first term: '
# Enter second term:
#
# Enter first term:
# Enter second term:
#
# Enter first term: (
# Enter second term: )
#
# Enter first term: 9
# Enter second term: /
#
# Enter first term: //
# Enter second term: /
#
# Enter first term: