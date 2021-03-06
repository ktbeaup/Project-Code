#import urllib to access webpages
	#Beautiful soup in order to interprate the HTML.
	#urllib parse in order to determine attributes of a URL
	#enchantment for US-dictionary lookup

import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
import enchant



def GoogleCorrelation(search_term, perc_correlation=0):
	"""
	This function take in a search term percent correlation and returns a list of related terms from Google Correlate:
	https://www.google.com/trends/correlate
	"""

	#format that search term and append it to the Google URL.
	search_term_frmt = search_term.replace(' ','+').lower()
	url = "https://www.google.com/trends/correlate/search?e={}&t=weekly&p=us".format(search_term_frmt)

	#Google doesn't allow webscrapers ontheir sites so we need to mask our id (i.e. User Agent) by looking like a regular user.
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	headers={'User-Agent':user_agent,}
	request=urllib.request.Request(url,None,headers)
	response = urllib.request.urlopen(request)

	#read the html from the site navigated to by the urllib request.
	data = response.read()

	#ingest the HTML into bs4 package as a 'soup' object.
	soup = BeautifulSoup(data, "lxml")

	#identify the correlated search term object in the HTML 
	results = soup.find("div", {"id":"results"})

	#find the scores of the correlated search terms
	scores = [float(str(x).replace('<small>','').replace('</small>','')) for x in list(results.findAll("small"))]

	#create a list of correlated search terms
	searches = [(str(results.find("span")).replace('<span>','').replace('</span>',''))]#first search term is formatted differently in HTML
	terms_ut = [str(x) for x in results.findAll("a", {"onclick":"addHash(this);"})]#untrimmed terms via list compresion

	#loop through remaining correlated search terms (untrimmed), trim them, and append then to the searches list.
	for term in terms_ut:
	    term_t = term[term.find('">')+2:term.find('</')]
	    searches.append(term_t)

	#combine the two lists (search_terms, scores) into a list of tuples using the zip function.
	corr_searches = [(search_term,1.0)] + list(zip(searches, scores))

	#return a list of terms that are 90% similar
	return list(filter(lambda x: x[1]>(float(perc_correlation)/100),corr_searches))




def GoogleNewsLinks(search_term, date_start, date_end):
	"""
	This function returns a list of articles URLs from the Google News Advanced Search Feature.
	"""

	search_term_frmt = '%22'+search_term.replace(' ','+')+'%22'
	date_start_frmt = date_start[5:7]+'%2F'+date_start[8:10]+'%2F'+date_start[0:4]
	date_end_frmt = date_end[5:7]+'%2F'+date_end[8:10]+'%2F'+date_end[0:4]


	url = ('https://www.google.com/search?cf=all&hl=en&pz=1&ned=us&tbm=nws&gl=us&as_epq={exct}&as_occt=any&as_drrb=b&as_mindate={st1}&as_maxdate={end1}&tbs=cdr%3A1%2Ccd_min%3A{st2}%2Ccd_max%3A{end2}&authuser=0&tbas=0'
	       .format(exct=search_term_frmt,
	              st1=date_start_frmt,
	              end1=date_end_frmt,
	              st2=date_start_frmt,
	              end2=date_end_frmt))


	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	headers={'User-Agent':user_agent,}
	request=urllib.request.Request(url,None,headers)
	response = urllib.request.urlopen(request)
	data = response.read()

	soup = BeautifulSoup(data,"lxml")

	news_articles_ut = list(filter(lambda x: 'href="/url?q=' in str(x), list(soup.findAll("a"))))

	news_articles = list(set([str(x)[str(x).find('/url?q')+7:str(x).find('&amp')] for x in news_articles_ut]))

	return news_articles




def GetArticleDomain(url):
	"""
	This function returns the domain of the website which owns the article.
	"""

	return '{uri.scheme}://{uri.netloc}/'.format(uri=parse.urlparse(url))




def GetArticle(url):
    """
    This function take a URL as input and returns the content contained within the 'p'-tags of the html.
    p-tags represent paragraphs on webpages.
    
    """
    #send python to the URL and extract the data through the masked user agent 
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}
    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, "lxml")
    

    #return html contained within 'p-tags' as a list and then concatenate that list seperated with '.'
    text_body = ". ".join([str(x) for x in soup.findAll('p')])
    
    
    #replace most non-alpha characters and common tags associated with html
    replace_grammar_char = ['0','1','2','3','4','5','6','7','8','9',',',';','?','!','.','+','_','(',')','[',']','{','}','\n','%','/','#','~','<','>','*','&','=','|','"','@',':']
    replace_html = ['class','div','function','click','amp','sections','quot','com','news','var','head','buffer','script','follow','res','homepage','configuration','wrapper','byline','span','copyright']
    replace_terms = replace_grammar_char+replace_html
    
    for char in replace_terms:
        text_body = text_body.replace(char, ' ')
    text_body_words = text_body.split(' ')
    text_body_words = list(filter(lambda x: x != '' and len(x)>1, text_body_words))
     
    #import english dictionary for lookup purposes
    d = enchant.Dict("en_US")
    
    #remove words which are in the top 200 words and are less than 3 charatcers long
    relevant_words = list(filter(lambda x: d.check(x) == True, text_body_words))

    return " ".join(relevant_words)
