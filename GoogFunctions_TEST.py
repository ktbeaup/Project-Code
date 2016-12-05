
#import urllib to access webpages and Beautiful soup in order to interprate the HTML.
from GoogFunctions import GoogleCorrelation, GoogleNewsLinks, GetArticle, GetArticleDomain

input_term = input('Enter a search term: \n')
input_corr = input('Enter minimum correlation threshold percent (ex. 90): \n')

print('search terms related to '+input_term+' are:\n')
print(GoogleCorrelation(input_term, input_corr))


input_start = input('Enter a start date (yyyy-mm-dd): \n')
input_end = input('Enter a end date (yyyy-mm-dd): \n')

print('article terms related to '+input_term+' are:\n')
print(GoogleNewsLinks(input_term, input_start, input_end))


input_url = input('Enter an articles URl: \n')
print('article states:\n')
print(GetArticle(input_url))

print('This article come from: '+GetArticleDomain(url))