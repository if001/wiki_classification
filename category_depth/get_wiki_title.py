import requests

def get_wikipedia_links(title, n_hops=1):
    """
    指定したページからn_hopsまでのページのリンクを取得
    """
    base_url = "https://ja.wikipedia.org/w/api.php"
    
    # Keep track of visited pages and results
    visited = set()
    result = []

    # Initialize the queue with the first page and the current hop count
    queue = [(title, 0)]
    visited.add(title)

    while queue:
        current_title, hops = queue.pop(0)
        if hops > n_hops:
            break

        # Fetch links and categories from the current page
        params = {
            "action": "query",
            "format": "json",
            "prop": "links|categories",  # Add categories to the query
            "titles": current_title,
            "pllimit": 5,
            "cllimit": "max"
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        # Process the pages
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            # Get the title and category count
            page_title = page_data.get("title", "No title")
            categories = page_data.get("categories", [])
            category_count = len(categories)

            # Append the title and category count to the result
            result.append((page_title, category_count))

            # Process links for further exploration
            links = page_data.get("links", [])
            for link in links:
                link_title = link.get("title")
                if link_title not in visited:
                    visited.add(link_title)
                    queue.append((link_title, hops + 1))

    return result


def get_subcategory_titles(category, depth=1):
    """
    指定したカテゴリの下位カテゴリにあるページのタイトルを取得する
    """
    base_url = "https://ja.wikipedia.org/w/api.php"
    
    # Initialize sets to avoid duplicates
    visited_categories = set()
    result_titles = set()
    
    # Start with the main category
    queue = [(category, 0)]
    visited_categories.add(category)
    
    while queue:
        current_category, current_depth = queue.pop(0)
        if current_depth > depth:
            break
        
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": current_category,
            "cmlimit": "max",
            "cmtype": "subcat|page"
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        category_members = data.get("query", {}).get("categorymembers", [])
        # print('category', current_category)
        # print('category_members', category_members)
        # print()
        
        for member in category_members:
            if member["ns"] == 14:  # Namespace 14 is for categories
                subcategory_title = member["title"]
                if subcategory_title not in visited_categories:
                    visited_categories.add(subcategory_title)
                    queue.append((subcategory_title, current_depth + 1))
            elif member["ns"] == 0:  # Namespace 0 is for pages
                page_title = member["title"]
                result_titles.add(page_title)
    
    return list(result_titles)

def get_pages_and_depth_from_category(category, use_bfs_depth=True):
    """
    指定されたカテゴリの下位カテゴリにあるすべてのページタイトルとそのページのカテゴリの深さを返します
    """
    base_url = "https://ja.wikipedia.org/w/api.php"

    def get_subcategories_and_pages(current_category, current_depth):
        # Set up API request to get subcategories and pages
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": current_category,
            "cmlimit": "max",
            "cmtype": "subcat|page"
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        category_members = data.get("query", {}).get("categorymembers", [])
        subcategories = []
        pages = []

        # Separate subcategories and pages
        for member in category_members:
            if member["ns"] == 14:  # Namespace 14 is for categories
                subcategories.append(member["title"])
            elif member["ns"] == 0:  # Namespace 0 is for pages
                pages.append((member["title"], current_depth))

        return subcategories, pages

    def get_root_depth(current_category):
        # Set up API request to get parent categories and calculate depth
        depth = 0
        current_categories = [current_category]

        while current_categories:
            next_categories = []
            for category in current_categories:
                # Request the parent categories
                params = {
                    "action": "query",
                    "format": "json",
                    "prop": "categories",
                    "titles": category,
                    "cllimit": "max",
                    "clshow": "!hidden"  # Exclude hidden categories
                }
                response = requests.get(base_url, params=params)
                data = response.json()

                pages = data.get("query", {}).get("pages", {})
                for page_id, page_info in pages.items():
                    parent_categories = page_info.get("categories", [])
                    next_categories.extend([cat['title'] for cat in parent_categories])

            if next_categories:
                depth += 1
                current_categories = next_categories
            else:
                break

        return depth

    # BFS to explore subcategories and collect pages with depth
    depth = 0
    queue = [(category, depth)]
    visited_categories = set()
    all_pages_with_depth = []

    while queue:
        current_category, current_depth = queue.pop(0)
        if current_category in visited_categories:
            continue
        visited_categories.add(current_category)

        # Get subcategories and pages
        subcategories, pages = get_subcategories_and_pages(current_category, current_depth)

        if not use_bfs_depth:  # If we want to use root-based depth
            pages = [(title, get_root_depth(current_category)) for title, _ in pages]

        all_pages_with_depth.extend(pages)

        # Add subcategories to the queue with incremented depth (only for BFS)
        for subcategory in subcategories:
            queue.append((subcategory, current_depth + 1))

    return all_pages_with_depth


def get_pages_and_deepest_depth_from_category(category):
    base_url = "https://ja.wikipedia.org/w/api.php"
    
    def get_subcategories_and_pages(current_category, current_depth):
        # Set up API request to get subcategories and pages
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": current_category,
            "cmlimit": "max",
            "cmtype": "subcat|page"
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        category_members = data.get("query", {}).get("categorymembers", [])
        subcategories = []
        pages = []

        # Separate subcategories and pages
        for member in category_members:
            if member["ns"] == 14:  # Namespace 14 is for categories
                subcategories.append(member["title"])
            elif member["ns"] == 0:  # Namespace 0 is for pages
                pages.append(member["title"])

        return subcategories, pages

    def get_deepest_category_depth(page_title):
        # Retrieve all categories the page belongs to and calculate the depth
        params = {
            "action": "query",
            "format": "json",
            "prop": "categories",
            "titles": page_title,
            "cllimit": "max",
            "clshow": "!hidden"  # Exclude hidden categories
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        max_depth = 0

        for page_id, page_info in pages.items():
            categories = page_info.get("categories", [])
            for category in categories:
                category_title = category['title']
                depth = get_category_depth_from_root(category_title)
                max_depth = max(max_depth, depth)

        return max_depth

    def get_category_depth_from_root(current_category):
        # Traverse up the category tree and return the depth from the root
        depth = 0
        current_categories = [current_category]

        while current_categories:
            next_categories = []
            for category in current_categories:
                # Request the parent categories
                params = {
                    "action": "query",
                    "format": "json",
                    "prop": "categories",
                    "titles": category,
                    "cllimit": "max",
                    "clshow": "!hidden"  # Exclude hidden categories
                }
                response = requests.get(base_url, params=params)
                data = response.json()

                pages = data.get("query", {}).get("pages", {})
                for page_id, page_info in pages.items():
                    parent_categories = page_info.get("categories", [])
                    next_categories.extend([cat['title'] for cat in parent_categories])

            if next_categories:
                depth += 1
                current_categories = next_categories
            else:
                break

        return depth

    # BFS to explore subcategories and collect pages with depth
    queue = [category]
    visited_categories = set()
    all_pages_with_depth = {}

    while queue:
        current_category = queue.pop(0)
        if current_category in visited_categories:
            continue
        visited_categories.add(current_category)

        # Get subcategories and pages
        subcategories, pages = get_subcategories_and_pages(current_category, 0)

        # Calculate the deepest depth for each page
        for page in pages:
            deepest_depth = get_deepest_category_depth(page)
            all_pages_with_depth[page] = deepest_depth

        # Add subcategories to the queue for further exploration
        queue.extend(subcategories)

    return all_pages_with_depth

# titles = get_wikipedia_links("算数", n_hops=1)
# print(titles)

# titles = get_wikipedia_links("理科", n_hops=2)
# print(titles)

# titles = get_wikipedia_links("国語", n_hops=2)
# print(titles)

# titles = get_wikipedia_links("日本史", n_hops=2)
# print(titles)

# titles = get_wikipedia_links("世界史", n_hops=2)
# print(titles)

# titles = get_wikipedia_links("英語", n_hops=2)
# print(titles)


# titles = get_subcategory_titles('Category:学科別分類', depth=1)
# print(titles)
# titles = get_subcategory_titles('Category:主題別分類', depth=1)
# print(titles)
# titles = get_subcategory_titles('言語学', depth=2)
# print(titles)



category="Category:機械学習"
# print("bfs")
# pages_with_bfs_depth = get_pages_and_depth_from_category(category, use_bfs_depth=True)
# for title, depth in pages_with_bfs_depth:
#     print(f"Page title: {title}, BFS Depth: {depth}")

# print("ルートカテゴリからの深さ")
# pages_with_root_depth = get_pages_and_depth_from_category(category, use_bfs_depth=False)
# for title, depth in pages_with_root_depth:
#     print(f"Page title: {title}, Root Depth: {depth}")

pages_with_root_depth = get_pages_and_deepest_depth_from_category(category)
for title, depth in pages_with_root_depth:
    print(f"Page title: {title}, Root Depth: {depth}")
