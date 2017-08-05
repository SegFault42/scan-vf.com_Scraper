import urllib2
import urllib
import sys
import re
import os
from BeautifulSoup import BeautifulSoup

find_chapter_name = "li  class=\"active\""
find_manga_name = "<img class=\"img-responsive\""

website = "website.html"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def save_html_file(site):
    req = urllib2.Request(site, headers=hdr)
    response = urllib2.urlopen(req)
    data = response.read()
    filename = website
    file = open(filename, 'w')
    file.write(data)
    file.close()

def get_info():
    #info[0] = chapter name, info[1] = manga name
    info = []
    file = open(website, "r")
    info.append(get_chapter_name(file))
    info.append(get_manga_name(file))
    file.close()
    return info

def get_manga_name(file):
    line = file.readline()
    while line:
        if (line.find(find_manga_name) != -1):
            break
        line = file.readline()
    manga_name = re.search("alt=\'(.*):", line)
    return manga_name.group(1)

def get_chapter_name(file):
    line = file.readline()
    while line:
        if line.find(find_chapter_name) != -1:
            break
        line = file.readline()
    chapter_name = re.search('">(.*)</a>', line)
    return chapter_name.group(1)

def create_directory(chapter_name, manga_name):
    if not os.path.exists(manga_name):
        os.makedirs(manga_name)
    if not os.path.exists(manga_name + '/' + chapter_name):
        os.makedirs(manga_name + '/' + chapter_name)

def get_png_list():
    png = []
    file = open(website, "r")
    soup = BeautifulSoup(file)
    for index, link in enumerate(soup.findAll("img")):
        if link.get("data-src") != None:
            png.append(link.get("data-src"))
            png[index] = png[index].replace(" ", "")
    return png

def save_png(chapter_name, manga_name, png):
    count = 1
    for i in png:
        req = urllib2.Request(i, headers=hdr)
        img = urllib2.urlopen(req)
        name = i.split("/")
        print "\033[1;32mDownload : \033[0m" + manga_name + "/" + chapter_name + "/" + str(name[-1])
        localFile = open(manga_name + "/" + chapter_name + "/" + str(name[-1]), 'wb')
        localFile.write(img.read())
        localFile.close()
        count += 1
    print ""

def main():
    i = 1
    while i < len(sys.argv):
        save_html_file(sys.argv[i])
        info = get_info()
        create_directory(info[0], info[1])
        png = get_png_list()
        save_png(info[0], info[1], png)
        os.remove(website)
        i += 1

if __name__ == '__main__':
    main()
