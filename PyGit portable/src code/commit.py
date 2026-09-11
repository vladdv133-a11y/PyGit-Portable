from git_object import GitObject
from committagparser import parse_committag, serialise_committag

class GitCommit(GitObject):
    fmt=b'commit'

    def deserialize(self, data):
        self.commit = parse_committag(data)

    def serialize(self):
        return serialise_committag(self.kvlm)

    def init(self):
        self.commit = dict()

    def __init__(self, data=None):
        if data != None:
            self.deserialize(data)
        else:
            self.init()