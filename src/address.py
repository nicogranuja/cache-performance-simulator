class Address:
    is_valid = False
    tag = 0
    index = 0
    offset = 0
    addr = ''

    def __init__(self, addr='', offset_bits=0, index_bits=0, tag_bits=0):
        # Return default values for empty address (ignore)
        if int(addr, base=16) == 0:
            return

        self.addr = addr

        # TODO Split the binary addr values for tag index and offset
        # self.tag =
        # self.index =
        # self.offset =

        self.is_valid = True

    # TODO Should return two values  as a tuple whether or not it overlaps
    # and the new index value
    def index_overlaps(self, read_bytes):
        return (False, '')
