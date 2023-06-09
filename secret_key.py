from secrets import token_bytes
from base64 import b64encode

'''Вариант создания случайного секретного ключа на Windows(алгоритм HS256)'''

print(b64encode(token_bytes(32)).decode())
