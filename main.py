from arguments import Arguments
from cache import Cache


def main():
    args = Arguments()
    args.print_header()

    cache = Cache(args)
    cache.read_and_parse_trace_file()

    cache.print_results()
    print("\n------------------------------------------------------------------------------------\n")
    
    # Milestone 1
    cache.print_traces(20)


if __name__ == "__main__":
    main()
