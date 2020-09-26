import requests, json, time, csv

url = "https://www.instagram.com/graphql/query"

short_code = input ('Plese Enter a short code: ')

end_cursor = ''
count = 0
counter_file = 1
jumlah_per_file = 1000

writer = csv.writer(open('comment_results/{} {}.csv'.format(short_code, counter_file), 'w', newline=''))
headers = ['User Name', 'Text']
writer.writerow(headers)

while 1:
    variables = {
        "shortcode": short_code,
        "first": 50,
        "after" : end_cursor
    }

    params = {
        'query_hash': 'bc3296d1ce80a24b1b6e40b1e72903f5',
        'variables' : '{"shortcode":"B3u1usagA36","first":12}'
    }

    r = requests.get(url, params=params).json()

    try:
        users = r['data']['shortcode_media']['edge_media_to_parent_comment']['edges']
    except:
        print('Wait for 20 secs')
        time.sleep(20)
        continue

    for user in users:
        if count % jumlah_per_file == 0 and count != 0:
            counter_file += 1
            writer = csv.writer(open('comment_result/{} {}.csv'.format(short_code, counter_file), 'w', newline=''))
            headers = ['User Name', 'text']
            writer.writerow(headers)
        username = (user['node']['owner']['username'])
        text = user['node']['text']
        # writer = csv.writer(open('comment_results/{} {}.csv'.format(short_code), 'a' , newline='', encoding='utf-8'))
        data = [username, text]
        writer.writerow(data)
        count += 1
        print(count, username, text)

    end_cursor = r['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']
    has_next_page = r['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']
    if has_next_page == False: break
    time.sleep(2)

