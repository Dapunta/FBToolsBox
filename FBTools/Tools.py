import re, random

def ConvertURL(i):
    if 'http' in str(i):
        if   'www.facebook.com'    in str(i): url = i
        elif 'm.facebook.com'      in str(i): url = i.replace('m.facebook.com','www.facebook.com')
        elif 'mbasic.facebook.com' in str(i): url = i.replace('mbasic.facebook.com','www.facebook.com')
        elif 'web.facebook.com'    in str(i): url = i.replace('web.facebook.com','www.facebook.com')
    else:
        if   'www.facebook.com'    in str(i): url = 'https://' + i
        elif 'm.facebook.com'      in str(i): url = 'https://' + i.replace('m.facebook.com','www.facebook.com')
        elif 'mbasic.facebook.com' in str(i): url = 'https://' + i.replace('mbasic.facebook.com','www.facebook.com')
        elif 'web.facebook.com'    in str(i): url = 'https://' + i.replace('web.facebook.com','www.facebook.com')
        else:
            if 'facebook.com' in str(i).lower(): url = 'https://www.facebook.com' + i.replace('facebook.com','').replace('Facebook.com','')
            else: url = 'https://www.facebook.com/%s'%(i)
    return(url)

def GetData(req):
    try:
        av = re.search(r'"actorID":"(.*?)"',str(req)).group(1)
        __user = av
        __a = str(random.randrange(1,6))
        __hs = re.search(r'"haste_session":"(.*?)"',str(req)).group(1)
        __ccg = re.search(r'"connectionClass":"(.*?)"',str(req)).group(1)
        __rev = re.search(r'"__spin_r":(.*?),',str(req)).group(1)
        __spin_r = __rev
        __spin_b = re.search(r'"__spin_b":"(.*?)"',str(req)).group(1)
        __spin_t = re.search(r'"__spin_t":(.*?),',str(req)).group(1)
        __hsi = re.search(r'"hsi":"(.*?)"',str(req)).group(1)
        fb_dtsg = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"}',str(req)).group(1)
        jazoest = re.search(r'jazoest=(.*?)"',str(req)).group(1)
        lsd = re.search(r'"LSD",\[\],{"token":"(.*?)"}',str(req)).group(1)
        Data = {'av':av,'__user':__user,'__a':__a,'__hs':__hs,'dpr':'1.5','__ccg':__ccg,'__rev':__rev,'__spin_r':__spin_r,'__spin_b':__spin_b,'__spin_t':__spin_t,'__hsi':__hsi,'__comet_req':'15','fb_dtsg':fb_dtsg,'jazoest':jazoest,'lsd':lsd}
        return(Data)
    except Exception as e: return({})