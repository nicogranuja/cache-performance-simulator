from .tag import Tag
#from .cache import Cache
#from .arguments import Arguments

import random

class Index:
    tags = []
    associativity = 1
    rep_policy = 'RR'
    replace_index = 0

    def __init__(self, tag='', associativity=1, rep_policy='RR'):
        self.tags = []
        self.tags.append(Tag(tag))
        self.associativity = associativity
        self.rep_policy = rep_policy

    def add_or_replace_tag(self, tag, compulsory_misses, conflict_misses, total_bytes, cache_size):
        # If we just need to add the tag
        if len(self.tags) < self.associativity:
            self.tags.append(Tag(tag))
            compulsory_misses += 1
        else:
            self.replace_tag(tag)
            if total_bytes > cache_size:
                conflict_misses += 1
        return (compulsory_misses, conflict_misses)

    def has_tag(self, tag):
        for t in self.tags:
            if t.tag == tag:
                return True
        return False

    def get_tag(self, tag):
        for t in self.tags:
            if t.tag == tag:
                return t
        return None

    def replace_tag(self, tag):
        if self.rep_policy == 'RR':
            self.replace_tag_RR(tag)
        elif self.rep_policy == 'RND':
            self.replace_tag_RND(tag)
        else:
            self.replace_tag_LRU(tag)

    def replace_tag_RR(self, tag):
        self.tags[self.replace_index % self.associativity] = Tag(tag)
        self.replace_index += 1

    def replace_tag_RND(self, tag):
        self.tags[random.randrange(0, self.associativity)] = Tag(tag)

    def replace_tag_LRU(self, tag):
        pass
