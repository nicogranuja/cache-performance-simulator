from arguments import Arguments
from cache import Cache


def main():
    args = Arguments()
    args.print_header()

    cache = Cache(args)
    cache.read_and_parse_trace_file()

    # Milestone 1
    cache.print_traces(20)

    cache.print_results()


if __name__ == "__main__":
    main()
