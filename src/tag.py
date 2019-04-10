class Tag:
    tag = ''
    valid_bit = 0

    def __init__(self, tag=''):
        self.tag = tag
        self.valid_bit = 0

    def set_valid_bit(self):
        self.valid_bit = 1

    def valid_bit_is_set(self):
        return self.valid_bit == 1