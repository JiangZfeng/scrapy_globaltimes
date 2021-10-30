import re

str = 'https://www.globaltimes.cn/page/202110/1236019.shtml'
print(re.findall(r'\d{7}',str))