import os
import json
import random
import time

def load_categories(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_sentences_by_key(sentences_dir, key):
    filepath = os.path.join(sentences_dir, f'{key}.json')
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return []

def main():
    categories = load_categories('categories.json')
    if not categories:
        print(json.dumps({"code":500,"status":"error","message":"No categories found"}, ensure_ascii=False))
        return
    cat_obj = random.choice(categories)
    key = cat_obj.get('key', '') 
    catname = cat_obj.get('desc', cat_obj.get('name', key))
    sentences = load_sentences_by_key('sentences', key)
    if not sentences:
        print(json.dumps({"code":500,"status":"error","message":"No sentences found for key: %s" % key}, ensure_ascii=False))
        return
    s = random.choice(sentences)
    _id = s.get('id') or int(time.time() * 1000)
    _date = s.get('date') or int(_id // 1000)
    result = {
        "code": 200,
        "status": "success",
        "response": {
            "data": {
                "id": _id,
                "hitokoto": s.get('hitokoto', ''),
                "cat": key,
                "catname": catname,
                "author": s.get("creator", ''),
                "source": s.get("from", '')
            }
        }
    }
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
