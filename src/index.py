from .tag import Tag

class Index:
    # Dictionary of tags <tag, Tag>
    tags = {}
    associativity = 1
    rep_policy = 'RR'
    replace_index = 0

    def __init__(self, tag='', associativity=1, rep_policy='RR'):
        self.tags[tag] = Tag(tag)
        self.associativity = associativity
        self.rep_policy = rep_policy

    def add_or_replace_tag(self, tag):
        # If we just need to add the tag
        if len(self.tags) < self.associativity:
            self.tags[tag] = Tag(tag)
        else:
            self.replace_tag(tag)

    def has_tag(self, tag):
        return tag in self.tags

    def get_tag(self, tag):
        return self.tags[tag]

    def replace_tag(self, tag):
        if self.rep_policy == 'RR':
            self.replace_tag_RR(tag)
        elif self.rep_policy == 'RND':
            self.replace_tag_RND(tag)
        else:
            self.replace_tag_LRU(tag)

    # TODO implement replacement methods on full index
    def replace_tag_RR(self, tag):
        pass

    def replace_tag_RND(self, tag):
        pass

    def replace_tag_LRU(self, tag):
        pass
