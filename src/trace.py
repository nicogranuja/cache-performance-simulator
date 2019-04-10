class Trace:
    length = 0
    address = 0
    dst_m = 0
    src_m = 0

    def __init__(self, length, address, dst_m, src_m):
        self.length = length
        self.address = address
        self.dst_m = dst_m
        self.src_m = src_m

    def print_trace(self):
        print("length: {}, address: {}, dst_m: {}, src_m: {}".format(self.length, self.address, self.dst_m, self.src_m))

    def print_trace_milestone_1(self):
        print("{}: ({})".format(self.address, self.length))
