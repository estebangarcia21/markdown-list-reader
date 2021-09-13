import argparse
from parse import parse_markdown, read_args


def main():
    parser = argparse.ArgumentParser(
        description='read a markdown string or file'
    )

    parser.add_argument('--string', '-s', type=str,
                        help='a valid markdown string')
    parser.add_argument('--file', '-f', type=argparse.FileType('r'),
                        help='the path to the markdown file')

    args = parser.parse_args()
    md_string = read_args(args)

    parse_markdown(md_string)


if __name__ == '__main__':
    main()
