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
            addr, overlap_bytes = self.get_overlap_bytes(new_addr, read_bytes)
            return (True, addr, overlap_bytes)
        
        return (False, '', 0)

    def get_overlap_bytes(self, new_addr, read_bytes):
        overlap_after = 1
        tmp_addr_number = int(self.tag + self.index + self.offset, 2)

        while overlap_after < read_bytes:
            tmp_addr_number += overlap_after
            tmp_addr_bin = format(tmp_addr_number, '032b')
            tmp_addr = Address(tmp_addr_bin, index_bits=self.index_bits, tag_bits=self.tag_bits)

            if self.index != tmp_addr.index:
                return (tmp_addr, overlap_after)

            overlap_after += 1

        return (new_addr, 0)

