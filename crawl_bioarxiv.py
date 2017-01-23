from bs4 import BeautifulSoup
import requests
import urllib
import io

def bioarxiv_find_links(soup):
	list=[]
	data = soup.findAll('div',attrs={'class':'highwire-cite-title'})    # Finds Preprints divs
	for div in data:
	 links = div.findAll('a')                                           # For every Prerprint Divs, scrape hyperlink
	 for a in links:
	  list.append("http://biorxiv.org" + a['href']+'.article-info')     # Add full path to preprint info to the list
	return list;  

def bioarxiv_meta(soup):  # BioArXiv entries contain all the relevant info as Meta tags. So it's supereasy to scrape
	try:
		result = None
		citation_author = soup.find("meta", {"name":"citation_author"})
		citation_author_email = soup.find("meta", {"name":"citation_author_email"})
		citation_author_institution = soup.find("meta", {"name":"citation_author_institution"})
		citation_title= soup.find("meta", {"name":"citation_title"})
		published_time= soup.find("meta", {"name":"article:published_time"})
		#author_orcid= soup.find("meta", {"name":"citation_author_orcid"}) 
		authors_number = len(soup.findAll("meta", {"name":"citation_author"}))
		citation_author_emails = soup.findAll("meta", {"name":"citation_author_email"})
		if (citation_author is not None) and (citation_author_email is not None) and (citation_author_institution is not None) and (published_time is not None) and (authors_number is not None):
			result=[citation_title['content'],citation_author['content'],citation_author_email['content'],citation_author_institution['content'],published_time['content'],str(authors_number)] 
		return result;
	except ValueError:
		return None;

### Main Loop

links_list = []
url='http://biorxiv.org/search/numresults%3A100%20sort%3Arelevance-rank%20format_result%3Acondensed?page=' # Bioarxiv URL 
# Creating loop over listing pages 
for N in range(0,39):                     # Bioarxiv only shows 40 pages. This is fine for now, but we can scrape the whole site by refining search by subject (see bottom)
	r  = requests.get(url+str(N))         # Request url 
	dataURL = r.text                 
	soup = BeautifulSoup(dataURL,'lxml')  # Use BeautifulSoup -> HTML (using lxml parser. Faster than html5lib, but beware of compatibility issues)
	links_list.extend(bioarxiv_find_links(soup))  # Find all links to preprints
unique_links_list = list(set(links_list)) # Remove eventual duplicates using sets (Note that sets change the elements order)
print(unique_links_list)

# Iterate over list of links, extract Author info and Email and create final database
# Format: First Author   Email   Title   Institute   Publication Date   Number of Authors 
tsv=""
file_name = 'bioarxiv'
text_file = io.open(file_name + ".tsv", 'w', encoding='utf8') 
for link in unique_links_list:
	r =  requests.get(link)
	dataAbstract = r.text
	soup = BeautifulSoup(dataAbstract,'lxml')
	meta=bioarxiv_meta(soup)
	print(meta)
	if meta is not None:
		try:
			tsv += str(meta[1]) + '\t' + str(meta[2]) + '\t' + str(meta[0]) + '\t' + str(meta[3]) + '\t' + str(meta[4]) + '\t' + str(meta[5]) + '\n'
		except TypeError:
			print('TypeError for: ' + meta)
			continue
text_file.write(tsv)
text_file.close()

### End 

# Notes for extending the script: 
# Search by subject
#http://biorxiv.org/search/subject_collection_code%3AAnimal%20Behavior%20and%20Cognition%20numresults%3A100%20sort%3Apublication-date%20direction%3Adescending%20format_result%3Acondensed
#http://biorxiv.org/search/subject_collection_code%3AAnimal%20Behavior%20and%20Cognition%20numresults%3A100%20sort%3Apublication-date%20direction%3Adescending%20format_result%3Acondensed?page=1
# Since we don't know how many pages are returned, will have to stop when listed results in page are equal to previous page OR results in previous page <100
#http://biorxiv.org/search/subject_collection_code%3ABiochemistry%20numresults%3A100%20sort%3Apublication-date%20direction%3Adescending%20format_result%3Acondensed
#http://biorxiv.org/search/subject_collection_code%3ABioengineering%20numresults%3A100%20sort%3Apublication-date%20direction%3Adescending%20format_result%3Acondensed


