import requests

url = "http://web1.ncaa.org/stats/StatsSrv/rankings"

def csv_dump(sport_code='MBB', academic_year='2015', rpt_weeks='141', div='1', stat_seq='-103'):
    """
    Starting point. Dumps an unparsed, messy csv. Most inputs are based on 
    arbitrary NCAA codes that users should not have to know (except for maybe 
    sportCode).
    
    :param sport_code:
        NCAA code for desired sport. Defaults to Men's Basketball.
    :param academic_year:
        Four digit academic year. Defaults to 2015.
    :param rpt_weeks:
        NCAA code for end week of returned stats. Defaults to last week of 2015.
    :param div:
        NCAA division. Defaults to 1.
    :param stat_seq:
        NCAA code for specific stats requested. Defaults to all team stats.
    """
    payload = { 'sportCode': sport_code,
                'academicYear': academic_year,
                'rptType': 'CSV',
                'rptWeeks': rpt_weeks,
                'div': div,
                'statSeq': stat_seq,
                'doWhat': 'showrankings'
                }
    r = requests.post(url, payload)
    with open("results.csv", "w") as f:
        f.write(r.content)