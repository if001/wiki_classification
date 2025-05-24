"""
wikipediaの動詞と名詞の頻度をカウント
"""

from datasets import load_dataset, Dataset
import MeCab
import pandas as pd


def count_words(text, vocab_counter, vocab_type):
    t = MeCab.Tagger("-d /usr/local/lib/python3.10/dist-packages/unidic/dicdir")
    node = t.parseToNode(text)
    while node:
        info = node.feature.split(",")
        node = node.next
        word = None
        if len(info) > 6 and info[6] != "*":
            if info[0] == "動詞":
                word = info[10]
            if info[0] == "名詞":
                word = info[10]
        if word is not None:
            if word in vocab_counter:
                vocab_counter[word] = vocab_counter[word] + 1
            else:
                vocab_counter[word] = 1
                if info[0] == "動詞":
                    vocab_type[word] = "v"
                if info[0] == "名詞":
                    vocab_type[word] = "n"
        if node is None:
            break


vocab_counter = {}
vocab_type = {}
# ds = load_dataset("if001/aozorabunko-clean-sin")
# ds = load_dataset("izumi-lab/wikinews-ja-20230728")
ds = load_dataset("izumi-lab/wikipedia-ja-20230720", split="train")
ds = ds.shuffle(seed=42).select(range(4000))

print(ds)
count = 0
for v in ds:
    text = v["text"]
    sentences = text[:2000].split("。")
    count_words(text, vocab_counter, vocab_type)
    count += 1
    if count % 500 == 0:
      print('done', count)
    #if count > 400:
    #  break

t_dict = {
    "words": list(vocab_counter.keys()),
    "count": list(vocab_counter.values()),
    "type": list(vocab_type.values()),
}
df = pd.DataFrame.from_dict(t_dict, orient="index").T