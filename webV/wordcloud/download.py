import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# df1 = pd.read_csv('kyweibo.csv', encoding='utf-8')
# df1 = pd.read_csv('计算机专业考研weibo.csv', encoding='utf-8')
# df1 = df1.fillna('') # 将NaN值替换成空字符串


# df2 = pd.read_csv('kyzhihu.csv',encoding='utf-8')
# df2 = pd.read_csv('计算机专业考研zhihu.csv',encoding='utf-8')
# df2 = df2.fillna('') # 将NaN值替换成空字符串
# 
# text = ' '.join(df1['content'].tolist() + df1['topic'].tolist()+df2['title'].tolist()+df2['content'].tolist())
# wc = WordCloud(font_path = r'./MSYH.TTC')
# wc.generate(text)
 
# plt.imshow(wc)
# plt.axis("off") # 不显示坐标轴
# plt.show()



# 分词并去除停用词
nltk.download('stopwords')
nltk.download('punkt')
