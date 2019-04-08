from src.cache import Cache
from src.arguments import Arguments


def main():
    args = Arguments()
    args.print_header()

    cache = Cache(args)
    cache.read_and_parse_trace_file()

    cache.print_results()


if __name__ == "__main__":
    main()
