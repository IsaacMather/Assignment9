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
        