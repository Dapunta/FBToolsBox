import re, json
from .Tools import ConvertURL, GetData

DefaultUAWindows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
HeadersGet  = lambda i=DefaultUAWindows : {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Cache-Control':'max-age=0','Pragma':'akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-get-request-id,akamai-x-get-nonces,akamai-x-get-client-ip,akamai-x-feo-trace','Sec-Ch-Prefers-Color-Scheme':'light','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':i,'Viewport-Width':'924'}
HeadersPost = lambda i=DefaultUAWindows : {'Accept':'*/*','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.facebook.com','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':i}

def TokenEAAG(r, cookie):
    try:
        url = 'https://business.facebook.com/business_locations'
        req = r.get(url,cookies={'cookie':cookie})
        tok = re.search(r'(\["EAAG\w+)', req.text).group(1).replace('["','')
        return(tok)
    except Exception as e: return('')

def TokenEAAB(r, cookie):
    try:
        req1 = r.get('https://www.facebook.com/adsmanager/manage/campaigns',cookies={'cookie':cookie},allow_redirects=True).text
        nek1 = re.search(r'window.location.replace\("(.*?)"\)',str(req1)).group(1).replace('\\','')
        req2 = r.get(nek1,cookies={'cookie':cookie},allow_redirects=True).text
        tok  = re.search(r'accessToken="(.*?)"',str(req2)).group(1)
        return(tok)
    except Exception as e: return('')

class GetInfoProfile():

    def __init__(self, r=False, cookie=False, profile=False):
        self.r = r
        self.cookie = cookie
        self.url = ConvertURL(profile)
        try: self.req = self.r.get(self.url, headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text
        except Exception as e: self.req = None
        self.Data = GetData(self.req)
        self.token_eaag = TokenEAAG(self.r, self.cookie)
        self.token_eaab = TokenEAAB(self.r, self.cookie)
        self.MainScrape()

    def MainScrape(self):
        Data = self.Data.copy()
        Target = re.search(r'"userID":"(.*?)"',str(self.req)).group(1)
        self.LootData(self.req, 0)
        raw_section_token, section_token = self.Navigation(Data, Target, 'about')
        collection_token = self.Scrap(Data, Target, raw_section_token, section_token, 1, None)
        self.Scrap(Data, Target, raw_section_token, section_token, 2, collection_token['BasicContact'])
        self.LootData(Target, 3)

    def Navigation(self, Data, Target, Route):
        Data.update({'client_previous_actor_id':Data['__user'],'route_url':'/%s/%s'%(Target,Route),'routing_namespace':'fb_comet'})
        pos = self.r.post('https://www.facebook.com/ajax/navigation/', data=Data, cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        raw_section_token = re.search(r'"rawSectionToken":"(.*?)"',str(pos)).group(1)
        section_token = re.search(r'"sectionToken":"(.*?)"',str(pos)).group(1)
        return (raw_section_token, section_token)

    def Scrap(self, Data, target_id, raw_section_token, section_token, type, collection_token):
        Var = {"UFI2CommentsProvider_commentsKey":"ProfileCometAboutAppSectionQuery","appSectionFeedKey":"ProfileCometAppSectionFeed_timeline_nav_app_sections__%s"%(raw_section_token),"collectionToken":collection_token,"pageID":target_id,"rawSectionToken":raw_section_token,"scale":2,"sectionToken":section_token,"showReactions":True,"userID":target_id,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":False}
        Data.update({'fb_api_req_friendly_name':'ProfileCometAboutAppSectionQuery','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'6958968654184286'})
        pos = self.r.post('https://web.facebook.com/api/graphql/', data=Data, cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
        self.LootData(pos, type)
        collection = {
            'BasicContact':re.search(r'"name":"Info Kontak dan Dasar","id":"(.*?)"',str(pos)).group(1),
            'Family':re.search(r'"name":"Keluarga dan Hubungan","id":"(.*?)"',str(pos)).group(1)}
        return(collection)

    def LootData(self, pos, type):
        if type == 0:
            try: self.id, self.name, self.gender, self.short_name = list(re.findall(r'"ProfileActionBlock","profile_owner":{"id":"(.*?)","name":"(.*?)","gender":"(.*?)","short_name":"(.*?)"',str(pos))[0])
            except Exception as e: self.id, self.name, self.gender, self.short_name = '', '', '', ''
            try: self.username = re.search(r'"userVanity":"(.*?)"',str(pos)).group(1)
            except Exception as e: self.username = ''
        elif type == 1:
            try: self.work = re.search(r'"text":"(.*?)"},"field_type":"work"',str(pos)).group(1).split('"text":"')[-1]
            except Exception as e: self.work = ''
            try: self.education = re.search(r'"text":"(.*?)"},"field_type":"education"',str(pos)).group(1).split('"text":"')[-1]
            except Exception as e: self.education = ''
            try: self.current_city = re.search(r'"text":"(.*?)"},"field_type":"current_city"',str(pos)).group(1).split('"text":"')[-1]
            except Exception as e: self.current_city = ''
            try: self.hometown = re.search(r'"text":"(.*?)"},"field_type":"hometown"',str(pos)).group(1).split('"text":"')[-1]
            except Exception as e: self.hometown = ''
            try: self.relationship = re.search(r'"text":"(.*?)"},"field_type":"relationship"',str(pos)).group(1).split('"text":"')[-1]
            except Exception as e: self.relationship = ''
        elif type == 2:
            try: self.birthday = ' '.join([i.split('"text":"')[-1] for i in re.findall(r'"text":"(.*?)"},"field_type":"birthday"',str(pos))])
            except Exception as e: self.birthday = ''
            try: self.language = re.search(r'"text":"(.*?)"},"field_type":"languages"',str(pos)).group(1).split('"text":"')[-1]
            except Exception as e: self.language = ''
            try: self.website = re.search(r'"text":"(.*?)"},"field_type":"website"',str(pos)).group(1).split('"text":"')[-1]
            except Exception as e: self.website = ''
            try: self.github = re.search(r'"text":"(.*?)"},"field_type":"screenname","list_item_groups":\[{"list_items":\[{"heading_type":\".*?\","text":{"delight_ranges":\[\],"image_ranges":\[\],"inline_style_ranges":\[\],"aggregated_ranges":\[\],"ranges":\[\],"color_ranges":\[\],"text":"GitHub"}',str(pos)).group(0).split('"text":"')[-2].split('"}')[0]
            except Exception as e: self.github = ''
            try: self.instagram = re.search(r'"text":"(.*?)"},"field_type":"screenname","list_item_groups":\[{"list_items":\[{"heading_type":\".*?\","text":{"delight_ranges":\[\],"image_ranges":\[\],"inline_style_ranges":\[\],"aggregated_ranges":\[\],"ranges":\[\],"color_ranges":\[\],"text":"Instagram"}',str(pos)).group(0).split('"text":"')[-2].split('"}')[0]
            except Exception as e: self.instagram = ''
        elif type == 3:
            try: self.friend = self.r.get('https://graph.facebook.com/%s/friends?limit=0&access_token=%s'%(str(pos),self.token_eaab),cookies={'cookie':self.cookie}).json()['summary']['total_count']
            except Exception as e: self.friend = 0
            try: self.follower = self.r.get('https://graph.facebook.com/%s/subscribers?limit=0&access_token=%s'%(str(pos),self.token_eaag),cookies={'cookie':self.cookie}).json()['summary']['total_count']
            except Exception as e: self.follower = 0

class GetInfoPage():

    def __init__(self, r=False, cookie=False, page=False):
        self.r = r
        self.cookie = cookie
        self.url = ConvertURL(page)
        try: self.req = self.r.get(self.url, headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text
        except Exception as e: self.req = None
        self.Data = GetData(self.req)
        self.ScrapGeneral()

    def ScrapGeneral(self):
        try: self.id = re.search(r'"userID":"(.*?)"',str(self.req)).group(1)
        except Exception as e: self.id = ''
        try: self.username = re.search(r'"userVanity":"(.*?)"',str(self.req)).group(1)
        except Exception as e: self.username = ''
        try: self.name = re.search(r'"ProfileActionBlock","profile_owner":{"id":"%s","name":"(.*?)","gender"'%(str(self.id)),str(self.req)).group(1)
        except Exception as e: self.name = ''
        try: 
            x = re.findall(r'"text":"(.*?)"},"uri"',str(self.req))
            self.follower = str('%s | %s'%(x[0],x[1])).replace(str('\\u00a0'),' ')
        except Exception as e: self.follower = ''
        try: self.category = re.search(r'"category_name":"(.*?)"',str(self.req)).group(1)
        except Exception as e: self.category = ''

class GetInfoGroup():

    def __init__(self, r=False, cookie=False, group=False):
        self.r = r
        self.cookie = cookie
        self.url = ConvertURL(group)
        try: self.req = self.r.get(self.url, headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text
        except Exception as e: self.req = None
        self.Data = GetData(self.req)
        self.ScrapGeneral()
        self.ScrapDetail()

    def ScrapGeneral(self):
        try: self.id = re.search(r'"groupID":"(.*?)"',str(self.req)).group(1)
        except Exception as e: self.id = ''
        try: self.username = re.search(r'"group_address":"(.*?)"',str(self.req)).group(1)
        except Exception as e: self.username = ''
        try: self.name = re.search(r'"id":"%s","name":"(.*?)"'%(str(self.id)),str(self.req)).group(1)
        except Exception as e: self.name = ''
        try: self.privacy = re.search(r'"text":"(.*?)"}},"group_member_profiles"',str(self.req)).group(1).split('"text":"')[-1]
        except Exception as e: self.privacy = ''
        try: self.membership = re.search(r'"viewer_join_state":"(.*?)"',str(self.req)).group(1)
        except Exception as e: self.membership = ''

    def ScrapDetail(self):
        Data = self.Data.copy()
        Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'CometGroupAboutRootQuery','variables': json.dumps({"groupID":self.id,"scale":2}),'server_timestamps':True,'doc_id':'7342142219152385'})
        pos = self.r.post('https://web.facebook.com/api/graphql/', data=Data, cookies={'cookie':self.cookie}, allow_redirects=True).json()
        try: self.description = pos['data']['group']['description_with_entities']['text']
        except Exception as e: self.description = ''
        try: self.admin = int(pos['data']['group']['facepile_admin_profiles']['count'])
        except Exception as e: self.admin = 0
        try: self.moderator = int(pos['data']['group']['facepile_moderator_profiles']['count'])
        except Exception as e: self.moderator = 0
        try: self.member = int(pos['data']['group']['if_viewer_can_see_activity_section']['group_total_members_info_text'].split(' ')[0].replace('.',''))
        except Exception as e: self.member = 0
        try: self.new_member = pos['data']['group']['if_viewer_can_see_activity_section']['group_new_members_info_text']
        except Exception as e: self.new_member = ''
        try: self.post_last_day = pos['data']['group']['if_viewer_can_see_activity_section']['number_of_posts_in_last_day']
        except Exception as e: self.post_last_day = ''
        try: self.post_last_month = pos['data']['group']['if_viewer_can_see_activity_section']['number_of_posts_in_last_month']
        except Exception as e: self.post_last_month = ''
        try: self.visibility = pos['data']['group']['about_info_items'][1]['group']['discoverability_info']['description']['text']
        except Exception as e: self.visibility = ''
        try: self.history = pos['data']['group']['about_info_items'][2]['group']['group_history']['group_history_summary']['text']
        except Exception as e: self.history = ''