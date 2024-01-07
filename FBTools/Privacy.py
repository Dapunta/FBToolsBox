import re, json
from .Tools import ConvertURL, GetData

DefaultUAWindows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
HeadersGet  = lambda i=DefaultUAWindows : {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Cache-Control':'max-age=0','Pragma':'akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-get-request-id,akamai-x-get-nonces,akamai-x-get-client-ip,akamai-x-feo-trace','Sec-Ch-Prefers-Color-Scheme':'light','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':i,'Viewport-Width':'924'}
HeadersPost = lambda i=DefaultUAWindows : {'Accept':'*/*','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.facebook.com','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':i}

class PostPrivacy():

    def __init__(self, r=False, cookie=False, post=None, privacy=None):

        self.r = r
        self.cookie = cookie
        self.url = ConvertURL(post)
        try: self.req = self.r.get(self.url, headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        except Exception as e: self.req = None
        self.Data = GetData(self.req)

        if   privacy == 1: self.privacy = 'EVERYONE'
        elif privacy == 2: self.privacy = 'FRIENDS'
        else:              self.privacy = 'SELF'

    def Execute(self):
        try:
            privacy_write_id = re.search(r'"privacy_write_id":"(.*?)"',str(self.req)).group(1)
            post_id = re.search(r'"post_id":"(.*?)"',str(self.req)).group(1)
            Var = {"input":{"privacy_mutation_token":None,"privacy_row_input":{"allow":[],"base_state":self.privacy,"deny":[],"tag_expansion_state":"UNSPECIFIED"},"privacy_write_id":privacy_write_id,"render_location":"COMET_STORY_MENU","actor_id":self.Data['__user'],"client_mutation_id":"1"},"privacySelectorRenderLocation":"COMET_STORY_MENU","scale":2,"storyRenderLocation":"timeline","tags":None}
            self.Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'CometPrivacySelectorSavePrivacyMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id': '6846271792123707'})
            pos = self.r.post('https://web.facebook.com/api/graphql/', data=self.Data, cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
            if '"selected_option":{"privacy_row_input":{"allow":[],"base_state":"%s","deny":[],"privacy_targeting"'%(self.privacy) in str(pos): return({'status':'success','id':post_id,'privacy':self.privacy,'message':None})
            else: return({'status':'failed','id':post_id,'privacy':None,'message':'Spam Or Something'})
        except Exception as e: return({'status':'failed','id':None,'privacy':None,'message':'Something Went Wrong'})

class PhotoPrivacy():

    def __init__(self, r=False, cookie=False, photo=None, privacy=None):

        self.r = r
        self.cookie = cookie
        self.url = ConvertURL(photo)
        try: self.req = self.r.get(self.url, headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        except Exception as e: self.req = None
        self.Data = GetData(self.req)

        if   privacy == 1: self.privacy = 'EVERYONE'
        elif privacy == 2: self.privacy = 'FRIENDS'
        else:              self.privacy = 'SELF'

    def Execute(self):
        try:
            privacy_write_id = re.search(r'"privacy_write_id":"(.*?)"',str(self.req)).group(1)
            photo_id = re.search(r'"photo_id":"(.*?)"',str(self.req)).group(1)
            Var = {"input":{"privacy_mutation_token":None,"privacy_row_input":{"allow":[],"base_state":self.privacy,"deny":[],"tag_expansion_state":"UNSPECIFIED"},"privacy_write_id":privacy_write_id,"render_location":"COMET_MEDIA_VIEWER","actor_id":self.Data['__user'],"client_mutation_id":"1"},"privacySelectorRenderLocation":"COMET_MEDIA_VIEWER","scale":2,"storyRenderLocation":None,"tags":None}
            self.Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'CometPrivacySelectorSavePrivacyMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id': '6846271792123707'})
            pos = self.r.post('https://web.facebook.com/api/graphql/', data=self.Data, cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
            if '"selected_option":{"privacy_row_input":{"allow":[],"base_state":"%s","deny":[],"privacy_targeting"'%(self.privacy) in str(pos): return({'status':'success','id':photo_id,'privacy':self.privacy,'message':None})
            else: return({'status':'failed','id':photo_id,'privacy':None,'message':'Spam Or Something'})
        except Exception as e: return({'status':'failed','id':None,'privacy':None,'message':'Something Went Wrong'})

class AlbumPrivacy():

    def __init__(self, r=False, cookie=False, album=None, privacy=None):

        self.r = r
        self.cookie = cookie
        self.url = ConvertURL(album)
        try: self.req = self.r.get(self.url, headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        except Exception as e: self.req = None
        self.Data = GetData(self.req)

        if   privacy == 1: self.privacy = 'EVERYONE'
        elif privacy == 2: self.privacy = 'FRIENDS'
        else:              self.privacy = 'SELF'

    def Execute(self):
        try:
            privacy_write_id = re.search(r'"privacy_write_id":"(.*?)"',str(self.req)).group(1)
            album_id = re.search(r'"mediaSetToken":"a.(.*?)"',str(self.req)).group(1)
            Var = {"input":{"privacy_mutation_token":None,"privacy_row_input":{"allow":[],"base_state":self.privacy,"deny":[],"tag_expansion_state":"UNSPECIFIED"},"privacy_write_id":privacy_write_id,"render_location":"COMET_STREAM","actor_id":self.Data['__user'],"client_mutation_id":"1"},"privacySelectorRenderLocation":"COMET_STREAM","scale":2,"storyRenderLocation":None,"tags":None}
            self.Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'CometPrivacySelectorSavePrivacyMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id': '6846271792123707'})
            pos = self.r.post('https://web.facebook.com/api/graphql/', data=self.Data, cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
            if '"selected_option":{"privacy_row_input":{"allow":[],"base_state":"%s","deny":[],"privacy_targeting"'%(self.privacy) in str(pos): return({'status':'success','id':album_id,'privacy':self.privacy,'message':None})
            else: return({'status':'failed','id':album_id,'privacy':None,'message':'Spam Or Something'})
        except Exception as e: return({'status':'failed','id':None,'privacy':None,'message':'Something Went Wrong'})