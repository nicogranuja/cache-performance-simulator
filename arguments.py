import argparse
import sys

# Parse and validate cmd arguments
parser = argparse.ArgumentParser(
    prog="Cache Simulator", description="This program will create a cache simulator based on the arguments passed")
parser.add_argument("-f", dest="file", required=True,
                    help="Trace file name")
parser.add_argument("-s", dest="cache_size", type=int,
                    required=True, metavar="[1-8192]", help="Cache size in KB (1KB to 8MB)")
parser.add_argument("-b", dest="block_size", type=int,
                    choices=range(4, 65), metavar="[4-64]", required=True, help="Block size in bytes (4 bytes to 64 bytes)")
parser.add_argument("-a", dest="associativity", type=int,
                    required=True, help="Associativity (1, 2, 3, 4, 8, 16)", choices=[1, 2, 3, 4, 8, 16])
parser.add_argument("-r", dest="replacement_policy", required=True,
                    help="Replacement Policy (RR or RND or LRU)", choices=["RR", "RND", "LRU"])
args_parser = parser.parse_args()


# Singleton class to only hold the arguments
class Arguments:
    file = args_parser.file
    cache_size = args_parser.cache_size
    block_size = args_parser.block_size
    associativity = args_parser.associativity
    replacement_policy = args_parser.replacement_policy

    def print_header(self):
        all_args = " ".join(sys.argv)

        print("Cache Simulator CS 3853 Spring 2019 – Group #1\n")
        print("Cmd Line: {}\nTrace File: {}\nCache Size: {} KB\nBlock Size: {} bytes\nAssociativity: {}\nR-Policy: {}\n".format(
            all_args, self.file, self.cache_size, self.block_size, self.get_formatted_associativity(), self.replacement_policy))

    def get_formatted_associativity(self):
        associativity = str(self.associativity) + "-way"

        if self.associativity == 1:
            associativity = "direct"

        return associativity
