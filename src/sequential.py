__author__ = 'Avijit'


from goose import Goose
import lxml.html
import urllib2
from Queue import Queue
from modules_read_write import *
import time
import re
from path import path

PATH_current = path('sequential.py').abspath()
PATH = "/".join(PATH_current.split('/')[:-2])
data_store = {}
LINKS_CRAWLED = 0
DOMAINS = []
DEPTH = 2


def check_condition(page):
    title_by_goose = page.title
    if(len(title_by_goose)> 0):
        #return title_by_goose[0].isdigit() #it is condition for esl website
        return title_by_goose.endswith('Reading Comprehension')   #for uvcs websites
    else:
        return False


def extract_stories(url):
    #domain = None
    try:
        g = Goose()
        page = g.extract(url)
        domain = page.domain
        #print "avi"
        if (check_condition(page) == True):
            #print "entered"
            title_by_goose = page.title
            extracted_info = {}
            #title = ' '.join(title_by_goose.split(' ')[1:]) #set according to condition to grab correct title for ESL site
            title = title_by_goose.split(":")[1].lstrip(' ')
            story = page.cleaned_text
            meta_description = page.meta_description
            authors = page.authors                    #it's a list, as author could be multiple
            published_dates = page.publish_date
            #since story type is unicode, not string
            lines = 0
            words = 0
            para = 1
            if(len(story)!=0):
                for letter in story:
                    if(letter=='.'):
                        lines+=1
                    elif(letter==' '):
                        words+=1
                    elif(letter=='\n'):
                        para+=1
            extracted_info['title']= title
            extracted_info['story']= story
            extracted_info['para'] = para
            extracted_info['domain']= domain
            extracted_info['lines']= lines
            extracted_info['words']= words
            extracted_info['meta_description']= meta_description
            extracted_info['authors']= authors
            extracted_info['published_dates']= published_dates
            if (len(story) != 0):                       #it's 2nd check as condition above may lead to some page that has title but not story
                data_store[url] = extracted_info
                print len(data_store)
                print "link", url, "\nTitle", data_store[url]['title'], "\nStory", data_store[url]['story'], "\nParagraph", data_store[url]['para'], \
                "\ndomain:",data_store[url]['domain'], "\nlines:",data_store[url]['lines'], "\nwords:",data_store[url]['words'],"\nmeta_description:",\
                data_store[url]['meta_description'],"\nauthor",data_store[url]['authors'],"\npublished_date:",data_store[url]['published_dates'], "\n"
        #print domain
        return domain                #It is needed to enque only useful links, avoide useless links
    except:
        return None

def extract_links(q, url, url_depth, visited):
    page = None
    try:
        req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
        page = urllib2.urlopen(req)
        html = page.read()
        dom = lxml.html.fromstring(html)
        try:
            for plink in dom.xpath('//a/@href'):
                link = str(plink)
                if (link.startswith('http') is False):
                     end_of_url = url.split('/')[-1]
                     #print end_of_url
                     result = re.match(r'index.*', end_of_url) #such problem comes when many files dived in slots of 25 etc and links to rest
                     #print result
                     if(result != None):
                         url = "/".join(url.split('/')[:-1]) + "/"
                     link = str(url) + link
                curr_depth = url_depth -1
                if(curr_depth >=1 and (link not in visited)):
                    q.put((link, curr_depth), True)
        except:
            return None
    except(urllib2.URLError, ValueError):
        print "url:", url, "unable to open"


def crawl(q):
    global LINKS_CRAWLED
    visited = []
    while(q.empty() == False):
        LINKS_CRAWLED +=1
        url_tuple = q.get()
        print url_tuple
        url = url_tuple[0]
        url_depth = url_tuple[1]
        visited.append(url)
        domain = extract_stories(url)        #saves stories from the links
        #print domain
        if(domain in DOMAINS):
            extract_links(q, url, url_depth, visited)        #find and add links to the queue

def getdomain(url):
    try:
        g = Goose()
        page = g.extract(url)
        domain = page.domain
        return domain
    except:
        return None


def initialize_queue(seed_urls, depth):
    q = Queue(maxsize=0)
    #[q.put((url, depth), True) for url in seed_urls]
    for url in seed_urls:
        url = url.strip('\n')           #url has enters in the file seed.txt
        DOMAINS.append(getdomain(url))
        q.put((url, depth), True)
    crawl(q)

def check_dict_built(data_store):
    print "checking dictionary built..."
    if(len(data_store)>0):
        print "dictionary built successful.."
        print "stories extracted", len(data_store)
    else:
        print "dictionary built failed..."
        print "exiting..."
        exit()

if __name__ == "__main__":
    start_time = time.time()
    seed_urls = []
    seed_urls = load_index()
    initialize_queue(seed_urls, DEPTH)
    check_dict_built(data_store)
    write_to_file_json(data_store)
    write_stories_txt(data_store)
    print "success.."
    print "Total", LINKS_CRAWLED, "links crawled sequentially..."
    print "time:", (time.time() - start_time), "seconds"



