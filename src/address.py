class Address:
    is_valid = False
    tag = ''
    index = ''
    offset = ''
    addr = ''
    overlap = ''
    overlapCheck = ''
    overlap_splice = ''
    overlap_end = ''
    index_bits = 0
    offset_bits = 0
    tag_bits = 0
    index_bits_end = 0
    print(overlap)

    def __init__(self, addr='', offset_bits='', index_bits='', tag_bits=''):
        # Return default values for empty address (ignore)
        if int(addr, base=16) == 0:
            return

        self.addr = addr
        self.tag_bits = tag_bits
        self.index_bits = index_bits
        self.offset_bits = offset_bits

        index_bits_start = tag_bits + 1
        index_bits_end = index_bits_start + index_bits - 1
        self.overlap_splice = tag_bits
        self.overlap_end = index_bits_start + index_bits - 1

        self.tag = addr[0:tag_bits]
        self.index = addr[tag_bits:index_bits_end]
        self.offset = addr[index_bits_end:]
        self.overlap = addr[tag_bits:]

        self.is_valid = True

    def print_address(self):
        print("addr", self.addr, "tag", self.tag, "index", self.index, "offset", self.offset)

    # TODO Should return two values  as a tuple whether or not it overlaps
    # and the new index value
    def index_overlaps(self, read_bytes):
        index_length = "0%db" % (self.index_bits + self.offset_bits)
        self.overlapCheck = format((int(self.overlap, 2) + read_bytes), index_length)
        new_index = self.overlapCheck[:self.index_bits]
        self.addr = self.tag + self.overlapCheck

        if new_index == self.index:
            print("Returned false properly")
            return False, ''
        else:

            print("returned true properly")
            return True, self

