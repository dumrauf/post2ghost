import argparse
import sys

from posts.PostToGhostFileHandler import PostToGhostFileHandler


def _parse_args(args):
    parser = argparse.ArgumentParser(
        description='Post2Ghost - Upload Markdown Articles as Draft Ghost Blog Posts')
    parser.add_argument('-f',
                        dest='filename',
                        required=True,
                        type=str,
                        help='The Markdown file')
    args = parser.parse_args()
    return args


def main():
    parser = _parse_args(sys.argv[1:])
    post_to_ghost_file_handler = PostToGhostFileHandler()
    post_to_ghost_file_handler.post_to_ghost(path=parser.filename)


if __name__ == "__main__":
    main()
