# readme

### classification.py
wikipediaの一部の文章をtsneで可視化

### get_title_depth_from_category
wikipediaの記事の専門性は、カテゴリの深さで評価できる

https://arxiv.org/abs/2004.09958

wikipediaのカテゴリは階層構造を持つ。  
また、ベースのカテゴリが存在する  
`Category:学科別分類`、`Category:主題別分類` など

カテゴリの下位カテゴリを取り出し、そのカテゴリに属するページのタイトルとその記事が属するカテゴリの深度を計測する.

https://ja.wikipedia.org/wiki/Category:%E5%AD%A6%E7%A7%91%E5%88%A5%E5%88%86%E9%A1%9E