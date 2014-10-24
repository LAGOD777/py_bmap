# _*_ coding:utf-8 _*_

#xiaohei.python.seo.call.me:)

#win+python2.7.x
import json
import sys
import time
import types
import urllib
import linecache
import urllib2



reload(sys)
sys.setdefaultencoding('utf-8')


class BaiduMap:
    """
    """
    def __init__(self, keyword):
        self.keyword = keyword
        self.query = [
                ('b', '(-1599062.039999999,811604.75;24779177.96,8168020.75)'),
                ('c', '1'),
                ('from', 'webmap'),
                ('ie', 'utf-8'),
                ('l', '4'),
                ('newmap', '1'),
                ('qt', 's'),
                ('src', '0'),
                ('sug', '0'),
                ('t', time.time().__int__()),
                ('tn', 'B_NORMAL_MAP'),
                ('wd', keyword),
                ('wd2', '')
                 ]
        self.mapurl = 'http://map.baidu.com/'
        #print keyword.decode('gbk').encode('utf8')
        self.file = open('%s.txt' % keyword, 'w')
        self.count = 0
        self.count_c = 0
        self.total_num = 0
        self._get_city()

    def _fetch(self, query=None, json=True):
        data = urllib.urlencode(query)
        url = self.mapurl + '?' + data
        #print url
        #page = urllib2.urlopen(url)
        #html_doc = page.read()
        #soup = BeautifulSoup(html_doc,fromEncoding='gb18030')
        #print url
        opener = urllib.FancyURLopener()
        #time.sleep(1)
        data = opener.open(url).read()

        if json:
            return self._tojson(data)
        else:
            return data

    def _tojson(self, data):
        try:
            js = json.loads(data, 'utf-8')
        except:
            js = None

        return js

    def _get_city(self):
        data = self._fetch(self.query)
        if type(data['content']) is not types.ListType:
            print 'keyworld error.'
            sys.exit()

        self.city = data['content']

        if data.has_key('more_city'):
            for c in data['more_city']:
                self.city.extend(c['city'])


        for city in self.city:
            self.total_num += city['num']


    def _get_data(self, city, page=0):
        query = [
                ('addr', '0'),
                ('b', '(%s)' % city['geo'].split('|')[1]),
                ('c', city['code']),
                ('db', '0'),
                ('gr', '3'),
                ('ie', 'utf-8'),
                ('l', '9'),
                ('newmap', '1'),
                ('on_gel', '1'),
                ('pn', page),
                ('qt', 'con'),
                ('src', '7'),
                ('sug', '0'),
                ('t', time.time().__int__()),
                ('tn', 'B_NORMAL_MAP'),
                ('wd', self.keyword),
                ('wd2', ''),
                 ]
        data = self._fetch(query)
        return data

    def _save(self, content, city):
        for c in content:
            self.count += 1
            self.count_c += 1
            if c.has_key('tel'):
                tel = c['tel']
            else:
                tel = ''

            _data = '%s\t%s\t%s\t%s\n' % (city['name'], c['name'], c['addr'], tel)
            self.file.write(_data)
            print '(%s/%s) %s[%s/%s]' % (self.count, self.total_num, city['name'], self.count_c, city['num'])

    def get(self, city):
        self.count_c = 0

        pages = abs(-city['num'] / 10)
        for page in range(0, pages):
            data = self._get_data(city, page)
            try:
                if data.has_key('content'):
                    self._save(data['content'], city)
            except (AttributeError,TypeError,IOError):
                print 'get出现验证码！请等待.......'

    def get_all(self):
        for city in self.city:
            #print city
            try:
                self.get(city)
            except (AttributeError,TypeError,IOError):
                print 'get_all出现验证码！请等待.......'
                    
        self.file.close()
def get_citys():
    citys=[]
    count = -1
    for count,line in enumerate(open('hangye.txt', 'r')):
        pass
    count += 1
    num1 =1
    while num1<=count:
            count1 = linecache.getline('hangye.txt',num1)
            num1 +=1
            count1 = count1.strip()
            citys.append(count1)
    return citys

if __name__ == '__main__':
    citys = get_citys()
    for cti in citys:
        if sys.argv.__len__() > 1:
            keyword = sys.argv[1]
        else:
        	try:
        		keyword = cti
         
		        baidumap = BaiduMap(keyword)
		        print cti.decode('gbk').encode('utf8')
		        print '_' * 20
		        print 'CITY: %s' % baidumap.city.__len__()
		        print 'DATA: %s' % baidumap.total_num
		        baidumap.get_all()
	    	except (AttributeError,TypeError,IOError):
	    		print '出现验证码！请等待.......'
