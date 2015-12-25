import os
import re
import requests
import pandas as pd
from io import StringIO

url = 'http://web1.ncaa.org/stats/StatsSrv/rankings'

def csv_dump(dir_path='dump', sport_code='MBB', academic_year='2015', rpt_weeks='141', div='1', stat_seq='-101'):
    """
    Dumps a csv file according to inputs to specified path. Most inputs are based on 
    arbitrary NCAA codes that users should not have to know (except for maybe 
    sport_code).
    
    :param dir_path:
        Path to directory to dump CSV files in. Defaults to directory called 'dump'
    
    Other inputs documented in :method:`.ncaa_request`.
    """
    csv = csv_cleanup(ncaa_request('CSV', sport_code, academic_year, rpt_weeks, div, stat_seq))
    
    path = dir_path + '/' + sport_code + '/div' + div
        
    if not os.path.exists(path):
        os.makedirs(path)
            
    with open(path+'/'+academic_year+'.csv', 'w') as f:
        f.write(csv)

def csv_cleanup(content=None):
    """
    Cleans up the csv output from NCAA stats. Separates different tables into 
    individual strings. 
    
    Returns a dictionary with filenames as keys and csv strings as values.
    
    :param content:
        Original output from NCAA stats
    """
    files = {}
    csvs = []
    
    if content is None:
        return files
    
    key = ''
    for line in content.split('\n'):
        if 'Division' in line:
            key = re.sub(r'DivisionI*', '', line.replace(' ', ''))
            files[key] = ''
        if ',' in line:
            files[key] = files[key] + line + '\n'
            
    for value in files.values():
        csvs.append(pd.read_csv(StringIO(value.decode('utf-8'))))
    
    merged = reduce(lambda left,right: pd.merge(left, right[right.columns.difference(left.columns.difference(['Name']))], on='Name'), csvs)
    return merged.to_csv()

def ncaa_request(rpt_type, sport_code, academic_year, rpt_weeks, div, stat_seq):
    """
    Makes request to NCAA web application at http://web1.ncaa.org/stats/StatsSrv/rankings?. 
    
    :param rpt_type:
        Format of response. Can be HTML, ASCII, PDF or CSV.
    :param sport_code:
        NCAA code for desired sport.
    :param academic_year:
        Four digit academic year. Earliest input is 2002.
    :param rpt_weeks:
        NCAA code for end week of returned stats.
    :param div:
        NCAA division.
    :param stat_seq:
        NCAA code for specific stats requested.
    """
    payload = { 'sportCode': sport_code,
                'academicYear': academic_year,
                'rptType': rpt_type,
                'rptWeeks': rpt_weeks,
                'div': div,
                'statSeq': stat_seq,
                'doWhat': 'showrankings'
                }
                
    r = requests.post(url, payload)
    return r.content
    
