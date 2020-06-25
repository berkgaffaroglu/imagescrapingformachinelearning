import json,shutil,os, urllib.request, re, threading, posixpath, urllib.parse, argparse, socket, time, hashlib, pickle, signal, imghdr
if os.path.exists('workspace') == True:
    shutil.rmtree('workspace')
    
#config
output_dir = './workspace' #default output dir
adult_filter = True #Do not disable adult filter by default
socket.setdefaulttimeout(2)

tried_urls = []
image_md5s = {}
in_progress = 0
urlopenheader={ 'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
siteList = list()
with open('siteler.json') as e:
    data = json.load(e)

for site in data['siteler']:
    siteList.append(site)
    
j = -1
def getCurrentWebsite():
    global j
    if j >= len(siteList)-1:
        j = 0
        return siteList[j]
    else:
        j+=1
        return siteList[j]

def download(pool_sema: threading.Semaphore, url: str, output_dir: str):
    global in_progress

    if url in tried_urls:
        return
    pool_sema.acquire()
    in_progress += 1
    path = urllib.parse.urlsplit(url).path
    filename = posixpath.basename(path).split('?')[0] #Strip GET parameters from filename
    name, ext = os.path.splitext(filename)
    name = name[:36].strip()
    filename = name + ext

    try:
        request=urllib.request.Request(url,None,urlopenheader)
        image=urllib.request.urlopen(request).read()
        if not imghdr.what(None, image):
            return

        md5_key = hashlib.md5(image).hexdigest()
        if md5_key in image_md5s:
            return

        i = 0
        while os.path.exists(os.path.join(output_dir, filename)):
            if hashlib.md5(open(os.path.join(output_dir, filename), 'rb').read()).hexdigest() == md5_key:
                return
            i += 1
            filename = "%s-%d%s" % (name, i, ext)

        image_md5s[md5_key] = filename

        imagefile=open(os.path.join(output_dir, filename),'wb')
        imagefile.write(image)
        imagefile.close()
        tried_urls.append(url)
    except Exception as e:
       pass
    finally:
        pool_sema.release()
        in_progress -= 1

def fetch_images_from_keyword(pool_sema: threading.Semaphore, keyword: str, output_dir: str, filters: str, limit: int):
    current = 0
    last = ''
    while True:
        time.sleep(0.1)

        if in_progress > 10:
            continue

        request_url='https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(keyword) + '&first=' + str(current) + '&count=35&adlt=' + adlt + '&qft=' + ('' if filters is None else filters)
        request=urllib.request.Request(request_url,None,headers=urlopenheader)
        response=urllib.request.urlopen(request)
        html = response.read().decode('utf8')
        links = re.findall('murl&quot;:&quot;(.*?)&quot;',html)
        try:
            if links[-1] == last:
                return
            for index, link in enumerate(links):
                if limit is not None and current + index >= limit:
                    return
                t = threading.Thread(target = download,args = (pool_sema, link, output_dir))
                t.start()
                current += 1
            last = links[-1]
        except IndexError:
            return

def backup_history(*args):
    download_history = open(os.path.join(output_dir, 'download_history.pickle'), 'wb')
    pickle.dump(tried_urls,download_history)
    copied_image_md5s = dict(image_md5s)  #We are working with the copy, because length of input variable for pickle must not be changed during dumping
    pickle.dump(copied_image_md5s, download_history)
    download_history.close()
    if args:
        exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Bing image bulk downloader')
    parser.add_argument('-s', '--search-string', help = 'Keyword to search', required = False)
    parser.add_argument('-f', '--search-file', help = 'Path to a file containing search strings line by line', required = False)
    parser.add_argument('-o', '--output', help = 'Output directory', required = False)
    parser.add_argument('--adult-filter-on', help ='Enable adult filter', action = 'store_true', required = False)
    parser.add_argument('--adult-filter-off', help = 'Disable adult filter', action = 'store_true', required = False)
    parser.add_argument('--filters', help = 'Any query based filters you want to append when searching for images, e.g. +filterui:license-L1', required = False)
    parser.add_argument('--limit', help = 'Make sure not to search for more than specified amount of images.', required = False, type = int)
    parser.add_argument('--threads', help = 'Number of threads', type = int, default = 20)
    args = parser.parse_args()
    if (not args.search_string) and (not args.search_file):
        parser.error('Provide Either search string or path to file containing search strings')
    if args.output:
        output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_dir_origin = output_dir
    signal.signal(signal.SIGINT, backup_history)
    try:
        download_history = open(os.path.join(output_dir, 'download_history.pickle'), 'rb')
        tried_urls=pickle.load(download_history)
        image_md5s=pickle.load(download_history)
        download_history.close()
    except (OSError, IOError):
        tried_urls=[]
    if adult_filter:
        adlt = ''
    else:
        adlt = 'off'
    if args.adult_filter_off:
        adlt = 'off'
    elif args.adult_filter_on:
        adlt = ''
    pool_sema = threading.BoundedSemaphore(args.threads)
    def searchFor(tag):
        fetch_images_from_keyword(pool_sema, tag,output_dir, args.filters, args.limit)
    if args.search_string:
        pass
    elif args.search_file:
        try:
            inputFile=open(args.search_file)
        except (OSError, IOError):
            exit(1)
        for keyword in inputFile.readlines():
            output_sub_dir = os.path.join(output_dir_origin, keyword.strip().replace(' ', '_'))
            if not os.path.exists(output_sub_dir):
                os.makedirs(output_sub_dir)
            fetch_images_from_keyword(pool_sema, keyword,output_sub_dir, args.filters, args.limit)
            backup_history()
            time.sleep(10)
        inputFile.close()
from tagCreator import getTagList,writeLastTag

tagList = getTagList()
with open('config.json') as e:
    data = json.load(e)

for ayar in data['ayarlar']:
    manuelWait = ayar['manuelBeklemeDakika']
    autoWait = ayar['otomatikBeklemeDakika']
    defaultMode = ayar['defaultMod']
print(f'\n{getTagList()}\n')
print("Eger yukaridaki tag listesi bos ise lütfen 'keywords.csv' dosyasini yenileyin.\n")
if defaultMode == 'a' or defaultMode == 'A':
    time.sleep(3)
    os.system('cls')
    print('Default mod olarak indirme ve yükleme seçildi.')
    mode = 'a'
elif defaultMode == 'b' or defaultMode == 'B':
    time.sleep(3)
    os.system('cls')
    print('Default mod olarak sadece indirme seçildi.')
    mode = 'b'
else:
    print("\nLütfen mod seçin:\n")
    print("a. Indirme ve yükleme için 'a' yazip Enter'a basin.")
    print("b. Sadece indirme için 'b' yazip Enter'a basin. (Dosyalar silinmez)\n")
    mode = input(':')
    os.system('cls')

from app import run
firstRun = True
for tag in tagList:
    print(f'Tag için indirme yapiliyor: {tag}')
    searchFor(tag)
    writeLastTag(tag)
    site = getCurrentWebsite()

    if mode == 'a' or mode == 'A':
        
        if site == siteList[0] and not firstRun:
            print(f'Ilk siteye geri dönüldü. Bekleme süresi bittikten sonra post atilacak. \nBekleniyor: {autoWait} dakika.')
            time.sleep(autoWait*60)
            run(tag,mode,site)
       
        else:
            run(tag,mode,site)
        firstRun = False
        
    else:
        
        run(tag,mode,site)
        print(f'Bekleniyor: {manuelWait} dakika.')
        time.sleep(manuelWait*60)





