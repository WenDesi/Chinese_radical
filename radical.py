# encoding=utf-8

import re
import csv
import urllib2
from bs4 import BeautifulSoup

class Radical(object):
    dictionary_filepath = 'xinhua.csv'
    baiduhanyu_url = 'http://hanyu.baidu.com/zici/s?ptype=zici&wd=%s'

    def __init__(self):
        self.read_dictionary()

        self.origin_len = len(self.dictionary)

    def read_dictionary(self):
        self.dictionary = {}

        file = open(self.dictionary_filepath, 'rU')
        reader = csv.reader(file)

        for line in reader:
            self.dictionary[line[0].decode('utf-8')] = line[1].decode('utf-8')

        file.close()

    def write_dictionary(self):
        file_obj = open(self.dictionary_filepath, 'wb')

        writer = csv.writer(file_obj)
        for word in self.dictionary:
            writer.writerow([word,self.dictionary[word]])

        file_obj.close()

    def get_radical(self,word):
        word = word.decode('utf-8')

        if word in self.dictionary:
            return self.dictionary[word]
        else:
            return self.get_radical_from_baiduhanyu(word)

    def post_baidu(self,url):
        print url
        try:
            timeout = 5
            request = urllib2.Request(url)
            #伪装HTTP请求
            request.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
            request.add_header('connection','keep-alive')
            request.add_header('referer', url)
            # request.add_header('Accept-Encoding', 'gzip')  # gzip可提高传输速率，但占用计算资源
            response = urllib2.urlopen(request, timeout = timeout)
            html = response.read()
            #if(response.headers.get('content-encoding', None) == 'gzip'):
            #    html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
            response.close()
            return html
        except Exception as e:
            print 'URL Request Error:', e
            return None

    def anlysis_radical_from_html(self,html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        li = soup.find(id="radical")
        radical = li.span.contents[0]

        return radical

    def add_in_dictionary(self,word,radical):
        # add in file
        file_object = open(self.dictionary_filepath,'a+')
        file_object.write(word+','+radical+'\r\n')
        file_object.close()

        # refresh dictionary
        self.read_in_dictionary()

    def get_radical_from_baiduhanyu(self,word):
        url = self.baiduhanyu_url % word
        html = self.post_baidu(url)

        if html == None:
            return None

        radical = self.anlysis_radical_from_html(html)
        if radical != None:
            self.dictionary[word] = radical

        return radical



    def save(self):
        if len(self.dictionary) > self.origin_len:
            self.write_dictionary()

if __name__ == '__main__':
    r = Radical()
    print r.get_radical('棶')
    r.save()



    