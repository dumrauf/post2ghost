import argparse
import sys

from posts.ReceiptFile import Receipt


def _parse_args(args):
    parser = argparse.ArgumentParser(
        description='FetchReceipt - Get the Latest Receipt for a Post from the Ghost server')
    parser.add_argument('-f',
                        dest='filename',
                        required=True,
                        type=str,
                        help='The Markdown file')
    args = parser.parse_args()
    return args


def main():
    parser = _parse_args(sys.argv[1:])
    receipt = Receipt(path=parser.filename)
    receipt.fetch_receipt()


if __name__ == "__main__":
    main()
