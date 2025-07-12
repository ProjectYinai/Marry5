import os
import json
import random
import time
script_path = os.path.split(os.path.realpath(__file__))[0]
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

def generate_hitokoto_message():
    categories = load_categories(f"{script_path}/categories.json")
    if not categories:
        result = {"code":500,"status":"error","message":"No categories found"}
        return result
    cat_obj = random.choice(categories)
    key = cat_obj.get('key', '') 
    catname = cat_obj.get('desc', cat_obj.get('name', key))
    sentences = load_sentences_by_key(f'{script_path}/sentences', key)
    if not sentences:
        result = {"code":500,"status":"error","message":"No sentences found for key: %s" % key}
        return result
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
    return result
