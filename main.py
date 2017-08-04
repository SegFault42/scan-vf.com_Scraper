import urllib2
import sys
import re
import os

site = sys.argv[1]
find_chapter_name = "li  class=\"active\""
find_manga_name = "<img class=\"img-responsive\""
website = "website.html"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def save_html_file():
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

def main():
    save_html_file()
    info = get_info()
    create_directory(info[0], info[1])
    os.remove(website)

if __name__ == '__main__':
    main()
