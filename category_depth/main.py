import requests

WIKIPEDIA_API_URL = "https://ja.wikipedia.org/w/api.php"

def get_subcategories(category, depth=0, max_depth=10):
    """
    指定したカテゴリのすべての下位カテゴリを取得
    """
    subcategories = []
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmtype": "subcat",
        "cmlimit": "max"
    }

    response = requests.get(WIKIPEDIA_API_URL, params=params).json()
    subcats = response.get("query", {}).get("categorymembers", [])
    
    for subcat in subcats:
        subcategories.append((subcat['title'], depth + 1))
        if depth < max_depth:
            subcategories.extend(get_subcategories(subcat['title'].replace("Category:", ""), depth + 1, max_depth))

    return subcategories

def get_category_pages(category, depth=0):
    """
    指定したカテゴリのページを取得
    """
    pages = []
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmtype": "page",
        "cmlimit": "max"
    }

    response = requests.get(WIKIPEDIA_API_URL, params=params).json()
    pages_data = response.get("query", {}).get("categorymembers", [])
    
    for page in pages_data:
        if "Template:" in page['title']:
            continue
        pages.append((page['title'], depth))

    return pages

def get_all_pages_in_subcategories(category, max_depth=10):
    """
    指定したカテゴリの下位カテゴリにあるすべてのページとそのカテゴリの深さを取得
    """
    # カテゴリにあるページとその深さ
    all_pages = get_category_pages(category, depth=0)
    
    # 下位カテゴリを取得
    subcategories = get_subcategories(category, depth=0, max_depth=max_depth)
    
    # 各下位カテゴリごとのページを取得
    for subcat, subcat_depth in subcategories:
        pages_in_subcat = get_category_pages(subcat.replace("Category:", ""), depth=subcat_depth)
        all_pages.extend(pages_in_subcat)
    
    return all_pages


category="機械学習"
# category="学科別分類"
pages_with_depth = get_all_pages_in_subcategories(category, max_depth=1)

for title, depth in pages_with_depth:
    print(f"Title: {title}, Depth: {depth}")