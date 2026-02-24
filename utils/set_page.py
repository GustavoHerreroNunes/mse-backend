def set_page(index_data, key, page_num):
    for item in index_data:
        if item["bookmark_key"] == key:
            item["page_num"] = page_num + 1
            break
