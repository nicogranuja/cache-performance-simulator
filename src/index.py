from .tag import Tag

class Index:
    # Dictionary of tags <tag, Tag>
    tags = []
    associativity = 1
    rep_policy = 'RR'
    replace_index = 0

    def __init__(self, tag='', associativity=1, rep_policy='RR'):
        self.tags.append(Tag(tag))
        self.associativity = associativity
        self.rep_policy = rep_policy

    def add_or_replace_tag(self, tag):
        # If we just need to add the tag

        print ("curr tags")
        for t in self.tags:
            print (t.tag)
        print ()

        if len(self.tags) < self.associativity:
            self.tags.append(Tag(tag))
            print ("TAG ADDED")
        else:
            print ("REPLACED TAG")
            self.replace_tag(tag)

    def has_tag(self, tag):
        for t in self.tags:
            if t.tag == tag:
                return True
        return False

    def get_tag(self, tag):
        for t in self.tags:
            if t.tag == tag:
                return t
        return none

    def replace_tag(self, tag):
        if self.rep_policy == 'RR':
            self.replace_tag_RR(tag)
        elif self.rep_policy == 'RND':
            self.replace_tag_RND(tag)
        else:
            self.replace_tag_LRU(tag)

    # TODO implement replacement methods on full index
    def replace_tag_RR(self, tag):

        print("curr: {} ".format(self.replace_index % self.associativity))
        self.tags.pop(self.replace_index % self.associativity)
        self.tags.insert(self.replace_index % self.associativity, Tag(tag))
        self.replace_index += 1

        # print()
        # print ("new tags")
        # for t in self.tags:
        #     print (t.tag)
        # print()

    def replace_tag_RND(self, tag):
        pass

    def replace_tag_LRU(self, tag):
        pass

