
set_cookie = {'passport': 'v1'}
set_cookie.update({'name': 'yang'})
print(set_cookie)

if set_cookie:
    for k, v in list(set_cookie.items()):
        print(k, v)