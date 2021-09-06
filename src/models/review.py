from json import JSONEncoder


class Review(object):

    def __init__(self, reviewed, reviewer, description):
        self.reviewed = reviewed
        self.reviewer = reviewer
        self.description = description


class ReviewEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
