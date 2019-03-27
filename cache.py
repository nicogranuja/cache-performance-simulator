import math
import os.path as path
import sys
import re

from arguments import Arguments
from trace import Trace

address_space = 32
bytes_in_kb = 1024
valid_bits = 1
bits_per_byte = 8

# Cache class gets initialized with the class Arguments and calculates the cache main implementation
class Cache:
    traces = []

    def __init__(self, args: Arguments):
        self.args = args

    def print_results(self):
        print("------------------------------------------------------------------------------------")
        print("Cache Size: {} KB\nBlock Size: {} bytes\nAssociativity: {}\nPolicy: {}\n".format(
            self.args.cache_size, self.args.block_size, self.args.associativity, self.args.replacement_policy))
        print("Total # of Blocks: {} KB\nTag Size: {} bits\nIndex Size: {}, Total Indices: {} KB\nOverhead Size: {} bytes\nImplementation Memory Size: {} bytes\nCache Hit Rate: {}%".format(
            self.get_total_blocks(), self.get_tag_size(), self.get_index_size(), self.get_total_indices(),self.get_overhead_size(), self.get_imp_mem_size(), self.get_hit_rate()))

    # Get offset bits
    def get_block_offset(self):
        return int(math.log2(self.args.block_size))

    # Get blocks in KB
    def get_total_blocks(self):
        return int(self.args.cache_size / self.args.block_size)

    # Get tag bits
    def get_tag_size(self):
        return address_space - self.get_block_offset() - self.get_index_size()

    # Get index bits
    def get_index_size(self):
        return int(math.log2((self.args.cache_size * bytes_in_kb) / (self.args.associativity * math.pow(2, self.get_block_offset()))))

    # Get total indices
    def get_total_indices(self):
        return int(math.pow(2, self.get_index_size()) / bytes_in_kb)

    #Get implementation size needed
    def get_overhead_size(self):
        return int(self.get_total_blocks() * bytes_in_kb * (self.get_tag_size() + valid_bits) / bits_per_byte)

    #Get overhead size
    def get_imp_mem_size(self):
        return int(((self.args.cache_size * bytes_in_kb) + self.get_total_blocks() * bytes_in_kb * (self.get_tag_size() + valid_bits / bits_per_byte)))

    def get_hit_rate(self):
        return "TODO"

    # This method will fill up the array with traces objects based on the trace file
    def read_and_parse_trace_file(self):
        trace_file_path = path.normpath(self.args.file)

        if not path.exists(trace_file_path):
            print("File: {} does not exists".format(trace_file_path))
            sys.exit(1)

        line1Pattern = re.compile(r"EIP\s\((\d+)\):\s(\w+)")
        line2Pattern = re.compile(r"dstM:\s(\w+).*srcM:\s(\w+)")

        with open(trace_file_path, "r") as trace_file:
            while True:
                line1 = str(trace_file.readline())
                line2 = str(trace_file.readline())

                # Empty line
                trace_file.readline()

                if not line1 and not line2:
                    break

                regex1 = line1Pattern.match(line1)
                regex2 = line2Pattern.match(line2)

                # Save matched data to the traces class element
                length = int(regex1.group(1))
                address = hex(int(regex1.group(2), base=16))

                src_m = hex(int(regex2.group(1), base=16))
                dst_m = hex(int(regex2.group(2), base=16))

                self.traces.append(Trace(length, address, src_m, dst_m))

    def print_traces(self, print_number):
        for i in range(0, print_number):
            self.traces[i].print_trace_milestone_1()
