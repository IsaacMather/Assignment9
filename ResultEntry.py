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
        