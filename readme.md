# readme

### category_depth
wikipediaの記事の専門性は、カテゴリの深さで評価できる

https://arxiv.org/abs/2004.09958

wikipediaのカテゴリは階層構造を持つ。  
また、ベースのカテゴリが存在する  
`Category:学科別分類`、`Category:主題別分類` など

カテゴリの下位カテゴリを取り出し、そのカテゴリに属するページのタイトルとその記事が属するカテゴリの深度を計測する.

例: https://ja.wikipedia.org/wiki/Category:%E5%AD%A6%E7%A7%91%E5%88%A5%E5%88%86%E9%A1%9E

### count_words
wikipediaの動詞と名詞の頻度をカウント

[colab](https://colab.research.google.com/drive/1nt_3g0Kwo50K2xe5IjuoP224p560pZAg)

https://huggingface.co/datasets/if001/word_frequency_from_wiki_ja  
https://huggingface.co/datasets/if001/word_frequency_from_aozora


### readability_score
日本語の読みやすさ指標として以下が提案されている  
`X={ 平均文長 *-0.056}+{ 漢語率 *-0.126}+{ 和語率*-0.042}+{動詞率*-0.145}+{助詞率*-0.044}+11.724`

https://jreadability.net/sys/ja

[colab](https://colab.research.google.com/drive/1nt_3g0Kwo50K2xe5IjuoP224p560pZAg)
例: https://huggingface.co/datasets/if001/aozorabunko_readability_score

### show
classification.py
wikipediaの一部の文章をtsneで可視化
