import math
import os.path as path
import sys
import re

from .arguments import Arguments
from .trace import Trace
from .address import Address
from .index import Index

address_space = 32
bytes_in_kb = 1024
valid_bits = 1
bits_per_byte = 8
default_address_length = 4

# Cache class gets initialized with the class
# Arguments and calculates the cache main implementation
class Cache:
    index_dict = {}
    total = 0
    hits = 0
    misses = 0
    compulsory_misses = 0
    conflict_misses = 0

    block_offset_bits = 0
    index_bits = 0
    tag_bits = 0

    def __init__(self, args: Arguments):
        self.args = args
        self.block_offset_bits = self.get_block_offset()
        self.index_bits = self.get_index_size()
        self.tag_bits = self.get_tag_size()

    def print_results(self):
        print("\n***** Cache Calculated Parameters *****\n")
        print("Cache Size: {} KB\nBlock Size: {} bytes\nAssociativity: {}\nPolicy: {}\n".format(
            self.args.cache_size, self.args.block_size, self.args.associativity, self.args.replacement_policy))
        print("Total # of Blocks: {} KB\nTag Size: {} bits\nIndex Size: {}, Total Indices: {} KB\nOverhead Size: {} bytes\nImplementation Memory Size: {}".format(
            self.get_total_blocks(), self.get_tag_size(), self.get_index_size(), self.get_total_indices(), self.get_overhead_size(), self.get_imp_mem_size()))
        print("\n***** Cache Simulation Results *****\n")
        print("Total Cache Accesses: {}\nCache Hits: {}\nCache Misses: {}\n--- Compulsory Misses: {}\n--- Conflict Misses: {}".format(self.total, self.hits, self.misses, self.compulsory_misses, self.conflict_misses))
        print("\n***** ***** CACHE MISS RATE ***** *****\n")
        print("Cache Hit Rate: {}%".format(self.get_miss_rate()))
        print("\n***** ***** CACHE HIT RATE ***** *****\n")
        print("Cache Hit Rate: {}%".format(self.get_hit_rate()))

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
        block_offset_size = math.pow(2, self.get_block_offset())
        cache_size_bytes = self.args.cache_size * bytes_in_kb
        return int(math.log2(cache_size_bytes / (self.args.associativity * block_offset_size)))

    # Get total indices
    def get_total_indices(self):
        return int(math.pow(2, self.get_index_size()) / bytes_in_kb)

    # Get implementation size needed
    def get_overhead_size(self):
        blocks_bytes = self.get_total_blocks() * bytes_in_kb
        return int(blocks_bytes * (self.get_tag_size() + valid_bits) / bits_per_byte)

    # Get overhead size
    def get_imp_mem_size(self):
        cache_size = (self.args.cache_size * bytes_in_kb)
        return int((cache_size + self.get_overhead_size()))

    def get_hit_rate(self):
        return self.hits / self.total * 100

    def get_miss_rate(self):
        return self.misses / self.total * 100

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

                # Convert string to hex number then format it with 32 binary numbers using 0 as padding
                address = format(int(regex1.group(2), base=16), '032b')
                src_m = format(int(regex2.group(1), base=16), '032b')
                dst_m = format(int(regex2.group(2), base=16), '032b')

                trace = Trace(length, address, src_m, dst_m)
                self.handle_trace(trace)

    def handle_trace(self, trace: Trace):
        addr = Address(trace.address, offset_bits=self.block_offset_bits, index_bits=self.index_bits, tag_bits=self.tag_bits)
        src_m = Address(trace.src_m, offset_bits=self.block_offset_bits, index_bits=self.index_bits, tag_bits=self.tag_bits)
        dst_m = Address(trace.dst_m, offset_bits=self.block_offset_bits, index_bits=self.index_bits, tag_bits=self.tag_bits)

        self.simulate_cache(addr, trace.length)

        # If src_m and dst_m are valid addressess (greater than 00000000)
        if src_m.is_valid:
            self.simulate_cache(src_m, default_address_length)
        if dst_m.is_valid:
            self.simulate_cache(dst_m, default_address_length)

    def simulate_cache(self, addr: Address, length_read_bytes):
        if addr.index in self.index_dict:
            # Handle index already in the dictionary
            index = self.index_dict[addr.index]
            self.handle_index_in_dict(index, addr, length_read_bytes)

        else:
            # Save new index in dictionary
            self.index_dict[addr.index] = Index(tag=addr.tag, associativity=self.args.associativity, rep_policy=self.args.replacement_policy)
            self.misses += 1
            self.compulsory_misses += 1

        self.total += 1

    def handle_index_in_dict(self, index: Index, addr: Address, length_read_bytes):
        # TODO figure out if tag exists for the index does the tag
        # get appended or it doesn't affect the array at all
        if index.has_tag(addr.tag) and index.get_tag(addr.tag).valid_bit_is_set():
            # is a hit
            self.hits += 1
        else:
            # is a miss
            self.compulsory_misses, self.conflict_misses = index.add_or_replace_tag(addr.tag, self.compulsory_misses, self.conflict_misses)
            self.misses += 1
        
        overlaps, new_addr = addr.index_overlaps(length_read_bytes - 1)
        
        if overlaps:
            self.simulate_cache(new_addr, 0)
