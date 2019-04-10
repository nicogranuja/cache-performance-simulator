class Address:
    is_valid = False
    tag = ''
    index = ''
    offset = ''
    addr = ''

    def __init__(self, addr='', offset_bits='', index_bits='', tag_bits=''):
        # Return default values for empty address (ignore)
        if int(addr, base=16) == 0:
            return

        self.addr = addr

        index_bits_start = tag_bits + 1
        index_bits_end = index_bits_start + index_bits - 1

        self.tag = addr[0:tag_bits]
        self.index = addr[tag_bits:index_bits_end]
        self.offset = addr[index_bits_end:]

        self.is_valid = True

    def print_address(self):
        print("addr", self.addr, "tag", self.tag, "index", self.index, "offset", self.offset)

    # TODO Should return two values  as a tuple whether or not it overlaps
    # and the new index value
    def index_overlaps(self, read_bytes):
        return (False, '')
