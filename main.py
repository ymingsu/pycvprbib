# This script is created by Yming Su. At 2021-10-11
# 
from requests_html import HTMLSession, AsyncHTMLSession
import re
from urllib.parse import urlparse

session = HTMLSession()


# asession = AsyncHTMLSession()

def get_bib_from_sel(r, sel):
    mylist = []
    try:
        results = r.html.find(sel)
        for result in results:
            mytext = result.text
            # mylink = list(result.absolute_links)[0]
            mylist.append(mytext)
        return mylist
    except:
        return None


def get_bib_from_url(url):
    # session = HTMLSession()
    r = session.get(url)
    sel = "#content > dl > dd > div > div"
    # with open("cvpr20200618.bib", "w") as outfile:
    #    outfile.write("\n".join(get_bib_from_sel(r,sel)))


def get_bibtext_from_sel(r, sel):
    try:
        results = r.html.find(sel)
        # print(results)
        mytext = results[0].text
        return mytext
    except:
        return ""


def get_abstext_from_xpath(r, xpath):
    try:
        results = r.html.xpath(xpath)
        print("results is " + results)
        mytext = results[0].text
        return mytext
    except:
        return ""


def get_all_bib_from_paper_url(paperurl):
    try:
        r = session.get(paperurl)
        # bouu=requests.get(paperurl)
        # print(bouu.text)
        absel = "#abstract"
        # absxpath='/html/body/div[3]/dl/div[3]'
        bibsel = "#content > dl > dd > div > div"
        abstract = get_bibtext_from_sel(r, absel)
        # print("abstract is"+abstract)
        # if abstract=='':
        #     abstract=get_abstext_from_xpath(r,absxpath)
        #     print("abstract is"+abstract)
        bib = get_bibtext_from_sel(r, bibsel)
        abstractpart = ", abstract = {" + abstract + "}}"
        bibadded = bib[0:-2] + abstractpart
        return bibadded
    except:
        return ""


def get_paper_suburl(suburl):
    print("processing url " + suburl)
    subsel = "#content > dl > dt > a"
    # document.querySelector("#content > dl > dt:nth-child(2) > a")document.querySelector("#content > dl > dt:nth-child(5) > a")
    r = session.get(suburl)
    paper_urls = get_url_from_sel(r, subsel)
    return paper_urls


def get_sub_url(url):
    sel = "#content > dl > dd > a"
    r = session.get(url)
    sub_urls = get_url_from_sel(r, sel)
    # print(sub_urls)
    allidx = -1
    for idx in range(len(sub_urls)):
        o = urlparse(sub_urls[idx])
        if o.query == "day=all":
            allidx = idx
            break
    return sub_urls, allidx


def get_url_from_sel(r, sel):
    mylist = []
    try:
        results = r.html.find(sel)
        for result in results:
            mylink = list(result.absolute_links)[0]
            mylist.append(mylink)
        return mylist
    except:
        return None


def get_filename(url):
    o = urlparse(url)
    isroot = True
    match = re.match(r"([a-z]+)([0-9]+)", o.path.removeprefix('/'), re.I)
    paper_name = "CVPR"
    if match:
        items = match.groups()
        paper_name = items[0]
        paper_year = int(items[1])
        if paper_year<2018:# rooturl contain all papers
            isroot = False
    filename = o.path.removeprefix('/') + ".bib"
    if o.query != '':
        isroot = False
        filename = paper_name + o.query[4:len(o.query)] + ".bib"
        if o.query == "day=all":
            filename = o.path.removeprefix('/') + o.query.removeprefix('day=') + ".bib"
    return (isroot, filename)


def save_bib_from_url(url):
    [isroot, filename] = get_filename(url)
    # print(filename)
    papers_urls = []
    if isroot:
        [sub_urls, allidx] = get_sub_url(url)
        print(allidx)
        if allidx != -1:
            papers_urls.append(get_paper_suburl(sub_urls[allidx]))
        else:
            for sub_url in sub_urls:
                papers_url = get_paper_suburl(sub_url)
                papers_urls.append(papers_url)
    else:
        papers_urls.append(get_paper_suburl(rooturl))
    bibs = []
    print(len(papers_urls))
    for paper_url in papers_urls:
        bib = get_all_bib_from_paper_url(paper_url)
        bibs.append(bib)
    with open(filename, "w") as outfile:
        outfile.write("\n".join(bibs))


def save_bibs_from_url(url):
    [isroot, filename] = get_filename(url)
    # print(filename)
    if isroot:
        [sub_urls, allidx] = get_sub_url(url)
        for idx in range(len(sub_urls)):
            if idx == allidx:
                continue
            save_bib_from_suburl(sub_urls[idx])
    else:  # is sub url
        save_bib_from_suburl(url)


def save_bib_from_suburl(suburl):
    [isroot, filename] = get_filename(suburl)
    print(filename)
    bibs = []
    papers_urls = get_paper_suburl(suburl)
    lens = len(papers_urls)
    print(str(lens) + ' items included')
    for paper_url in papers_urls:
        bib = get_all_bib_from_paper_url(paper_url)
        bibs.append(bib)
    with open(filename, "w", encoding= "utf-8") as outfile:
        outfile.write("\n".join(bibs))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rooturl = 'https://openaccess.thecvf.com/CVPR2022'
    baseurl = 'https://openaccess.thecvf.com/CVPR2021?day=2021-06-21'
    url2 = 'https://openaccess.thecvf.com/CVPR2020?day=2020-06-18'
    url3 = 'https://openaccess.thecvf.com/CVPR2022?day=2022-06-21'
    urlall = 'https://openaccess.thecvf.com/CVPR2022?day=all'
    # paperurl = 'https://openaccess.thecvf.com/content/CVPR2021/html/Liu_Invertible_Denoising_Network_A_Light_Solution_for_Real_Noise_Removal_CVPR_2021_paper.html'
    # document.querySelector("#content > dl > dd:nth-child(1) > a")

    # save_bib_from_url(rooturl)
    save_bibs_from_url(urlall)
    # save_bib_from_suburl(baseurl)
    # get_bib_from_url(url)
    # bib=get_all_bib_from_paper_url(paperurl)
    # print(bib)
