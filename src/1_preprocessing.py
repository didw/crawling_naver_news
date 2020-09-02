import sys
import os
import argparse
from ktp.clean import Clean_kor


def parse_args(in_file, out_file):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", \
                        default=in_file, type=str, help="Input file path")
    parser.add_argument("-o", "--output", \
                        default=out_file, type=str, help="Output file path")
    parser.add_argument("-e", "--encoding", \
                        type=str, default='utf8', help="Encoding of input file")
    return parser.parse_args()


def main():
    print("1. Clean news data")
    in_file = '../news_0_combine/naver_news.txt'
    out_file = '../news_1_ktp/naver_news.txt'
    args = parse_args(in_file, out_file)
    obj = Clean_kor(args)
    obj.apply()


if __name__ == '__main__':
    main()
