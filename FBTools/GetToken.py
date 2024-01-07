import re

def TokenEAAG(r, cookie):
    try:
        url = 'https://business.facebook.com/business_locations'
        req = r.get(url,cookies={'cookie':cookie})
        tok = re.search(r'(\["EAAG\w+)', req.text).group(1).replace('["','')
        return(tok)
    except Exception as e: return('Token Invalid !')

def TokenEAAB(r, cookie):
    try:
        req1 = r.get('https://www.facebook.com/adsmanager/manage/campaigns',cookies={'cookie':cookie},allow_redirects=True).text
        nek1 = re.search(r'window.location.replace\("(.*?)"\)',str(req1)).group(1).replace('\\','')
        req2 = r.get(nek1,cookies={'cookie':cookie},allow_redirects=True).text
        tok  = re.search(r'accessToken="(.*?)"',str(req2)).group(1)
        return(tok)
    except Exception as e: return('Token Invalid !')

def TokenEAAD(r, cookie):
    try:
        url = 'https://www.facebook.com/events_manager2/overview'
        req = r.get(url,cookies={'cookie':cookie})
        tok = re.search(r'{"accessToken":"(EAAd\w+)',req.text).group(1)
        return(tok)
    except Exception as e: return('Token Invalid !')

def TokenEAAC(r, cookie):
    try:
        url = 'https://www.facebook.com/brand_safety/controls'
        req = r.get(url,cookies={'cookie':cookie})
        tok = re.search(r'{"accessToken":"(EAAC\w+)',req.text).group(1)
        return(tok)
    except Exception as e: return('Token Invalid !')

def TokenEAAF(r, cookie):
    try:
        url = 'https://www.facebook.com/test-and-learn/test'
        req = r.get(url,cookies={'cookie':cookie})
        tok = re.search(r'{"accessToken":"(EAAF\w+)',req.text).group(1)
        return(tok)
    except Exception as e: return('Token Invalid !')

def TokenEABB(r, cookie):
    try:
        url = 'https://www.facebook.com/ads/adbuilder/home'
        req = r.get(url,cookies={'cookie':cookie})
        tok = re.search(r'"accessToken":"(EABB\w+)',req.text).group(1)
        return(tok)
    except Exception as e: return('Token Invalid !')