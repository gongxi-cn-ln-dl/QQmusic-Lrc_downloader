import json
import os
import re
import sys
import time

import requests


def lrc_QQ(name,module):
    song_name = str(name.encode('utf-8'))
    song_name = song_name.replace('\\x','%')[:-1]
    song_name = song_name[2:]
    #print(song_name)
    
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p=1&n=15&w='+song_name
    
    res = requests.get(url)
    #print(res.text)
    html = json.loads(res.text.replace('callback(','')[:-1])['data'][module]['list']
    #print(html[0])
    song_ns = []
    singer_li = []
    for index,i in enumerate(html):
        singer_n = []
        for x in i['singer']:
            singer_n.append(x['name'])
        song_ns.append((index,'歌名： {}\n'.format(i['songname'])+'歌手： '+'  &  '.join(singer_n)+'\n'))
    
    for i in song_ns:
        out = []
        print(i[1])
        choice = input('这是不是您要找的歌？是请按1，不是请按任意键')
        if choice == '1':
            out = i
            break
    #print(html[out[0]])
    mid = html[out[0]]['songmid']
    for i in html[out[0]]['singer']:
        singer_li.append(i['name'])
    url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg?nobase64=1&musicid={}&-=jsonp1&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'.format(html[out[0]]['songid'])
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'https://y.qq.com',
    'Referer': 'https://y.qq.com/n/yqq/'+module+'/'+mid+'.html',
    #'User-Agent':' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    res = requests.get(url,headers=headers)#
    html1 = ''
    html2 = ''
    html1 = str(re.sub('\[(.*?)\]','',res.json()['lyric']))
    html2 = str(re.sub('&#10;','\n',html1))
    html3 = str(re.sub('&#32;',' ',html2))
    html3 = str(re.sub('&#39;','\'',html3))
    html3 = str(re.sub('&#38;apos&#59;','\'',html3))
    html3 = str(re.sub('&#\d\d;','',html3))
    #os.system('cls')
    #print(html3)
    with open('{}-{}.txt'.format(name,' & '.join(singer_li)),'w',encoding = 'utf-8') as f:
        f.write(html3)

def lrc_163(name):
    name1 = str(name.encode('utf-8'))[3:-1]
    print(name)
    data={
    'types': 'search',
    'count': '20',
    'source': 'netease',
    'pages': '1',
    'name': name
    }
    url_1 = 'http://www.gequdaquan.net/gqss/api.php?callback=jQuery1113019331792980069662_1573970728286'
    url2='http://www.gequdaquan.net/gqss/api.php?callback=jQuery1113019331792980069662_1573970728286'
    res=requests.post(url_1,data=data)
    #print(res.text)
    text=re.sub('jQuery1113019331792980069662_1573970728286\(','',res.text)[:-1]
    
#print(text)
    song_list=json.loads(text)
    for i in song_list:
        #print(i)
        print('\n歌曲:    '+i['name'],'\n歌手：   '+' & '.join(i['artist']),'\n专辑：   '+i['album'])
        asw=input('这首是不是您需要的？是请按1，不是请按任意键')
        if asw == '1':
            data2={
            'types': 'lyric',
            'id': str(i['lyric_id']),
            'source': 'netease'
            }
            res=requests.post(url2,data=data2)
            #print(res.text)
            song=re.sub('jQuery1113019331792980069662_1573970728286\(','',res.text)
            song=re.sub('\)','',song)
            #print(song)
            if str(song) == '{"lyric":"","tlyric":""}':
                print('该歌曲无歌词')
                time.sleep(5)
                sys.exit()
            song_url=json.loads(song)
            #song_url=song_url.replace('\\','')[0]
            #print(song_url)
            #song_url = song_url['lyric'].decode('utf-8')
            html = re.sub('\[(.*?)\]','',song_url['lyric'])
            print(html)
            with open('{}-{}.txt'.format(name,' & '.join(i['artist'])),'w',encoding = 'utf-8') as f:
                f.write(html)
            break
print('''
本工具目前支持网易云和QQ音乐歌词下载
更新请移步 https://github.com/gongxi-cn-ln-dl/QQmusic-Lrc_downloader
感谢使用！''')
time.sleep(3)
os.system('cls')
cho = input('''
请选择播放器
1.网易云音乐
2.QQ音乐''')
if cho == '1':
    lrc_163(input('请输入歌名: '))
elif cho == '2':
    lrc_QQ(input('请输入歌名: '),'song')
else:
    print('请重新输入！')
