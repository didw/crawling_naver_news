import sys
import os
from tqdm import tqdm


def get_nlen(fname):
    num_line = sum(1 for line in open(fname, "r"))
    return num_line


def run_kss(in_path, out_path):
    nlen = get_nlen(in_path)
    pbar = tqdm(total=nlen)
    with open(out_path, 'w') as f_out:
        with open(in_path) as f_in:
            for line in f_in.readlines():
                for sent in kss.split_sentences(line):
                    f_out.write(f"{sent}\n")
                f_out.write("\n")
                pbar.update(1)
    pbar.close()


def main():
    in_file = '../news_2_kss/naver_news.txt'
    out_file = '../news_3_clean/naver_news.txt'
    run_kss(in_file, out_file)


if __name__ == '__main__':
    main()
