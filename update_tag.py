import argparse
import sys

from tags.TagFileHandler import TagFileHandler


def _parse_args(args):
    parser = argparse.ArgumentParser(
        description='UpdateTag - Update Ghost Tags')
    parser.add_argument('-f',
                        dest='filename',
                        required=True,
                        type=str,
                        help='The JSON file describing the tag')
    args = parser.parse_args()
    return args


def main():
    parser = _parse_args(sys.argv[1:])
    tag_file_handler = TagFileHandler()
    tag_file_handler.create_or_update_tag(path=parser.filename)


if __name__ == "__main__":
    main()
