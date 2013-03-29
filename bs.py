# This program searches through the available top free agents in a fantrax
# fantasy hockey league. It then sorts those players based on fantasyhockeygeek.com
# rankings and displays them.

from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv

def enum(sequence, start=1):
    #variance of enumerate to start at 1
    for i, x in enumerate(sequence):
        yield i+start, x

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def get_free_agent(players_url):
    soup = make_soup(players_url)
    players = [a.string for a in soup.findAll("a", "hand")]
    
    #remove any blank values
    players = [x for x in players if x != None]
    
    #encode from uni to utf-8
    players = [item.encode('utf-8') for item in players]
    
    #reformat name from 'Last, First' to 'First Last'
    players = [" ".join(n.split(", ")[::-1]) for n in players]
    return players

def get_fhg(fhg):
    #open csv data from fhg
    with open(fhg, 'rb') as f:
        reader = [reader for reader in csv.reader(f)]
    return reader

def filter_fhg(fhg_csv):
    #get fhg stats from csv
    fhg_stats = get_fhg(fhg_csv)
    shrunklist = []
    
    #shrink fhg stats to top 250
    for row in range(1,251):
        shrunklist.append(fhg_stats[row])
        
    #remove the 1st, and 6th on fields
    for i in range(len(shrunklist)):
        del shrunklist[i][0]
        del shrunklist[i][4:]
        
    #convert field 3 to int for sorting
    for i in range(len(shrunklist)):
        shrunklist[i][3] = int(shrunklist[i][3])
    return shrunklist

def get_end_result(fantrax, fhg_stats):
    end_result = []
    
    #search through fhg for matching fantrax players
    for i in range(len(fantrax)):
        for x in range(len(fhg_stats)):
            if fantrax[i] in fhg_stats[x][0]:
                end_result.append(fhg_stats[x])
                
    #sort list of matches by field 3
    end_result.sort(key=lambda x: x[3], reverse=True)
    
    return end_result

if __name__ == '__main__':
    
     #location of free agents
     players_url = ("http://www6.fantrax.com/fantasy/statistics.go?leagueId=cj0e5gc5h8elfcx7"
                    "&isSubmit=y&sort=SCORE&sortScId=&sortScPosId=&reportGroupIndex=&aggregateInfoIndex="
                    "&previousSortOrderKey=SCORE%7C%7C&transactionPeriod=10&ov=false&prevPageNumber=1"
                    "&pageNumber=&maxResultsPerPage=250&hiddenTabCount=3&view=&seasonOrProjection=SEASON_30l"
                    "&timeframeType=YEAR_TO_DATE&period=10&timeStartType=PERIOD_ONLY&startDate=2013-01-19"
                    "&endDate=2013-03-28&positionOrGroup=HOCKEY_SKATING&statusOrTeamFilter=ALL_AVAILABLE"
                    "&displayType=TRACKED&miscDisplayType=ALL&searchName=")
     
     #location of fhg csv file
     fhg_csv = 'schmohawkey.csv'
     
     fantrax = get_free_agent(players_url)
     fhg_stats = filter_fhg(fhg_csv)

     end_results = get_end_result(fantrax, fhg_stats)

     #print list of matches
     for x in enum(end_results):
        print x

     #print results to text file
     f = open('./results.txt', 'w')
     for item in end_results:
         f.write("%s\n" % item)
     f.close()

     #operation is complete
     print "DONE"
