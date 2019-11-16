import requests,re,os,time,json

def QQ_lrc(name,module):
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
    for index,i in enumerate(html):
        singer_n = []
        song_info = []
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
    
    mid = html[out[0]]['songmid']
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
    html1 = str(re.sub('\[(.*?)\]','\n',res.json()['lyric']))
    html2 = str(re.sub('&#\d\d;','',html1))
    os.system('cls')
    print(html2)
    with open('{}_lrc.txt'.format(name),'w') as f:
        f.write(html2)

print('''
本工具目前仅支持QQ音乐歌词下载
更新请移步 https://github.com/gongxi-cn-ln-dl/QQmusic-Lrc_downloader
感谢使用！''')
time.sleep(4)
os.system('cls')
QQ_lrc(input('请输入歌名: ','song'))
