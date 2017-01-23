from bs4 import BeautifulSoup
import requests
import urllib2
import urllib
import re
from optparse import OptionParser
import os.path
import re
import gzip
from os import popen
from random import randint
from time import sleep


'''
' This script is designed to parse tex source files from arXiv and pull out email
' addresses.
'
' This script is based on an earlier script that actually downloaded the source files
' from arXiv.
'
' Now, we download the source files in bulk ahead of time.  This script assumes we
' already have the source files in a folder somewhere.
'
'''

# Definitions and Regular Expressions 
regex_email = r'[\w\.-]+@[\w\.-]+\.[\w-]+'
source_directory = "data/input/arxiv_source"


# Extract a string between two substrings (Used to cut out TeX file from the zip archive)
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


# Make a list of all files

  ## A: Open Zip file
  for i in range(len(ids)):    # Loop over the downloaded zip archives
      try:
         f=gzip.open(str(ids[i]).replace(".", "")+'.zip','rb') # Open the archive (note this is a temp op)
         content=f.read()
         f.close()
  ## B: Trim The article from the archive, then search for emails
         article_content = find_between(content, "begin{document}", "end{document}" ) # Obviously This only works for LaTeX docs
         emails.append(re.findall(regex_email, article_content))                             # Find all emails in the Article  
         print 'Article '+str(i), re.findall(regex_email, article_content)
  #       # TBD: Add if email empty -> 'No emails found'
         pass
      except IOError:
         emails.append('')
         print 'Article '+str(i), 'IOError'  # If we want to handle more complicated file formats we might wanna give more infos on what happened.   
         pass    

  # 5) Make output tsv file with: ArxivID, First Author, Paper's title, Subject, # authors, Corresponding Email

  i=0
  tsv=""

  print 'Preparing tsv file with data: '
  file_name = field #maybe add date here
  text_file = open(file_name + ".tsv", "w")

  print 'ArXiv ID  ||  1st Author  ||                                       Article Title                               ||   Subject              ||   # of Authors ||   Emails'
  for span in soup.findAll("span", {"class" : "list-identifier"}): # Crawl the list-identifier spans and extract the arxiv_ids
      ids_raw = span.findAll('a')
      ids.append(re.sub('arXiv:', '',ids_raw[0].text.strip()))
      print ids[i],'||',first_authors[i], '||', re.sub('Title:','',titles[i].text.strip()),'||', subjects[i].text.strip(),'||',number_authors[i],'||', emails[i]
      if len(emails[i])>0 and number_authors[i]>1:
        try:
          # print i, str(emails[i][0]), str(field), str(first_authors[i]), str(re.sub('Title:','',titles[i].text.strip())), str(subjects[i].text.strip())
          tsv += str(field) + '\t' + str(ids[i]) + '\t' + str(first_authors[i])+ '\t' + str(emails[i][0]) + '\t' + str(re.sub('Title:','',titles[i].text.strip())) + '\t' +  str(subjects[i].text.strip()).encode('utf8') + '\t' + str(number_authors[i]) + '\n'
        except:
          print 'Possible unicode error!'
          #continue # TBD: Look into/improve unicode conversion
      i=i+1
  text_file.write(tsv)
  text_file.close()



fields = ['hep-ex','nlin', 'q-bio' , 'cs' , 'astro-ph', 'cond-mat', 'hep-th','math-ph','nlin','nucl-ex','nucl-th','physics','quant-ph','gr-qc','hep-lat','hep-ex','hep-ph','math','corr','q-fin','stat']
for field in fields:
  a = arxiv_retrieve(field)



