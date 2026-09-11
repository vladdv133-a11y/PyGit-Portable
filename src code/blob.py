from git_object import GitObject


# Blobs are a git object that holds raw data from the user (e.g. files like main.c)
class Blob(GitObject):
    def __init__(self, data):
        self.data = data

    def get_name(self):
        return b"blob"

    def serialize(self):
        return self.data

    def deserialize(self, data):
        self.data = data
