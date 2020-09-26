import requests, json
import time

url = 'https://www.instagram.com/graphql/query/'

short_code = input('Please Enter a short code : ')
variables = {"shortcode": short_code,"include_reel": True,"first":100}

end_cursor = ''
count = 0

while 1:
    variables = {
        "shortcode" : short_code,
        "first" : 50,
        "after" : end_cursor
    }

    params = {
        'query_hash': 'd5d763b1e2acf209d62d22d184488e57',
        'variables' : json.dumps(variables)
    }

    r = requests.get(url, params=params).json()

    try : users = r['data']['shortcode_media']['edge_liked_by']['edges']
    except:
        print('Wait for 20 secs')
        time.sleep(20)
        continue

    for user in users:
        username = user['node']['username']
        full_name = user['node']['full_name']
        profile_pic = user['node']['profile_pic_url']
        count += 1
        print(count, username, full_name, profile_pic)

    end_cursor = r['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']
    has_next_page = r['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']
    if has_next_page == False: break
    time.sleep(2)
    # print(has_next_page)
