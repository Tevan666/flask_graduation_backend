import requests, json

if __name__ == '__main__':
  target = 'https://image.baidu.com/search/albumsdata?pn=30&rn=30&tn=albumsdetail&word=%E4%BA%BA%E7%89%A9&album_tab=%E5%8A%A8%E7%89%A9&album_id=693&ic=0&curPageNum=1'
  header = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
  s = requests.Session()
  s.headers['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
  data = s.get(target).text
  json_data = json.loads(data)
  img_url = json_data['albumdata']
  for i in img_url['linkData']:
    print('url', i['thumbnailUrl'])