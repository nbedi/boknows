import os
import re
import requests
import pandas as pd
from datetime import date

import sys

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from functools import reduce
    from io import StringIO

url = 'http://web1.ncaa.org/stats/StatsSrv/rankings'

def get_ncaa_data(sport_code, div, stat_seq, academic_year='latest', rpt_weeks='latest'):
    """
    """
    payload = { 'sportCode': sport_code }
    latest = requests.post('http://web1.ncaa.org/stats/StatsSrv/rankings', payload)
    latest_date = latest.text.split('div'+div+'txt',1)[1].split('Through Games ',1)[1].split('\"',1)[0].replace('/','')
    
    path = 'dump/' + sport_code + '/div' + div
    
    if os.path.isfile(path+'/'+latest_date+'_'+stat_seq+'.csv'):
        return open(path+'/'+latest_date+'_'+stat_seq+'.csv').read()
    else:
        return csv_dump(sport_code=sport_code, div=div, stat_seq=stat_seq, academic_year=academic_year, rpt_weeks=rpt_weeks)
        

def csv_dump(dir_path='dump', sport_code='MBB', academic_year='latest', rpt_weeks='latest', div='1', stat_seq='team'):
    """
    Dumps a csv file according to inputs to specified path. Most inputs are based on 
    arbitrary NCAA codes that users should not have to know (except for maybe 
    sport_code).
    
    :param dir_path:
        Path to directory to dump CSV files in. Defaults to directory called 'dump'
    
    Other inputs documented in utils.ncaa_request.
    """
    csv_output = csv_cleanup(ncaa_request('CSV', sport_code, academic_year, rpt_weeks, div, stat_seq))
    
    path = dir_path + '/' + sport_code + '/div' + div
        
    if not os.path.exists(path):
        os.makedirs(path)
            
    with open(path+'/'+csv_output[0]+'_'+stat_seq+'.csv', 'w') as f:
        f.write(csv_output[1])
    
    return csv_output[1]

def csv_cleanup(content=None):
    """
    Cleans up the csv output from NCAA stats. Separates different tables into 
    individual strings. 
    
    Returns a tuple with filename and csv content.
    
    :param content:
        Original output from NCAA stats
    """
    files = {}
    csvs = []
    
    if content is None:
        return files
    
    filename = content.split('Through Games ',1)[1].split('\n',1)[0].replace('/','')
    
    key = ''
    for line in content.split('\n'):
        if 'Division' in line:
            key = re.sub(r'DivisionI*', '', line.replace(' ', ''))
            files[key] = ''
        if ',' in line:
            files[key] = files[key] + line + '\n'
            
    for value in files.values():
        csvs.append(pd.read_csv(StringIO(value)))
    
    merged = reduce(lambda left,right: pd.merge(left, right[right.columns.difference(left.columns.difference(['Name']))], on='Name'), csvs)
    return (filename, merged.drop('Rank', 1).to_csv())

def ncaa_request(rpt_type, sport_code, academic_year, rpt_weeks, div, stat_seq):
    """
    Makes request to NCAA web application at http://web1.ncaa.org/stats/StatsSrv/rankings?. 
    
    :param rpt_type:
        Format of response. Can be HTML, ASCII, PDF or CSV.
    :param sport_code:
        NCAA code for desired sport.
    :param academic_year:
        Numerical four digit academic year or 'latest'. Earliest input is 2002.
    :param rpt_weeks:
        Numerical NCAA code for end week of returned stats or 'latest'.
    :param div:
        NCAA division.
    :param stat_seq:
        NCAA code for specific stats requested. Generic terms 'team' and 'player' 
        will return all team or individual stats.
    """
    if academic_year == 'latest':
        academic_year = date.today().year + 1 if date.today().month > 9 else date.today().year
    
    if rpt_weeks == 'latest':
        weeks_payload = { 'sportCode': sport_code,
                          'academicYear': academic_year
                        }
        rw = requests.post('http://web1.ncaa.org/stats/StatsSrv/rankings', weeks_payload)
        rpt_weeks = rw.text.split('div'+div+'val',1)[1].split('\"',2)[1]
        
    stat_seq = '-101' if stat_seq == 'team' else '-103' if stat_seq == 'player' else stat_seq
    
    payload = { 'sportCode': sport_code,
                'academicYear': academic_year,
                'rptType': rpt_type,
                'rptWeeks': rpt_weeks,
                'div': div,
                'statSeq': stat_seq,
                'doWhat': 'showrankings'
                }
                
    r = requests.post(url, payload)
    return r.text
