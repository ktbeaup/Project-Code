
#import urllib to access webpages and Beautiful soup in order to interprate the HTML.
import urllib.request
from bs4 import BeautifulSoup

#Allow user to input a search term to analyze, then format that search term and append it to the Google URL.
search_term = input('Input Search Term:\n')
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
corr_searches_90 = list(filter(lambda x: x[1]>.9,corr_searches))

print('Search Terms related to '+search_term+' are:\n')
print(corr_searches_90)
