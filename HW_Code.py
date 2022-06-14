


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
        return self._score < other._score

    def __gt__(self, other):
        return self._score > other._score

    def __eq__(self, other):
        return self._score == other._score

class WebStore:

    def __init__(self, ds):
        self._store = ds()
        self._search_result = MinHeap()


    #focus on why i have keywords in locations that they do not exist
    #somehow i'm

    #somewhere i am replacing an actual intersection with the root

    #look at the constructor for the keryword entry, for some reason it may
    # be an error


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
        common_urls = list(common_urls)

        #Now we need a metric that will rank the sites. Iterate through your
        # list of sites and calculate:
        for url in common_urls:
            term_one_location_list = term_one_keyword_entry._sites[url]
            term_two_location_list = term_two_keyword_entry._sites[url]

            term_one_location_list.sort()
            term_two_location_list.sort()

            #do i need to be adding anything to the list? ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            term_one_location_list = [x+1 for x in term_one_location_list]
            term_two_location_list = [x+1 for x in term_two_location_list]

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
            # adjusted_location_term_one = plain_location_term_one + 1
            # adjusted_location_term_two = plain_location_term_two + 1

            # PROXIMITY TO TOP~~~~~~~~~~~`
            # (location of first work) * (location of second word),m
            proximity_to_top = plain_location_term_one * plain_location_term_two

            # FREQUENCY ~~~~~~~~~~~~~~~
            # (1/frequency of first keyword) * (1/frequency of second word)
            # frequency is the number of times the word appears on the page. THis
            # should be easy to determine by examining the KeywordEntry object.
            # Notice we use the recriprocal. Higher frequency is better, but we are
            # using a MinHeap, so we want small numbers to be better.
            frequency_keyword_one = len(term_one_location_list)
            frequency_keyword_two = len(term_two_location_list)

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

            a = 0
            b = 0

            # Initialize result as max value
            result = sys.maxsize

            # Scan Both Arrays upto
            # sizeof of the Arrays
            while (a < term_one_location_list_length and b < term_two_location_list_length):

                if (abs(term_one_location_list[a] - term_two_location_list[b]) < result):
                    result = abs(term_one_location_list[a] - term_two_location_list[b])

                # Move Smaller Value
                if (term_one_location_list[a] < term_two_location_list[b]):
                    a += 1

                else:
                    b += 1

            if result == 0:
                result = 1
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # do i need to adjust the value of each of the
            # location values here? This is where we'd need to adjust all of
            # them!
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # while term_one_pointer < term_one_location_list_length and term_two_pointer < term_two_location_list_length:
            #     temp = abs(term_one_location_list[term_one_pointer] -
            #                term_two_location_list[term_two_pointer])
            #
            #     if temp < min_distance:
            #         min_distance = temp
            #
            #     if term_one_location_list[term_one_pointer] < \
            #             term_two_location_list[term_two_pointer]:
            #         term_one_pointer += 1
            #     else:
            #         term_two_pointer += 1
            #
            # # Neighboring words have a distance of 1, but if the two terms are the
            # # same distnace should also be 1. Ask yourself, why not zero?
            # if min_distance == 0:
            #     min_distance = 1

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


#sample output
# /Users/isaacmather/PycharmProjects/Assignment9/venv/bin/python /Users/isaacmather/PycharmProjects/Assignment9/main.py
# Enter first term: persistent
# Enter second term: defect
#
# Enter first term: placement
# Enter second term: defect
# http://compsci.mrreed.com 1.0145709240540254e+19
#
# Enter first term: spike
# Enter second term: position
# http://compsci.mrreed.com/8167.html 2.7670116110564327e+19
#
# Enter first term: waters
# Enter second term: waters
# http://compsci.mrreed.com/4820.html 9.223372036854776e+20
# http://compsci.mrreed.com/2649.html 7.142579305340338e+22
#
# Enter first term: scissors
# Enter second term: scissors
# http://compsci.mrreed.com/2649.html 3.6893488147419103e+19
# http://compsci.mrreed.com/7918.html 9.223372036854776e+20
# http://compsci.mrreed.com/5738.html 3.6893488147419103e+21
# http://compsci.mrreed.com/8167.html 4.4641120658377115e+21
# http://compsci.mrreed.com/4542.html 6.353980996189255e+22
#
# Enter first term: floor
# Enter second term: scissors
# http://compsci.mrreed.com/2649.html 5.902958103587057e+20
# http://compsci.mrreed.com/4542.html 1.7607417218355767e+22
#
# Enter first term:
# Enter second term: blank
#
# Enter first term: 1
# Enter second term: three
#
# Enter first term: [
# Enter second term: ]
#
# Enter first term:
# Enter second term:
#
# Enter first term: placement
# Enter second term: placement
# http://compsci.mrreed.com 9.223372036854778e+16
# http://compsci.mrreed.com/49.html 9.223372036854778e+16
#
# Enter first term: knobs
# Enter second term: placemenbt
#
# Enter first term: knobs
# Enter second term: placement
# http://compsci.mrreed.com 2.4903104499507896e+19
#
# Enter first term: scissors
# Enter second term: floor
# http://compsci.mrreed.com/2649.html 5.902958103587057e+20
# http://compsci.mrreed.com/4542.html 1.7607417218355767e+22
#
# Enter first term: floor
# Enter second term: scissors
# http://compsci.mrreed.com/2649.html 5.902958103587057e+20
# http://compsci.mrreed.com/4542.html 1.7607417218355767e+22
#
# Enter first term: isaac
# Enter second term: mather
#
# Enter first term: