import re
import jieba.analyse
import urllib.request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
page = 1
url = ''
count = Counter()
ok = False
str1 = re.compile(r'src="(http:[^=]+?\.jpg)"')
num = 0
while True:
    if page == 1:
        url = 'http://www.hbut.edu.cn/xiaoyuan/index.html'
    else:
        url = 'http://www.hbut.edu.cn/xiaoyuan/index_' + str(page) + '.html'
    page += 1
    res = urllib.request.urlopen(url)
    html = res.read().decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find(name="div", attrs={"class": "article_list"})
    con = tag.find_all("li")
    for li in con:
        if li.find(name="div", attrs={"class": "article_list_span"}).text > '2019-01-01':
            resp = urllib.request.urlopen(li.find(name="a").get("href"))
            html = resp.read().decode('utf-8')
            soup = BeautifulSoup(html, "html.parser")
            tag = soup.find(name="div", attrs={"class": "content"})
            imglist = re.findall(str1, str(tag))
            for img in imglist:
                urllib.request.urlretrieve(img, '%s.jpg' % num)
                num += 1
            text = tag.text.replace('\n', '')
            words = [word for word in jieba.cut(text, cut_all=True) if len(word) >= 2]
            count += Counter(words)
        else:
            ok = True
            break
    if ok is True:
        break
#测试（前十五的词及频数输出）
wo = count.most_common(15)
for ci in wo:
    k, v = ci
    print(str(k)+" "+str(v))
backgroud_Image = plt.imread(r'heart2.jpg')
wc = WordCloud(background_color='white', mask=backgroud_Image, max_words=80, font_path='C:/Windows/Fonts/STXINGKA.TTF', max_font_size=150, random_state=10)
wc.generate_from_frequencies(count)
image_colors = ImageColorGenerator(backgroud_Image)
wc.recolor(color_func=image_colors)
plt.imshow(wc)
plt.axis('off')
plt.show()
