class Address:
    is_valid = False
    tag = ''
    index = ''
    offset = ''
    addr = ''

    tag_bits = 0
    index_bits = 0

    def __init__(self, addr='', index_bits=0, tag_bits=0):
        # Return default values for empty address (ignore)
        if int(addr, base=16) == 0:
            return

        self.addr = addr
        self.index_bits = index_bits
        self.tag_bits = tag_bits

        index_bits_start = tag_bits + 1
        index_bits_end = index_bits_start + index_bits - 1

        self.tag = addr[0:tag_bits]
        self.index = addr[tag_bits:index_bits_end]
        self.offset = addr[index_bits_end:]

        self.is_valid = True

    def print_address(self):
        print("addr", self.addr, "tag", self.tag, "index", self.index, "offset", self.offset)

    def index_overlaps(self, read_bytes):
        new_addr_number = int(self.tag + self.index + self.offset, 2) + read_bytes
        new_addr_bin = format(new_addr_number, '032b')

        new_addr = Address(new_addr_bin, index_bits=self.index_bits, tag_bits=self.tag_bits)

        if self.index != new_addr.index:
            return (True, new_addr)
        
        return (False, '')
