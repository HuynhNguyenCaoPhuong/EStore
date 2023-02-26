# FILE NÀY CHỈ DIỄN GIẢI CÁCH HOẠT ĐỘNG CỦA API VÀ FILE JSON KHÔNG SỬ DỤNG TRONG PROJECT
# import requests

# url_api = "https://fakestoreapi.com/products/1/"
# data = requests.get(url_api)
# # data.content dủng để lấy nguyên mẫu, data.text dủng để điều chỉnh sử dụng trên model

# import json
# import urllib.request

# url = urllib.request.urlopen(
#     "http://maps.googleapis.com/maps/api/geocode/json?address=google")
# data = json.loads(url.read().decode())
# đa số sử dụng loads, load chỉ sử dụng cho xử lý file json đơn giản, do dev thường không rõ nên thường sử dụng loads cho cả file đơn giản và phức tạp
# urllib.request chỉ dùng cho các API không cài bảo mật authenticator, google giờ đã authenticator
# print(data)

import requests
import json

url_api = "https://fakestoreapi.com/products/1/"
# # data = requests.get(url_api)
# # Cách 1: cách này không sử dụng tốt
# # data = json.loads(requests.get(url_api))
# # print(data)
# # Cách 2: cách này sử dụng tốt
data = requests.get(url_api).json()
title = data['title']
description = data.get('description', 'Not available')

print(data)
print(title)
print(description)
