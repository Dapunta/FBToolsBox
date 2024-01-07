import re, pyotp, time, json, datetime, uuid
from .Tools import GetData
from .GetToken import TokenEAAG

DefaultUAWindows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
HeadersGet  = lambda i=DefaultUAWindows : {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Cache-Control':'max-age=0','Pragma':'akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-get-request-id,akamai-x-get-nonces,akamai-x-get-client-ip,akamai-x-feo-trace','Sec-Ch-Prefers-Color-Scheme':'light','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':i,'Viewport-Width':'924'}
HeadersPost = lambda i=DefaultUAWindows : {'Accept':'*/*','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.facebook.com','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':i}

class A2F():

    def __init__(self, r=False, cookie=False, stat=None, password=None):
        self.r = r
        self.cookie = cookie
        self.stat = stat
        self.password = password
        self.req = self.r.get('https://www.facebook.com/', headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        self.Data = GetData(self.req)

    def Auten(self):
        if self.stat == True or self.stat == 1:
            x1 = self.Post0('https://www.facebook.com/security/2fac/setup/qrcode/generate/')
            if 'Diperlukan Konfirmasi' in str(x1): x1 = self.Post1('https://www.facebook.com/security/2fac/setup/qrcode/generate/')
            if 'Diperlukan Konfirmasi' in str(x1): return({'status':'failed','key':None,'recovery':None,'message':'Wrong Password'})
            else:
                limit = 0
                while ('serialized_data' not in str(x1)):
                    if limit == 10: break
                    else:
                        x1 = self.Post0('https://www.facebook.com/security/2fac/setup/qrcode/generate/')
                        limit += 1
            if (limit == 10) and ('serialized_data' not in str(x1)):
                return({'status':'failed','key':None,'recovery':None,'message':'Account Spam'})
            elif 'serialized_data' in str(x1):
                next = 'https://www.facebook.com' + re.search(r'"redirect":"(.*?)"',str(x1)).group(1)
                pos1 = self.Post1(next)
                key = {
                    'code':re.search(r'"code":"(.*?)"',str(pos1)).group(1).replace(' ',''),
                    'qr':re.search(r'"src":"(.*?)"',str(pos1)).group(1)}
                code = pyotp.TOTP(key['code']).now()
                final = self.Pasang(code)
                if '"/security/2fac/setup/outro/"' in str(final) or '"/security/2fac/settings/"' in str(final): return({'status':'success','key':key['code'],'recovery':self.Recovery(),'message':None})
                else: return({'status':'failed','key':None,'recovery':None,'message':'Failed To Change Authentication'})
            else: return({'status':'failed','key':None,'recovery':None,'message':'Unknown Error'})

    def Post0(self, url):
        pos = self.r.post(url, data=self.Data, headers=HeadersPost(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        return(pos)

    def Post1(self, url):
        Data = self.Data.copy()
        Data.update({'__asyncDialog':1,'ajax_password':self.password,'confirmed':1})
        pos = self.r.post(url, data=Data, headers=HeadersPost(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        return(pos)

    def Pasang(self, code):
        Data = self.Data.copy()
        Data.update({'code':code,'dialog_loaded':True})
        pos = self.r.post('https://www.facebook.com/security/2fac/setup/verify_code/', data=Data, headers=HeadersPost(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        return(pos)

    def Recovery(self):
        try:
            Data = self.Data.copy()
            Data.update({'reset':True})
            pos = self.r.post('https://www.facebook.com/security/2fac/factors/recovery-code/', data=Data, headers=HeadersPost(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
            return(re.findall(r'"value":"(.*?)"',str(pos)))
        except Exception as e: return([])

class UnA2F():

    def __init__(self, r=False, cookie=False, stat=None, password=None):
        self.r = r
        self.cookie = cookie
        self.stat = stat
        self.password = password
        self.req = self.r.get('https://www.facebook.com/', headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        self.Data = GetData(self.req)

    def UnAuten(self):
        try:
            if self.stat == False or self.stat == 0:
                Data = self.Data.copy()
                Data.update({'next':'https://www.facebook.com/security/2fac/settings/','encpass':'#PWD_BROWSER:0:%s:%s'%(str(time.time()),str(self.password))})
                pos1 = self.r.post('https://www.facebook.com/login/reauth.php', data=Data, headers=HeadersPost(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
                pos2 = self.r.post('https://www.facebook.com/security/2fac/setup/turn_off/', data=self.Data, headers=HeadersPost(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
                if 'REMOVEMETHOD' in str(pos2):
                    nek = 'https://www.facebook.com' + re.search(r'"action":"(.*?)"',str(pos2)).group(1)
                    pos3 = self.r.post(nek, data=self.Data, headers=HeadersPost(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
                    if 'onTwoFactorSetupChange' in str(pos3) and 'redirectPageTo' in str(pos3): tur = {'status':'success','key':None,'recovery':None,'message':None}
                    else: tur = {'status':'failed','key':None,'recovery':None,'message':'Failed To Remove 2FA'}
                else: tur = {'status':'failed','key':None,'recovery':None,'message':'Wrong Password'}
        except Exception as e: tur = {'status':'failed','key':None,'recovery':None,'message':'Error, Something Went Wrong'}
        return(tur)

class GetAPP():

    def __init__(self, r=False, cookie=False):
        self.ActiveApps, self.ExpiredApps = [], []
        self.r = r
        self.cookie = cookie
        self.req = self.r.get('https://www.facebook.com/', headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        self.Data = GetData(self.req)
        self.Data.update({'fb_api_caller_class':'RelayModern','server_timestamps':True})

    def Execute(self):
        self.CheckAPP(1)
        self.CheckAPP(2)
        return({'active':self.ActiveApps,'expired':self.ExpiredApps})

    def CheckAPP(self,stat):
        if stat == 1:
            Data = self.Data.copy()
            node = 'activeApps'
            Data.update({'fb_api_req_friendly_name':'ApplicationAndWebsitePaginatedSettingAppGridListActiveQuery','doc_id':'4711129059016316'})
            self.CheckLoop(Data,node,stat,None)
        elif stat == 2:
            Data = self.Data.copy()
            node = 'expiredApps'
            Data.update({'fb_api_req_friendly_name':'ApplicationAndWebsitePaginatedSettingAppGridListExpiredQuery','doc_id':'4802508009803010'})
            self.CheckLoop(Data,node,stat,None)

    def CheckLoop(self,dta,node,stat,cursor):
        try:
            dta.update({'variables':json.dumps({"after":cursor,"first":6,"id":dta['__user']})})
            pos = self.r.post('https://www.facebook.com/api/graphql/',data=dta,headers=HeadersPost(),cookies={'cookie':self.cookie}).json()
            dat = pos['data']['node'][node]['edges']
            for x in dat:
                try:
                    dtk = x['node']['apps_and_websites_view']['detailView']
                    id, nm, st, wk = dtk['app_id'], dtk['app_name'], dtk['app_status'], dtk['install_timestamp']
                    tm = datetime.datetime.utcfromtimestamp(int(wk))
                    tgl, bln, thn = tm.day, ['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember'][int(tm.month)-1], tm.year
                    tdt = '%s %s %s'%(tgl,bln,thn)
                    # print('%s%s| %s%s| %s'%(id,' '*(17-len(str(id))),nm[:14],' '*(15-len(str(nm[:14]))),tdt))
                    fm = {'id':id,'name':nm,'date':tdt}
                    if stat == 1: self.ActiveApps.append(fm)
                    elif stat == 2: self.ExpiredApps.append(fm)
                except Exception as e: continue
            try:
                next = pos['data']['node'][node]['page_info']['has_next_page']
                if next == True:
                    cursor = pos['data']['node'][node]['page_info']['end_cursor']
                    self.CheckLoop(dta,node,stat,cursor)
                else: pass
            except Exception as e: pass
        except Exception as e: pass

class ProfileGuard():

    def __init__(self, r=False, cookie=False, stat=True):
        self.r = r
        self.cookie = cookie
        self.token = TokenEAAG(self.r, self.cookie)
        self.stat = stat

    def Execute(self):
        try:
            id = re.search('c_user=(.*?);',str(self.cookie)).group(1)
            Var = {'0':{'is_shielded':self.stat,'session_id':str(uuid.uuid4()),'actor_id':id,'client_mutation_id':str(uuid.uuid4())}}
            Data = {'variables':json.dumps(Var),'doc_id':'1477043292367183','query_name':'IsShieldedSetMutation','strip_defaults':True,'strip_nulls':True,'locale':'en_US','client_country_code':'US','server_timestamps':True,'fb_api_req_friendly_name':'IsShieldedSetMutation','fb_api_caller_class':'IsShieldedSetMutation'}
            hdp = HeadersPost().copy()
            hdp.update({'Authorization' : 'OAuth %s'%(self.token)})
            pos = self.r.post('https://graph.facebook.com/graphql',data=Data,headers=hdp,cookies={'cookie':self.cookie}).text
            if '"is_shielded":true' in str(pos): tur = {'status':'active','message':None}
            elif '"is_shielded":false' in str(pos): tur = {'status':'inactive','message':None}
            else: tur = {'status':'failed','message':'Token EAAG Invalid, Please Remove Your 2FA'}
        except Exception as e: tur = {'status':'failed','message':'Error, Something Went Wrong'}
        return(tur)