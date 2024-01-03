import re, random

DefaultUAWindows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
HeadersGet  = lambda i=DefaultUAWindows : {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Cache-Control':'max-age=0','Pragma':'akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-get-request-id,akamai-x-get-nonces,akamai-x-get-client-ip,akamai-x-feo-trace','Sec-Ch-Prefers-Color-Scheme':'light','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':i,'Viewport-Width':'924'}
HeadersPost = lambda i=DefaultUAWindows : {'Accept':'*/*','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.facebook.com','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':i}

def ConvertCookie(cok):
    try:
        sb     = re.search('sb=(.*?);',     str(cok)).group(1)
        datr   = re.search('datr=(.*?);',   str(cok)).group(1)
        c_user = re.search('c_user=(.*?);', str(cok)).group(1)
        xs     = re.search('xs=(.*?);',     str(cok)).group(1)
        fr     = re.search('fr=(.*?);',     str(cok)).group(1)
        cookie = f'sb={sb}; datr={datr}; c_user={c_user}; xs={xs}; fr={fr};'
    except Exception as e: cookie = cok
    return(cookie)

def LoginCookie(r, ua, cookie):
    try:
        req = r.get('https://www.facebook.com/profile.php', headers=HeadersGet(ua), cookies={'cookie':cookie}, allow_redirects=True).text
        id = re.search('"actorID":"(.*?)"',str(req)).group(1)
        nm = re.search('"NAME":"(.*?)"',str(req)).group(1)
        return(ConvertCookie(cookie))
    except Exception as e: return(False)

def LoginEmail(r, ua, email, password):
    try:
        Host = 'm.prod.facebook.com'
        HeadersGet = {'Host':Host,'Dpr':'1.25','Viewport-Width':'1000','Sec-Ch-Ua':'"Chromium";v="119", "Not?A_Brand";v="24"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'"Android"','Sec-Ch-Ua-Platform-Version':'','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Prefers-Color-Scheme':'dark','Upgrade-Insecure-Requests':'1','User-Agent':ua,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Sec-Fetch-Site':'none','Sec-Fetch-Mode':'navigate','Sec-Fetch-User':'?1','Sec-Fetch-Dest':'document','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Priority':'u=0, i',}
        Url = f'https://{Host}/login.php?'
        Req = r.get(Url,headers=HeadersGet,allow_redirects=True).text
        Data = {'m_ts':re.search('name="m_ts" value="(.*?)"',str(Req)).group(1),'li':re.search('name="li" value="(.*?)"',str(Req)).group(1),'try_number':re.search('name="try_number" value="(.*?)"',str(Req)).group(1),'unrecognized_tries':re.search('name="unrecognized_tries" value="(.*?)"',str(Req)).group(1),'email':email,'prefill_contact_point':email,'prefill_source':'browser_dropdown','prefill_type':'contact_point','first_prefill_source':'browser_dropdown','first_prefill_type':'contact_point','had_cp_prefilled':True,'had_password_prefilled':False,'is_smart_lock':False,'bi_xrwh':re.search('name="bi_xrwh" value="(.*?)"',str(Req)).group(1),'bi_wvdp':'{"hwc":true,"hwcr":false,"has_dnt":true,"has_standalone":false,"wnd_toStr_toStr":"function toString() { [native code] }","hasPerm":false,"has_seWo":true,"has_meDe":true,"has_creds":true,"has_hwi_bt":false,"has_agjsi":false,"iframeProto":"function get contentWindow() { [native code] }","remap":false,"iframeData":{"hwc":true,"hwcr":false,"has_dnt":true,"has_standalone":false,"wnd_toStr_toStr":"function toString() { [native code] }","hasPerm":false,"has_seWo":true,"has_meDe":true,"has_creds":true,"has_hwi_bt":false,"has_agjsi":false}}','pass':password,'fb_dtsg':re.search('{"dtsg":{"token":"(.*?)"',str(Req)).group(1),'jazoest':re.search('name="jazoest" value="(.*?)"',str(Req)).group(1),'lsd':re.search('name="lsd" value="(.*?)"',str(Req)).group(1),'__dyn':'','__csr':'','__req':str(random.randrange(1,6)),'__a':re.search('"encrypted":"(.*?)"',str(Req)).group(1),'__user':'0'}
        Cookie = '; '.join([str(x)+"="+str(y) for x,y in r.cookies.get_dict().items()]) + f'; dpr=4; locale=id_ID; m_pixel_ratio=4; wd=360x800;'
        HeadersPost = {'Host':Host,'Cookie':Cookie,'Content-Length':'2000','Cache-Control':'max-age=0','Dpr':'1.25','Viewport-Width':'1000','Sec-Ch-Ua':'"Chromium";v="119", "Not?A_Brand";v="24"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'"Android"','Sec-Ch-Ua-Platform-Version':'','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Prefers-Color-Scheme':'dark','Upgrade-Insecure-Requests':'1','Origin':f'https://{Host}','Content-Type':'application/x-www-form-urlencoded','User-Agent':ua,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'navigate','Sec-Fetch-User':'?1','Sec-Fetch-Dest':'document','Referer':Url,'Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Priority':'u=0, i'}
        Next = 'https://%s%s'%(Host,re.search('ajaxURI:"(.*?)"',str(Req)).group(1))
        Pos = r.post(Next,data=Data,headers=HeadersPost,cookies={'cookie':Cookie},allow_redirects=True)
        Cookie = '; '.join([str(x)+"="+str(y) for x,y in r.cookies.get_dict().items()]) + f'; dpr=4; locale=id_ID; m_pixel_ratio=4; wd=360x800;'
        if 'c_user' in str(Cookie): return(ConvertCookie(Cookie))
        else: return(False)
    except Exception as e: return(False)

def LoginPhone(r, ua, phone, password):
    try:
        Host = 'm.prod.facebook.com'
        HeadersGet = {'Host':Host,'Dpr':'1.25','Viewport-Width':'1000','Sec-Ch-Ua':'"Chromium";v="119", "Not?A_Brand";v="24"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'"Android"','Sec-Ch-Ua-Platform-Version':'','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Prefers-Color-Scheme':'dark','Upgrade-Insecure-Requests':'1','User-Agent':ua,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Sec-Fetch-Site':'none','Sec-Fetch-Mode':'navigate','Sec-Fetch-User':'?1','Sec-Fetch-Dest':'document','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Priority':'u=0, i',}
        Url = f'https://{Host}/login.php?'
        Req = r.get(Url,headers=HeadersGet,allow_redirects=True).text
        Data = {'m_ts':re.search('name="m_ts" value="(.*?)"',str(Req)).group(1),'li':re.search('name="li" value="(.*?)"',str(Req)).group(1),'try_number':re.search('name="try_number" value="(.*?)"',str(Req)).group(1),'unrecognized_tries':re.search('name="unrecognized_tries" value="(.*?)"',str(Req)).group(1),'email':phone,'prefill_contact_point':phone,'prefill_source':'browser_dropdown','prefill_type':'contact_point','first_prefill_source':'browser_dropdown','first_prefill_type':'contact_point','had_cp_prefilled':True,'had_password_prefilled':False,'is_smart_lock':False,'bi_xrwh':re.search('name="bi_xrwh" value="(.*?)"',str(Req)).group(1),'bi_wvdp':'{"hwc":true,"hwcr":false,"has_dnt":true,"has_standalone":false,"wnd_toStr_toStr":"function toString() { [native code] }","hasPerm":false,"has_seWo":true,"has_meDe":true,"has_creds":true,"has_hwi_bt":false,"has_agjsi":false,"iframeProto":"function get contentWindow() { [native code] }","remap":false,"iframeData":{"hwc":true,"hwcr":false,"has_dnt":true,"has_standalone":false,"wnd_toStr_toStr":"function toString() { [native code] }","hasPerm":false,"has_seWo":true,"has_meDe":true,"has_creds":true,"has_hwi_bt":false,"has_agjsi":false}}','pass':password,'fb_dtsg':re.search('{"dtsg":{"token":"(.*?)"',str(Req)).group(1),'jazoest':re.search('name="jazoest" value="(.*?)"',str(Req)).group(1),'lsd':re.search('name="lsd" value="(.*?)"',str(Req)).group(1),'__dyn':'','__csr':'','__req':str(random.randrange(1,6)),'__a':re.search('"encrypted":"(.*?)"',str(Req)).group(1),'__user':'0'}
        Cookie = '; '.join([str(x)+"="+str(y) for x,y in r.cookies.get_dict().items()]) + f'; dpr=4; locale=id_ID; m_pixel_ratio=4; wd=360x800;'
        HeadersPost = {'Host':Host,'Cookie':Cookie,'Content-Length':'2000','Cache-Control':'max-age=0','Dpr':'1.25','Viewport-Width':'1000','Sec-Ch-Ua':'"Chromium";v="119", "Not?A_Brand";v="24"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'"Android"','Sec-Ch-Ua-Platform-Version':'','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Prefers-Color-Scheme':'dark','Upgrade-Insecure-Requests':'1','Origin':f'https://{Host}','Content-Type':'application/x-www-form-urlencoded','User-Agent':ua,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'navigate','Sec-Fetch-User':'?1','Sec-Fetch-Dest':'document','Referer':Url,'Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Priority':'u=0, i'}
        Next = 'https://%s%s'%(Host,re.search('ajaxURI:"(.*?)"',str(Req)).group(1))
        Pos = r.post(Next,data=Data,headers=HeadersPost,cookies={'cookie':Cookie},allow_redirects=True)
        Cookie = '; '.join([str(x)+"="+str(y) for x,y in r.cookies.get_dict().items()]) + f'; dpr=4; locale=id_ID; m_pixel_ratio=4; wd=360x800;'
        if 'c_user' in str(Cookie): return(ConvertCookie(Cookie))
        else: return(False)
    except Exception as e: return(False)