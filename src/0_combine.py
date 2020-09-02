import os
import argparse
import random
from tqdm import tqdm


def get_parser():
    parser = argparse.ArgumentParser()

    # parser.add_argument("-s", "--sampling", \
    #                     type=bool, default=False, help="sampling")
    parser.add_argument('--sampling', dest='sampling', action='store_true')
    parser.add_argument('--no-sampling', dest='sampling', action='store_false')
    parser.set_defaults(sampling=True)
    args = parser.parse_args()
    return args


def get_total_len(args):
    res = 0
    for _path, _dir, flists in os.walk('../news'):
        if args.sampling:
            res += 1
        else:
            res += len(flists)
    return res


def main():
    print("0. Combine all news data")
    args = get_parser()
    print(args)
    fpath_out = '../news_0_combine/naver_news.txt'
    nlen = get_total_len(args)
    pbar = tqdm(total=nlen)
    with open(fpath_out, 'w', encoding='utf-8') as f_out:
        for path, _dir, flists in os.walk('../news'):
            random.shuffle(flists)
            for fname in flists:
                fpath = os.path.join(path, fname)
                with open(fpath) as f_in:
                    title = True
                    try:
                        for line in f_in.readlines():
                            if title:
                                title = False
                                continue
                            if line.strip() == '':
                                continue
                            f_out.write(line.strip())
                            f_out.write('\n')
                    except UnicodeDecodeError as e:
                        print(e)
                        print(fpath)
                        continue
                pbar.update(1)
                if args.sampling:
                    break
    pbar.close()


if __name__ == '__main__':
    main()
