from google import search
import urllib.request, urllib.error, urllib.parse
import re
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
import time

ALL_RESULTS=[]
ALL_ANSWERS_SORTED=[]
ALL_ANSWERS=dict()
IGNORE_LIST=['countries','country','cities','city','continent','continents','nation','state','states',
             'Countries','Country','Cities','City','Continent','Continents','Nation','State','States',
             'in','on','In','On','return','Return','link','Link']

def check_WordNet(word='Himalayas',def_word='mountain'):
  match_found=0
  D=wn.synsets(word)
  if D!=[]:
    for each in D:
      def1=each.definition()
      #print def1
      def1=def1.split(' ')
      c=0
      for each_d in def1:
        c+=1
        if def_word.lower()==each_d.lower():
          match_found=1
          break
        if c>9:
          break

  return match_found
  

def Tell_Me_Alfred(query="The Himalayas are",answer_type="Description"):

  global ALL_RESULTS
  global ALL_ANSWERS_SORTED
  global ALL_ANSWERS
  ALL_RESULTS=[]
  ALL_ANSWERS=dict()

  for url in search(query, stop=20):
    try:
      #print(url)
      ALL_RESULTS.append(url)
    except:
      print("URL Error")

  #ALL_RESULTS=['http://www.victoriamemorial-cal.org/', 'http://www.tripadvisor.in/Attraction_Review-g304558-d311680-Reviews-Victoria_Memorial_Hall-Kolkata_Calcutta_West_Bengal.html', 'http://kolkata.cityseekr.com/venue/403224-victoria-memorial', 'http://www.thecityguide.in/Kolkata/Art-Entertainment/SGGG/Victoria-Memorial-Elgin', 'http://www.justdial.com/Kolkata/Victoria-Memorial-Hall/033P6853927_BZDET', 'http://en.wikipedia.org/wiki/Victoria_Memorial_(India)', 'http://en.wikipedia.org/wiki/Victoria_Memorial_(India)#History', 'http://en.wikipedia.org/wiki/Victoria_Memorial_(India)#Finance', 'http://en.wikipedia.org/wiki/Victoria_Memorial_(India)#Design', 'http://en.wikipedia.org/wiki/Victoria_Memorial_(India)#Construction', 'http://ww.itimes.com/poll/best-image-of-victoria-memorial-kolkata-54ad5bd294fa2', 'http://www.trekearth.com/gallery/Asia/India/East/West_Bengal/Kolkata_(Calcutta)/photo1412050.htm', 'http://www.culturalindia.net/monuments/victoria-memorial.html', 'http://knowindia.gov.in/knowindia/culture_heritage.php?id=68', 'http://www.youtube.com/watch?v=C_0IvslcRqU', 'http://www.ixigo.com/victoria-memorial-kolkata-india-ne-1019165', 'http://www.lonelyplanet.com/india/kolkata-calcutta/sights/architecture/victoria-memorial', 'http://www.indianholiday.com/tourist-attraction/kolkata/victoria-memorial.html', 'http://www.mapsofindia.com/kolkata/places-of-interest/famous-monuments/victoria-memorial.html', 'https://www.facebook.com/pages/Victoria-Memorial-Hall-Kolkata/113100222172879', 'http://www.iloveindia.com/indian-monuments/victoria-memorial.html', 'http://www.kolkata.org.uk/tourist-attractions/victoria-memorial.html', 'http://www.vmsb.org/contact_us.html', 'http://mocomi.com/victoria-memorial-facts/', 'http://www.journeymart.com/de/india/west-bengal/kolkata/victoria-memorial.aspx', 'http://www.theincredibleindiatravel.com/victoria-memorial-hall-india/victoria-memorial.html', 'http://goindia.about.com/od/cities/ig/Kolkata-Photo-Gallery/Victoria-Memorial.htm', 'http://zeenews.india.com/news/sci-tech/victoria-memorial-museum-blackout-in-kolkata-for-earth-hour_1569445.html']
  #ALL_RESULTS=['http://en.wikipedia.org/wiki/Himalayas', 'http://en.wikipedia.org/wiki/Paro_Taktsang', 'http://en.wikipedia.org/wiki/List_of_Himalayan_peaks_and_passes', 'http://en.wikipedia.org/wiki/Indian_Himalayan_Region', 'http://en.wikipedia.org/wiki/Indian_Plate', 'http://simple.wikipedia.org/wiki/Himalayas', 'http://www.thehindu.com/sci-tech/energy-and-environment/emissions-from-biomass-burning-cross-the-himalayas/article7105899.ece', 'http://www.npr.org/blogs/goatsandsoda/2015/04/15/399579066/in-search-of-the-missing-trekkers-in-nepal-s-muddy-morass', 'http://www.nzherald.co.nz/bay-of-plenty-times/news/article.cfm?c_id=1503343&objectid=11434737', 'http://www.youtube.com/watch?v=HuSHOQ6gv5Y', 'http://www.britannica.com/EBchecked/topic/266037/Himalayas', 'http://www.english-online.at/geography/himalayas/himalaya-mountain-range.html', 'http://www.himalayanfootsteps.com/destinations/where-are-the-himalayas/', 'http://www.mountainprofessor.com/the-himalaya.html', 'http://www.himalaya2000.com/himalayan-facts/location-of-himalayas.html', 'http://www.unmuseum.org/yeti.htm', 'http://www.hitt-initiative.org/mla/?page_id=390', 'http://www.robinsonlibrary.com/geography/physical/mountains/himalaya.htm', 'http://geography.howstuffworks.com/asia/the-himalayas.htm', 'http://www.kidsdiscover.com/spotlight/himalayas-kids/', 'http://pubs.usgs.gov/gip/dynamic/himalaya.html', 'http://www.todayifoundout.com/index.php/2013/12/himalayas-formed/', 'http://www.pbs.org/wgbh/nova/everest/earth/birth.html', 'http://www.pbs.org/wnet/nature/the-himalayas-himalayas-facts/6341/', 'http://www.pbs.org/wnet/nature/the-himalayas-introduction/6338/', 'http://www.oddizzi.com/teachers/explore-the-world/physical-features/mountains/mountain-case-study/himalayas/', 'https://vimeo.com/121045965', 'http://www.worldwildlife.org/places/eastern-himalayas', 'http://www.answers.com/Q/What_are_the_Himalayas']

  print('YOUR TOP ANSWERS ARE:')
  c=0.0
  for res in ALL_RESULTS:
    Exact_Match_Found_flag=0
    try:
      timeout=0
      #print 'Checking Source:',res
      response = urllib.request.urlopen(res)
      page_data = response.read()
      page_data=BeautifulSoup(page_data)
      page_data=page_data.get_text()
      page_data=page_data.split('.')

      # Read from Individual Web Pages
      if answer_type=="Description":
        Start_T=time.time()
        for line in page_data:
          Curr_T=time.time()
          if(Curr_T-Start_T)>15.0:
            break
          if re.findall(query.lower(),line.lower())!=[]:
            c+=1.0
            line_low=line.lower()
            line=line_low.split(query.lower())
            print('===============================================================================')
            print('Answer ',c,':')
            line=query+line[1]+'.'
            print(line)
            print('\n\nSource: ',res)
            print('===============================================================================')
            Exact_Match_Found_flag=1
            break

      elif answer_type=="Location":
        query_parts=query.split(' ')
        Start_T=time.time()
        for line in page_data:
          Curr_T=time.time()
          if(Curr_T-Start_T)>30.0:
            break
          check_next=0
          for each_qp in query_parts:
            if re.findall(each_qp.lower(),line.lower())==[]:
              check_next=1
              break
          if check_next==1:
            continue
          else:
            line_parts=line.split(' ')
            for each_lp in line_parts:
              if (each_lp in query_parts) or (each_lp in IGNORE_LIST):  #Skip the Query Words
                continue
              if check_WordNet(word=each_lp,def_word='city') or check_WordNet(word=each_lp,def_word='country') or check_WordNet(word=each_lp,def_word='continent') or check_WordNet(word=each_lp,def_word='state'):
                c+=1.0
                print(each_lp)
                if  each_lp not in ALL_ANSWERS:
                  ALL_ANSWERS[each_lp]=1
                else:
                  ALL_ANSWERS[each_lp]+=1 
                Exact_Match_Found_flag=1
                break
            if Exact_Match_Found_flag:
              break

      #print 'Finished Checking Source:',res
    except :
      print()


  #Give a Probability for One Word Answers
  if answer_type=="Location":

    ALL_ANSWERS_SORTED=[]
    all_ans=list(ALL_ANSWERS.keys())
    for each_ans in all_ans:
      ALL_ANSWERS_SORTED.append([ALL_ANSWERS[each_ans],each_ans])

    ALL_ANSWERS_SORTED.sort()
    print('===============================================================================')
    print('SUMMARY:')
    print('---------------------------------------------------------------------------')
    for each_sa in range(0,len(ALL_ANSWERS_SORTED)):
      idx=len(ALL_ANSWERS_SORTED)-1-each_sa
      print(ALL_ANSWERS_SORTED[idx][1])
      print('Confidence Measure= ',(ALL_ANSWERS_SORTED[idx][0]/c*100.0),'%')
      print('---------------------------------------------------------------------------')
    print('===============================================================================')

# test the module
#Tell_Me_Alfred()
 
