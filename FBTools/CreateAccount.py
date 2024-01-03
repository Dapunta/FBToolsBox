import requests, re, time, random
import io, struct, base64, Crypto, binascii

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto import Random as RDM
from Crypto.Random import get_random_bytes
from nacl.public import PublicKey as PK
from nacl.public import SealedBox as SB

Author = 'Dapunta Khurayra X'
DefaultUA = 'Mozilla/5.0 (Linux; Android 13; SM-A055F Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.67 Mobile Safari/537.36'
HeadersGet = lambda i=DefaultUA : {'Host':'m.facebook.com','Cache-Control':'max-age=0','Upgrade-Insecure-Requests':'1','User-Agent':i,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Sec-Fetch-Site':'none','Sec-Fetch-Mode':'navigate','Sec-Fetch-User':'?1','Sec-Fetch-Dest':'document','Dpr':'1.25','Viewport-Width':'270','Sec-Ch-Ua':'','Sec-Ch-Ua-Mobile':'?1','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Prefers-Color-Scheme':'dark','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Priority':'u=0, i'}
HeadersPost = lambda i=DefaultUA : {'Host':'m.facebook.com','Content-Length':'480','Sec-Ch-Ua':'','Sec-Ch-Ua-Mobile':'?1','User-Agent':i,'Viewport-Width':'360','Content-Type':'application/x-www-form-urlencoded','Sec-Ch-Ua-Platform-Version':'','X-Asbd-Id':'129477','Dpr':'1.25','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Model':'','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua-Platform':'','Accept':'*/*','Origin':'https://m.facebook.com','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'cors','Sec-Fetch-Dest':'empty','Referer':'https://m.facebook.com/reg','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Priority':'u=1, i'}

class CreateAccount():

    def __init__(self):
        self.r = requests.Session()

    def SetData(self, name=False, password=False, birthday=False, email=False, phone=False, gender=0):
        if name!=False: self.name = name
        else: print("Parameter 'name' Not Found!")
        if password!=False: self.password = password
        else: print("Parameter 'password' Not Found!")
        if birthday!=False: self.birthday = birthday
        else: print("Parameter 'birthday' Not Found!")
        if email==False and phone==False: print("Parameter 'email' Or 'phone' Not Found!")
        else:
            if email!=False: self.email = email
            elif phone!=False: self.email = phone
        if gender==0: self.gender = '1'
        elif gender==1: self.gender = '2'
        else: print("Parameter 'gender' Not Found!")

    def Create(self):
        url = 'https://m.facebook.com/reg?refsrc=deprecated&rtime=%s&hrc=1&soft=hjk'%(str(time.time()))
        req = self.r.get(url, headers=HeadersGet(), allow_redirects=True).text
        FixData = {
            'fb_dtsg':re.search('"dtsg":{"token":"(.*?)"',str(req)).group(1),
            'jazoest':re.search('name="jazoest" value="(.*?)"',str(req)).group(1),
            'lsd':re.search('name="lsd" value="(.*?)"',str(req)).group(1),
            '__dyn':'',
            '__csr':'',
            '__req':str(random.randrange(1,7)),
            '__a':'',
            '__user':'0'}
        self.Step1(FixData)
        self.Step2(FixData)
        self.Step3(FixData)
        self.Step4(FixData)
        self.Step5(FixData)
        self.FinalStep1(req)

    def Step1(self, FixData): #--> Input Name
        Data = FixData.copy()
        Data.update({
            'firstname':self.name,
            'welcome_step_completed':True,
            'current_step_number':'0'})
        cok = '; '.join(['%s=%s'%(key,value) for key,value in self.r.cookies.get_dict().items()]) + '; m_pixel_ratio=1.25; wd=360x780;'
        pos = self.r.post('https://m.facebook.com/register/persist/', data=Data, headers=HeadersPost(), cookies={'cookie':cok}, allow_redirects=True).text

    def Step2(self, FixData): #--> Input Birthdate
        Data = FixData.copy()
        Data.update({
            'birthday_day':self.birthday.split('/')[0],
            'birthday_month':self.birthday.split('/')[1],
            'birthday_year':self.birthday.split('/')[2],
            'firstname':self.name,
            'did_use_age':False,
            'welcome_step_completed':True,
            'current_step_number':'1'})
        cok = '; '.join(['%s=%s'%(key,value) for key,value in self.r.cookies.get_dict().items()]) + '; m_pixel_ratio=1.25; wd=360x780;'
        pos = self.r.post('https://m.facebook.com/register/persist/', data=Data, headers=HeadersPost(), cookies={'cookie':cok}, allow_redirects=True).text

    def Step3(self, FixData): #--> Input Email Or Phone
        Data = FixData.copy()
        Data.update({
            'birthday_day':self.birthday.split('/')[0],
            'birthday_month':self.birthday.split('/')[1],
            'birthday_year':self.birthday.split('/')[2],
            'reg_email__':self.email,
            'firstname':self.name,
            'did_use_age':False,
            'welcome_step_completed':True,
            'current_step_number':'2'})
        cok = '; '.join(['%s=%s'%(key,value) for key,value in self.r.cookies.get_dict().items()]) + '; m_pixel_ratio=1.25; wd=360x780;'
        pos = self.r.post('https://m.facebook.com/register/persist/', data=Data, headers=HeadersPost(), cookies={'cookie':cok}, allow_redirects=True).text

    def Step4(self, FixData): #--> Input Gender
        Data = FixData.copy()
        Data.update({
            'birthday_day':self.birthday.split('/')[0],
            'birthday_month':self.birthday.split('/')[1],
            'birthday_year':self.birthday.split('/')[2],
            'sex':self.gender,
            'reg_email__':self.email,
            'firstname':self.name,
            'use_custom_gender':False,
            'did_use_age':False,
            'welcome_step_completed':True,
            'current_step_number':'3'})
        cok = '; '.join(['%s=%s'%(key,value) for key,value in self.r.cookies.get_dict().items()]) + '; m_pixel_ratio=1.25; wd=360x780;'
        pos = self.r.post('https://m.facebook.com/register/persist/', data=Data, headers=HeadersPost(), cookies={'cookie':cok}, allow_redirects=True).text
    
    def Step5(self, FixData): #--> Input Password
        Data = FixData.copy()
        Data.update({
            'birthday_day':self.birthday.split('/')[0],
            'birthday_month':self.birthday.split('/')[1],
            'birthday_year':self.birthday.split('/')[2],
            'sex':self.gender,
            'reg_email__':self.email,
            'firstname':self.name,
            'use_custom_gender':False,
            'did_use_age':False,
            'welcome_step_completed':True,
            'current_step_number':'3'})
        cok = '; '.join(['%s=%s'%(key,value) for key,value in self.r.cookies.get_dict().items()]) + '; m_pixel_ratio=1.25; wd=360x780;'
        pos = self.r.post('https://m.facebook.com/register/persist/', data=Data, headers=HeadersPost(), cookies={'cookie':cok}, allow_redirects=True).text

    def GenerateEncpass(self, req):
        tim, pbl, pbk = re.search('"__spin_t":(.*?),',str(req)).group(1), re.search('publicKey:"(.*?)",',str(req)).group(1), re.search('keyId:([0-9]+)',str(req)).group(1)
        rdb = RDM.get_random_bytes((len(Author)-2)*2); dpt = AES.new(rdb, AES.MODE_GCM, nonce=bytes([0]*(len(Author)-6)), mac_len=len(Author)-2); dpt.update(str(tim).encode("utf-8"))
        epw, ctg = dpt.encrypt_and_digest(self.password.encode("utf-8")); sld = SB(PK(binascii.unhexlify(str(pbl)))).encrypt(rdb)
        ecp = base64.b64encode(bytes([1,int(pbk),*list(struct.pack('<h', len(sld))),*list(sld),*list(ctg),*list(epw)])).decode("utf-8")
        Enc = '#PWD_BROWSER:%s:%s:%s'%(str(len(Author)-13),tim,str(ecp))
        return(Enc)

    def FinalStep1(self, req):
        encpass = self.GenerateEncpass(req)
        Data = {
            'ccp':re.search('name="ccp" value="(.*?)"',str(req)).group(1),
            'reg_instance':re.search('name="reg_instance" value="(.*?)"',str(req)).group(1),
            'submission_request':True,
            'helper':'',
            'reg_impression_id':re.search('name="reg_impression_id" value="(.*?)"',str(req)).group(1),
            'ns':'1',
            'zero_header_af_client':'',
            'app_id':'',
            'logger_id':re.search('name="logger_id" value="(.*?)"',str(req)).group(1),
            'field_names[0]':'firstname',
            'firstname':self.name,
            'field_names[1]':'birthday_wrapper',
            'birthday_day':self.birthday.split('/')[0],
            'birthday_month':self.birthday.split('/')[1],
            'birthday_year':self.birthday.split('/')[2],
            'age_step_input':'',
            'did_use_age':False,
            'field_names[2]':'reg_email__',
            'reg_email__':self.email,
            'field_names[3]':'sex',
            'sex':self.gender,
            'preferred_pronoun':'',
            'custom_gender':'',
            'field_names[4]':'reg_passwd__',
            'name_suggest_elig':False,
            'was_shown_name_suggestions':False,
            'did_use_suggested_name':False,
            'use_custom_gender':False,
            'guid':'',
            'pre_form_step':'',
            'encpass':encpass,
            'submit':'Sign Up',
            'fb_dtsg':re.search('"dtsg":{"token":"(.*?)"',str(req)).group(1),
            'jazoest':re.search('name="jazoest" value="(.*?)"',str(req)).group(1),
            'lsd':re.search('name="lsd" value="(.*?)"',str(req)).group(1),
            '__dyn':'',
            '__csr':'',
            '__req':str(random.randrange(1,7)),
            '__a':'',
            '__user':'0'}
        nek = 'https://m.facebook.com' + re.search('form method="post" action="(.*?)"',str(req)).group(1)
        cok = '; '.join(['%s=%s'%(key,value) for key,value in self.r.cookies.get_dict().items()]) + '; m_pixel_ratio=1.25; wd=360x780;'
        pos = self.r.post(nek, data=Data, headers=HeadersPost(), cookies={'cookie':cok}, allow_redirects=True).text
        cok = '; '.join(['%s=%s'%(key,value) for key,value in self.r.cookies.get_dict().items()]) + '; m_pixel_ratio=1.25; wd=360x780;'
        print(cok)