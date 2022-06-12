from MinHeap import MinHeap
from HashQP import HashQP
from WebStore import WebStore

def test_code():
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_code()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
