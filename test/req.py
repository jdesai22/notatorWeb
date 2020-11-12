import requests
import sys
import time

def add_to_cart(item_id, size_id, style_id, task_name, screenlock):
    """
    Add an item to cart with a specific item_id, size_id, and style_id.
    Only return session object if item added to cart properly.
    """

    s = requests.Session()
    atc_url = "https://www.supremenewyork.com/shop/"+item_id+"/add.json"

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.supremenewyork.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.supremenewyork.com/mobile/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }

    data = {
        "s": size_id,
        "st": style_id,
        "qty": "1"
    }

    atc_post = s.post(atc_url, headers=headers, data=data)
    if atc_post.json():
        if atc_post.json()['cart'][0]["in_stock"]:
        #     with screenlock:
            print(task_name + ": Added to Cart")
            return s


if __name__ == "__main__":
    add_to_cart("28883", "83764", "173749", "test", "nothing")