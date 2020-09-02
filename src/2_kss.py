import sys
import os
from tqdm import tqdm
import kss


def get_nlen(fname):
    num_line = sum(1 for line in open(fname, "r"))
    return num_line


def is_bad_paragraph(sentences):
    res = 0
    for sent in sentences:
        if len(sent) > 30:
            res += 1
    if res < 5:
        return True
    return False


end_filter_list = [
    "네이버메인에서조선구독하기",
    "문화닷컴바로가기",
    "무단전재및재배포금지",
    "무단복제및재배포금지",
    "서울경제채널구독",
    "무단전재재배포금지",
    "네이버채널뉴스구독",
    "오마이뉴스채널을구독",
    "디지털타임스채널구독",
    "네이버연합뉴스채널구독",
    "서울경제모바일페이지를만나보세요",
    "서울경제구독해주세요"
    "연합뉴스웹을만나보세요",
    "한국경제뉴스를받아보세요",
    "공감언론뉴시스",
    "스포츠서울공식페이스북",
    "네이버연합뉴스에서구독",
    "조선비즈받아보기",
    "국민일보채널구독하기",
    "한국일보뉴스를받아보세요",
    "세상을보는눈세계일보",
    "제보를기다립니다",
    "매일경제를받아보세요",
    "아시아경제뉴스를받아보세요",
    "매경이에어팟프로쏩니다",
    "부산일보구독하기",
    "한국일보뉴스를받아보세요",
    "뉴스헉스클릭해뉴스들어간다",
    "네이버메인에서디지털데일리뉴스",
    "세상을보는눈세계일보",
    "당신의제보가뉴스가됩니다",
    "대한민국24시간뉴스채널",
    "연합뉴스웹을만나보세요",
    "퀴즈풀고아이패드받자!",
    "기사공유하고코인적립하세요",
    "국민일보를구독하세요",
    "한국일보를구독하세요",
    "서울경제구독해주세요",
    "네이버연합뉴스구독",
    "뉴스채널구독하기",
    "네이버에서서울신문구독",
    "무단전재변형무단배포금지",
    "아이뉴스24를구독해주세요",
    "서울경제썸구독하기",
]
def is_end_sentence(sentence):
    sentence = sentence.replace(' ', '')
    for filt in end_filter_list:
        if filt in sentence:
            return True
    return False


other_filter_list = [
    "/사진"
]
def is_other_sentence(sentence):
    sentence = sentence.replace(' ', '')
    for filt in other_filter_list:
        if filt in sentence:
            return True
    return False


remove_filter_list = [
    "/연합뉴스"
]
def remove_sentence(sentence):
    for filt in remove_filter_list:
        sentence = sentence.replace(filt, '')
    return sentence


def run_kss(in_path, out_dir):
    nlen = get_nlen(in_path)
    pbar = tqdm(total=nlen)
    out_idx = 0
    cnt_sent = 0
    with open(in_path) as f_in:
        out_path = os.path.join(out_dir, f"kss_{out_idx}.txt")
        f_out = open(out_path, 'w')
        for _ in range(nlen):
            line = f_in.readline()
            pbar.update(1)
            sentences = kss.split_sentences(line)
            if is_bad_paragraph(sentences):
                continue
            for sent in sentences:
                if is_other_sentence(sent):
                    continue
                if is_end_sentence(sent):
                    break
                sent = remove_sentence(sent)
                f_out.write(f"{sent}\n")
                cnt_sent += 1
            f_out.write("\n")
            if cnt_sent > 1000000:
                f_out.close()
                out_idx += 1
                out_path = os.path.join(out_dir, f"kss_{out_idx}.txt")
                f_out = open(out_path, 'w')
                cnt_sent = 0
    pbar.close()
    f_out.close()


def main():
    print("2. Split sentences")
    in_file = '../news_1_ktp/naver_news.txt'
    out_dir = '../news_2_kss'
    run_kss(in_file, out_dir)


if __name__ == '__main__':
    main()
