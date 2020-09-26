import requests, json
import time, csv

url = 'https://www.instagram.com/graphql/query/'

short_code = input('Please Enter a short code : ')
variables = {"shortcode": short_code,"include_reel": True,"first":50}

end_cursor = ''
count = 0
counter_file = 1
jumlah_per_file = 1000

writer = csv.writer(open('hasil_like/{} {}.csv'.format(short_code, counter_file), 'w', newline=''))
headers = ['User Name', 'Full Name', 'Profil Pic']
writer.writerow(headers)

while 1:
    variables = {
        "shortcode" : short_code,
        "first" : 50,
        "after" : end_cursor
    }

    params = {
        'query_hash': 'bc3296d1ce80a240b1e72903f5',
        'variables' : json.dumps(variables)
    }

    r = requests.get(url, params=params).json()

    try : users = r['data']['shortcode_media']['edge_liked_by']['edges']
    except:
        print('Wait for 20 secs')
        time.sleep(20)
        continue

    for user in users:
        if count % jumlah_per_file == 0 and count != 0:
            counter_file += 1
            writer = csv.writer(open('hasil_like/{} {}.csv'.format(short_code, counter_file), 'w', newline=''))
            headers = ['User Name', 'Full Name', 'Profil Pic']
            writer.writerow(headers)
        username = user['node']['username']
        full_name = user['node']['full_name']
        profile_pic = user['node']['profile_pic_url']
        count += 1
        print(count, username, full_name, profile_pic)
        writer = csv.writer(open('hasil_like/{}.csv'.format(short_code), 'a', newline='', encoding='utf-8'))
        data = [username, full_name, profile_pic]
        writer.writerow(data)

        end_cursor = r['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']
        has_next_page = r['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']
        if has_next_page == False: break
        time.sleep(2)
    # print(has_next_page)
