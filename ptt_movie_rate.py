import requests
from bs4 import BeautifulSoup

print("*歡迎來到wei的作品：ptt電影版_電影雷度查詢（前10頁）")
print("*想看電影怕很雷被騙錢？\n*先來查查值不值得去電影院看～～")
print("*先說一下電影分類，大家別搞錯囉！ \n*好雷 = 好片\n*普雷 = 普通\n*負雷 = 爛片")
movie_name = input("請輸入電影名稱： ")
page_count = 10 #先設定爬10頁就好

def ptt_movies_cralwer():
    # 抓取指定頁數所有文章標題
    title = []
    for i in range(page_count):
        res = requests.get(f'https://www.ptt.cc/bbs/movie/search?page={i+1}&q={movie_name}')
        soup = BeautifulSoup(res.text, features='lxml')
        for entry in soup.select('.r-ent'):
            title.append(entry.select('.title')[0].text)

    # 找出標題有'雷'且有']'且沒有'Re'之分類，刪除多於之空格
    title_index = []
    for i in range(len(title)):
        if '雷' in title[i] and ']' in title[i] and 'Re' not in title[i]:
            title_index.append(title[i].split(']', 1)[0].split('[', 1)[1].replace(' ', ''))

    # count_rating
    good_count = 0
    ordinary_count = 0
    bad_count = 0
    for evaluation in title_index:
        if '好' in evaluation:
            good_count += 1
        elif '爛' in evaluation or '負' in evaluation:
            bad_count += 1
        elif '普' in evaluation and '好' not in evaluation and '爛' not in evaluation and '負' not in evaluation:
            ordinary_count += 1

    # print_result
    total_count = good_count + ordinary_count + bad_count
    if total_count == 0:
        result = "查無資料"
    else:
        good_percent = good_count / total_count * 100
        ordinary_percent = ordinary_count / total_count * 100
        bad_percent = bad_count / total_count * 100
        result = (
            f"評價總共有 {total_count} 篇\n好雷有 {good_count} 篇 / 好雷率為 {good_percent:.2f} %\n"
            f"普雷有 {ordinary_count} 篇 / 普雷率為 {ordinary_percent:.2f} %\n"
            f"負雷有 {bad_count} 篇 / 負雷率為 {bad_percent:.2f} %"
        )
    print(result)

if __name__ == "__main__":
    ptt_movies_cralwer()