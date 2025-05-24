from datasets import load_dataset, Dataset
import MeCab
import json

"""
X={ 平均文長 *-0.056}+{ 漢語率 *-0.126}+{ 和語率*-0.042}+{動詞率*-0.145}+{助詞率*-0.044}+11.724
"""

def count(text):
    w_count = 0
    k_count = 0
    word_count = 0
    v_count = 0  # 動詞
    p_count = 0  # 助詞
    t = MeCab.Tagger("-d /usr/local/lib/python3.10/dist-packages/unidic/dicdir")

    node = t.parseToNode(text)
    while node:
        info = node.feature.split(",")
        word_count += 1
        if len(info) > 6 and info[6] != "*":
            pos = info[0]
            if pos not in ["記号"]:
                # print("debug:", pos, info[8], info[12])
                if info[12] == "和":
                    w_count += 1
                if info[12] == "漢":
                    k_count += 1
                if pos == "動詞":
                    v_count += 1
                if pos == "助詞":
                    p_count += 1
        node = node.next
        if node is None:
            break
    return word_count, w_count, k_count, v_count, p_count


def cal(sentence_av, k_rate, w_rate, v_rate, p_rate):
    return (
        (sentence_av * -0.056)
        + (k_rate * -0.126)
        + (w_rate * -0.042)
        + (v_rate * -0.145)
        + (p_rate * -0.044)
        + 11.724
    )


ds = load_dataset("if001/aozorabunko-clean-sin")
print(ds)
ids = []
scores = []
titles = []
sentence_len = []
words = []
cnt = 0
for v in ds['train']:
    id = v["meta"]["作品ID"]
    title = v["meta"]["作品名"]
    text = v["text"]
    sentences = text[:2000].split("。")

    word_count_s = 0
    w_count_s = 0
    k_count_s = 0
    v_count_s = 0
    p_count_s = 0
    for t in sentences:
        word_count, w_count, k_count, v_count, p_count = count(t)
        word_count_s += word_count
        w_count_s += w_count
        k_count_s += k_count
        v_count_s += v_count
        p_count_s += p_count

    score = cal(
        word_count_s / len(sentences),
        k_count_s / word_count_s,
        w_count_s / word_count_s,
        v_count_s / word_count_s,
        p_count_s / word_count_s,
    )
    ids.append(id)
    scores.append(score)
    titles.append(title)
    sentence_len.append(len(sentences))
    words.append(word_count_s)
    cnt += 1
    if cnt % 500 == 0:
      print('done...', cnt)

    print(text[:2000])
    print({"id": ids, "score": scores, "title": titles, "sentence_len": sentence_len, "words": words})
    print(k_count_s, w_count_s, v_count_s, p_count_s)

    break
d = {"id": ids, "score": scores, "title": titles, "sentence_len": sentence_len, "words": words}
dataset = Dataset.from_dict(d)
print(dataset)
dataset.push_to_hub(f"if001/aozorabunko_readability_score")