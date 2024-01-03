import re, json, urllib
from .Tools import ConvertURL, GetData

DefaultUAWindows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
HeadersGet  = lambda i=DefaultUAWindows : {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Cache-Control':'max-age=0','Pragma':'akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-get-request-id,akamai-x-get-nonces,akamai-x-get-client-ip,akamai-x-feo-trace','Sec-Ch-Prefers-Color-Scheme':'light','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':i,'Viewport-Width':'924'}
HeadersPost = lambda i=DefaultUAWindows : {'Accept':'*/*','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.facebook.com','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':i}

class PostToFeed():

    def __init__(self, r=False, cookie=False, group=None, text=None, url=None, tag=None, privacy=None):

        self.r = r
        self.cookie = cookie
        try: self.req = self.r.get('https://web.facebook.com/', headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text
        except Exception as e: self.req = None
        self.Data = GetData(self.req)

        if text == None: self.text = ''
        else: self.text = text

        if url == None: self.attachments = []
        else:
            self.attachments = []
            for pt in url: self.UploadPhoto(pt)

        if tag == None: self.tag = []
        else: self.tag = tag

        if   privacy == None: self.privacy = 'EVERYONE'
        elif privacy == 1:    self.privacy = 'EVERYONE'
        elif privacy == 2:    self.privacy = 'FRIENDS'
        elif privacy == 3:    self.privacy = 'SELF'
        else:                 self.privacy = 'SELF'
    
    def UploadPhoto(self, url):
        try:
            file = {'file':('image.jpg',urllib.request.urlopen(url).read())}
            Data = self.Data.copy()
            Data.update({'source':'8','profile_id':Data['__user'],'waterfallxapp':'comet','upload_id':'jsc_c_1g'})
            pos = self.r.post('https://upload.facebook.com/ajax/react_composer/attachments/photo/upload',data=Data,files=file,cookies={'cookie':self.cookie},allow_redirects=True).text
            idf = re.search('"photoID":"(.*?)"',str(pos)).group(1)
            self.attachments.append({"photo":{"id":idf}})
        except Exception as e: pass

    def Execute(self):
        if not self.r or not self.cookie: tur = {'status':'failed','id':None,'message':'cookie invalid'}
        else:
            try:
                sessionid = re.search('"sessionID":"(.*?)"',str(self.req)).group(1)
                Var = {"input":{"composer_entry_point":"inline_composer","composer_source_surface":"timeline","idempotence_token":"%s_FEED"%(sessionid),"source":"WWW","attachments":self.attachments,"audience":{"privacy":{"allow":[],"base_state":self.privacy,"deny":[],"tag_expansion_state":"UNSPECIFIED"}},"message":{"ranges":[],"text":self.text},"with_tags_ids":self.tag,"inline_activities":[],"explicit_place_id":"0","text_format_preset_id":"0","logging":{"composer_session_id":sessionid},"navigation_data":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1703620101353,887511,190055527696468,,"},"tracking":[None],"event_share_metadata":{"surface":"newsfeed"},"actor_id":self.Data['__user'],"client_mutation_id":"1"},"displayCommentsFeedbackContext":None,"displayCommentsContextEnableComment":None,"displayCommentsContextIsAdPreview":None,"displayCommentsContextIsAggregatedShare":None,"displayCommentsContextIsStorySet":None,"feedLocation":"TIMELINE","feedbackSource":0,"focusCommentID":None,"gridMediaWidth":230,"groupID":None,"scale":1.5,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":True,"renderLocation":"timeline","useDefaultActor":False,"inviteShortLinkKey":None,"isFeed":False,"isFundraiser":False,"isFunFactPost":False,"isGroup":False,"isEvent":False,"isTimeline":True,"isSocialLearning":False,"isPageNewsFeed":False,"isProfileReviews":False,"isWorkSharedDraft":False,"UFI2CommentsProvider_commentsKey":"ProfileCometTimelineRoute","hashtag":None,"canUserManageOffers":False,"__relay_internal__pv__CometUFIIsRTAEnabledrelayprovider":False,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":False,"__relay_internal__pv__IsWorkUserrelayprovider":False,"__relay_internal__pv__IsMergQAPollsrelayprovider":False,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":False,"__relay_internal__pv__StoriesRingrelayprovider":False}
                self.Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name': 'ComposerStoryCreateMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'7338317599553815'})
                pos = self.r.post('https://web.facebook.com/api/graphql/', data=self.Data, cookies={'cookie':self.cookie}, allow_redirects=True).text
                if 'Status Baru Duplikat' in str(pos): tur = {'status':'failed','id':None,'message':"Don't Create Same/Duplicate Post"}
                else: tur = {'status':'success','id':re.search('"post_id":"(.*?)"',str(pos)).group(1),'message':None}
            except Exception as e: tur = {'status':'failed','id':None,'message':'Terjadi Kesalahan'}
        return(tur)

class PostToGroup():

    def __init__(self, r=False, cookie=False, group=None, text=None, url=None, tag=None, privacy=None):

        self.r = r
        self.cookie = cookie
        try: self.req = self.r.get('https://web.facebook.com/', headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text
        except Exception as e: self.req = None
        self.Data = GetData(self.req)

        if group == None: exit("\nParameter 'group' Must Be Included\n")
        else: self.group = group

        if text == None: self.text = ''
        else: self.text = text

        if url == None: self.attachments = []
        else:
            self.attachments = []
            for pt in url: self.UploadPhoto(pt)

        if tag == None: self.tag = []
        else: self.tag = tag
    
    def UploadPhoto(self, url):
        try:
            file = {'file':('image.jpg',urllib.request.urlopen(url).read())}
            Data = self.Data.copy()
            Data.update({'source':'8','profile_id':Data['__user'],'waterfallxapp':'comet','upload_id':'jsc_c_1g'})
            pos = self.r.post('https://upload.facebook.com/ajax/react_composer/attachments/photo/upload',data=Data,files=file,cookies={'cookie':self.cookie},allow_redirects=True).text
            idf = re.search('"photoID":"(.*?)"',str(pos)).group(1)
            self.attachments.append({"photo":{"id":idf}})
        except Exception as e: pass

    def Execute(self):
        if not self.r or not self.cookie: tur = {'status':'failed','id':None,'message':'cookie invalid'}
        else:
            try:
                sessionid = re.search('"sessionID":"(.*?)"',str(self.req)).group(1)
                Var = {"input":{"composer_entry_point":"publisher_bar_media","composer_source_surface":"group","composer_type":"group","logging":{"composer_session_id":sessionid},"source":"WWW","attachments":self.attachments,"message":{"ranges":[],"text":self.text},"with_tags_ids":self.tag,"inline_activities":[],"explicit_place_id":"0","text_format_preset_id":"0","navigation_data":{"attribution_id_v2":"CometGroupDiscussionRoot.react,comet.group,unexpected,1703627156789,472005,2361831622,,;GroupsCometPeopleRoot.react,comet.group.admin.people,unexpected,1703627121338,335432,,,;CometGroupDiscussionRoot.react,comet.group,via_cold_start,1703627109831,115805,2361831622,,"},"tracking":[None],"event_share_metadata":{"surface":"newsfeed"},"audience":{"to_id":self.group},"actor_id":self.Data['__user'],"client_mutation_id":"1"},"displayCommentsFeedbackContext":None,"displayCommentsContextEnableComment":None,"displayCommentsContextIsAdPreview":None,"displayCommentsContextIsAggregatedShare":None,"displayCommentsContextIsStorySet":None,"feedLocation":"GROUP","feedbackSource":0,"focusCommentID":None,"gridMediaWidth":None,"groupID":None,"scale":1.5,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":False,"renderLocation":"group","useDefaultActor":False,"inviteShortLinkKey":None,"isFeed":False,"isFundraiser":False,"isFunFactPost":False,"isGroup":True,"isEvent":False,"isTimeline":False,"isSocialLearning":False,"isPageNewsFeed":False,"isProfileReviews":False,"isWorkSharedDraft":False,"UFI2CommentsProvider_commentsKey":"CometGroupDiscussionRootSuccessQuery","hashtag":None,"canUserManageOffers":False,"__relay_internal__pv__CometUFIIsRTAEnabledrelayprovider":False,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":False,"__relay_internal__pv__IsWorkUserrelayprovider":False,"__relay_internal__pv__IsMergQAPollsrelayprovider":False,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":False,"__relay_internal__pv__StoriesRingrelayprovider":False}
                self.Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name': 'ComposerStoryCreateMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'7338317599553815'})
                pos = self.r.post('https://web.facebook.com/api/graphql/', data=self.Data, cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
                if 'Akun Anda dibatasi saat ini' in str(pos): tur = {'status':'failed','id':None,'message':'Your Account Restricted To Post In Group'}
                else:
                    idpost = re.search('"post_id":"(.*?)"',str(pos)).group(1)
                    if 'pending_posts/%s'%(idpost) in str(pos): tur = {'status':'pending','id':idpost,'message':'Pending Post'}
                    else: tur = {'status':'success','id':idpost,'message':None}
            except Exception as e: tur = {'status':'failed','id':None,'message':'Terjadi Kesalahan'}
        return(tur)

class CommentToPost():

    def __init__(self, r=False, cookie=False, post=None, text=None, photo=None, tag=None):

        self.r = r
        self.cookie = cookie
        self.url = ConvertURL(post)
        try: self.req = self.r.get(self.url, headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text
        except Exception as e: self.req = None
        self.Data = GetData(self.req)

        if text == None: self.text = ''
        else: self.text = text

        if photo == None: self.photo = []
        else: self.photo = self.UploadPhoto(photo)

        if tag == None: self.tag = []
        else:
            self.tag = []
            for i in tag: self.tag.append({"entity":{"id":i},"length":100,"offset":100})

    def UploadPhoto(self, url):
        try:
            data = self.Data.copy()
            file = {'file':('image.jpg',urllib.request.urlopen(url).read())}
            data.update({'source':'8','profile_id':data['__user'],'waterfallxapp':'comet','upload_id':'jsc_c_1g'})
            pos = self.r.post('https://web.facebook.com/ajax/ufi/upload/',data=data,files=file,cookies={'cookie':self.cookie},allow_redirects=True).text
            idf = re.search('"fbid":(.*?),',str(pos)).group(1)
            return([{"media":{"id":idf}}])
        except Exception as e: return([])

    def Execute(self):
        if not self.r or not self.cookie: tur = {'status':'failed','id':None,'message':'cookie invalid'}
        else:
            try:
                session_id = re.search('"sessionID":"(.*?)"',str(self.req)).group(1)
                client_id = re.search('"clientID":"(.*?)"',str(self.req)).group(1)
                try: feedback_id = re.search('"feedback":{"associated_group":null,"id":"(.*?)"},"is_story_civic":null',str(self.req)).group(1)
                except Exception as e: feedback_id = re.findall('"feedback_id":"(.*?)"',str(self.req))[-1]
                try: tracking = re.findall('{"action_link":null,"badge":null,"follow_button":null},"encrypted_tracking":"(.*?)"},"__module_operation_CometFeedStoryTitleSection_story"',str(self.req))[-1]
                except Exception as e: tracking = re.findall('"encrypted_tracking":"(.*?)"',str(self.req))[0]
                Vir = {"assistant_caller":"comet_above_composer","conversation_guide_session_id":session_id,"conversation_guide_shown":None}
                Var = {"feedLocation":"PERMALINK","feedbackSource":2,"groupID":None,"input":{"client_mutation_id":"1","actor_id":self.Data['__user'],"attachments":self.photo,"feedback_id":feedback_id,"formatting_style":None,"message":{"ranges":self.tag,"text":self.text},"attribution_id_v2":"CometSinglePostRoot.react,comet.post.single,via_cold_start,1703691784875,275571,,,","vod_video_timestamp":None,"is_tracking_encrypted":True,"tracking":[tracking,json.dumps(Vir)],"feedback_source":"OBJECT","idempotence_token":"client:%s"%(client_id),"session_id":session_id},"inviteShortLinkKey":None,"renderLocation":None,"scale":1.5,"useDefaultActor":False,"focusCommentID":None}
                self.Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'useCometUFICreateCommentMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'7128740410521626'})
                pos = self.r.post('https://web.facebook.com/api/graphql/', data=self.Data, cookies={'cookie':self.cookie}, allow_redirects=True).text
                if '"data":{"comment_create":{"feedback"' in str(pos): tur = {'status':'success','id':re.search('comment_id=(.*?)"',str(pos)).group(1),'message':None}
                else: tur = {'status':'failed','id':None,'message':'Spam Or Something Else'}
            except Exception as e: tur = {'status':'failed','id':None,'message':'Terjadi Kesalahan'}
        return(tur)

class ReactToPost():

    def __init__(self, r=False, cookie=False, post=None, react=None):
    
        self.r = r
        self.cookie = cookie
        self.url = ConvertURL(post)
        try: self.req = self.r.get(self.url, headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text
        except Exception as e: self.req = None
        self.Data = GetData(self.req)

        if react == None: self.react = 2
        else: self.react = react

    def Execute(self):
        if not self.r or not self.cookie: tur = {'status':'failed','react_type':None,'message':'cookie invalid'}
        else:
            try:
                react_type = ['Like','Love','Haha','Wow','Care','Sad','Angry'][self.react-1]
                react      = ['1635855486666999','1678524932434102','115940658764963','478547315650144','613557422527858','908563459236466','444813342392137'][self.react-1]
                session_id = re.search('"sessionID":"(.*?)"',str(self.req)).group(1)
                try: feedback_id = re.search('"feedback":{"associated_group":null,"id":"(.*?)"},"is_story_civic":null',str(self.req)).group(1)
                except Exception as e: feedback_id = re.findall('"feedback_id":"(.*?)"',str(self.req))[-1]
                try: encrypted_tracking = re.findall('{"action_link":null,"badge":null,"follow_button":null},"encrypted_tracking":"(.*?)"},"__module_operation_CometFeedStoryTitleSection_story"',str(self.req))[-1]
                except Exception as e: encrypted_tracking = re.findall('"encrypted_tracking":"(.*?)"',str(self.req))[0]
                var = {"input":{"attribution_id_v2":"CometSinglePostRoot.react,comet.post.single,via_cold_start,1697303736286,689359,,","feedback_id":feedback_id,"feedback_reaction_id":react,"feedback_source":"OBJECT","is_tracking_encrypted":True,"tracking":[encrypted_tracking],"session_id":session_id,"actor_id":self.Data['__user'],"client_mutation_id":"1"},"useDefaultActor":False,"scale":1.5}
                self.Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'CometUFIFeedbackReactMutation','variables':json.dumps(var),'server_timestamps':True,'doc_id':'6623712531077310'})
                pos = self.r.post('https://web.facebook.com/api/graphql/', data=self.Data, cookies={'cookie':self.cookie}, allow_redirects=True).text
                if '"feedback_react":{"feedback":{"can_viewer_react":true' in str(pos): tur = {'status':'success','react_type':react_type,'message':None}
                else: tur = {'status':'failed','react_type':react_type,'message':'Spam Or Something Else'}
            except Exception as e: tur = {'status':'failed','react_type':react_type,'message':'Terjadi Kesalahan'}
        return(tur)

class ShareToFeed():

    def __init__(self, r=False, cookie=False, post=None, group=None, text=None, tag=None, privacy=None):

        self.r = r
        self.cookie = cookie
        self.url = ConvertURL(post)
        try: self.req = self.r.get(self.url, headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text
        except Exception as e: self.req = None
        self.Data = GetData(self.req)

        if text == None: self.text = ''
        else: self.text = text

        if tag == None: self.tag = []
        else: self.tag = tag

        if   privacy == None: self.privacy = 'EVERYONE'
        elif privacy == 1:    self.privacy = 'EVERYONE'
        elif privacy == 2:    self.privacy = 'FRIENDS'
        elif privacy == 3:    self.privacy = 'SELF'
        else:                 self.privacy = 'SELF'

    def Execute(self):
        if not self.r or not self.cookie: tur = {'status':'failed','id':None,'message':'cookie invalid'}
        else:
            try:
                sessionid = re.search('"sessionID":"(.*?)"',str(self.req)).group(1)
                share_fbid = re.search('"share_fbid":"(.*?)"',str(self.req)).group(1)
                try: tracking = re.findall('{"action_link":null,"badge":null,"follow_button":null},"encrypted_tracking":"(.*?)"},"__module_operation_CometFeedStoryTitleSection_story"',str(self.req))[-1]
                except Exception as e: tracking = re.findall('"encrypted_tracking":"(.*?)"',str(self.req))[0]
                Var = {"input":{"composer_entry_point":"share_modal","composer_source_surface":"feed_story","composer_type":"share","idempotence_token":"%s_FEED"%(sessionid),"source":"WWW","is_tracking_encrypted":True,"tracking":[tracking,None],"audience":{"privacy":{"allow":[],"base_state":self.privacy,"deny":[],"tag_expansion_state":"UNSPECIFIED"}},"message":{"ranges":[],"text":self.text},"inline_activities":[],"text_format_preset_id":"0","attachments":[{"link":{"share_scrape_data":json.dumps({"share_type":22,"share_params":[int(share_fbid)]})}}],"with_tags_ids":self.tag,"logging":{"composer_session_id":sessionid},"navigation_data":{"attribution_id_v2":"CometSinglePostRoot.react,comet.post.single,via_cold_start,1703851502946,850033,,,"},"event_share_metadata":{"surface":"newsfeed"},"actor_id":self.Data['__user'],"client_mutation_id":"1"},"displayCommentsFeedbackContext":None,"displayCommentsContextEnableComment":None,"displayCommentsContextIsAdPreview":None,"displayCommentsContextIsAggregatedShare":None,"displayCommentsContextIsStorySet":None,"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":None,"gridMediaWidth":None,"groupID":None,"scale":2,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":True,"renderLocation":"homepage_stream","useDefaultActor":False,"inviteShortLinkKey":None,"isFeed":True,"isFundraiser":False,"isFunFactPost":False,"isGroup":False,"isEvent":False,"isTimeline":False,"isSocialLearning":False,"isPageNewsFeed":False,"isProfileReviews":False,"isWorkSharedDraft":False,"UFI2CommentsProvider_commentsKey":"CometModernHomeFeedQuery","hashtag":None,"canUserManageOffers":False,"__relay_internal__pv__CometUFIIsRTAEnabledrelayprovider":False,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":False,"__relay_internal__pv__IsWorkUserrelayprovider":False,"__relay_internal__pv__IsMergQAPollsrelayprovider":False,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":False,"__relay_internal__pv__StoriesRingrelayprovider":False}
                self.Data.update({'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'ComposerStoryCreateMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'7338317599553815'})
                pos = self.r.post('https://web.facebook.com/api/graphql/', data=self.Data, cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
                if 'Status Baru Duplikat' in str(pos): tur = {'status':'failed','id':None,'message':"Don't Create Same/Duplicate Post"}
                elif 'Tidak Dapat Membagikan Postingan' in str(pos): tur = {'status':'failed','id':None,'message':'post has been deleted or there is an error'}
                else: tur = {'status':'success','id':re.search('"post_id":"(.*?)"',str(pos)).group(1),'message':None}
            except Exception as e: tur = {'status':'failed','id':None,'message':'Terjadi Kesalahan'}
        return(tur)

class ShareToGroup():

    def __init__(self, r=False, cookie=False, post=None, group=None, text=None, tag=None, privacy=None):

        self.r = r
        self.cookie = cookie
        self.url = ConvertURL(post)
        try: self.req = self.r.get(self.url, headers=HeadersGet(), cookies={'cookie':self.cookie}, allow_redirects=True).text
        except Exception as e: self.req = None
        self.Data = GetData(self.req)

        if group == None: exit("\nParameter 'group' Must Be Included\n")
        else: self.group = group

        if text == None: self.text = ''
        else: self.text = text

        if tag == None: self.tag = []
        else: self.tag = tag

    def Execute(self):
        if not self.r or not self.cookie: tur = {'status':'failed','id':None,'message':'cookie invalid'}
        else:
            try:
                sessionid = re.search('"sessionID":"(.*?)"',str(self.req)).group(1)
                share_fbid = re.search('"share_fbid":"(.*?)"',str(self.req)).group(1)
                try: tracking = re.findall('{"action_link":null,"badge":null,"follow_button":null},"encrypted_tracking":"(.*?)"},"__module_operation_CometFeedStoryTitleSection_story"',str(self.req))[-1]
                except Exception as e: tracking = re.findall('"encrypted_tracking":"(.*?)"',str(self.req))[0]
                Var = {"input":{"composer_entry_point":"inline_composer","composer_source_surface":"group","composer_type":"group","logging":{"composer_session_id":sessionid},"source":"WWW","is_tracking_encrypted":True,"tracking":[tracking,None],"attachments":[{"link":{"share_scrape_data":json.dumps({"share_type":22,"share_params":[int(share_fbid)]})}}],"message":{"ranges":[],"text":self.text},"with_tags_ids":self.tag,"inline_activities":[],"explicit_place_id":"0","text_format_preset_id":"0","navigation_data":{"attribution_id_v2":"CometSinglePostRoot.react,comet.post.single,via_cold_start,1703874125062,522238,,,"},"event_share_metadata":{"surface":"newsfeed"},"audience":{"to_id":self.group},"actor_id":self.Data['__user'],"client_mutation_id":"1"},"displayCommentsFeedbackContext":None,"displayCommentsContextEnableComment":None,"displayCommentsContextIsAdPreview":None,"displayCommentsContextIsAggregatedShare":None,"displayCommentsContextIsStorySet":None,"feedLocation":"GROUP","feedbackSource":0,"focusCommentID":None,"gridMediaWidth":None,"groupID":None,"scale":2,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":False,"renderLocation":"group","useDefaultActor":False,"inviteShortLinkKey":None,"isFeed":False,"isFundraiser":False,"isFunFactPost":False,"isGroup":True,"isEvent":False,"isTimeline":False,"isSocialLearning":False,"isPageNewsFeed":False,"isProfileReviews":False,"isWorkSharedDraft":False,"UFI2CommentsProvider_commentsKey":None,"hashtag":None,"canUserManageOffers":False,"__relay_internal__pv__CometUFIIsRTAEnabledrelayprovider":False,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":False,"__relay_internal__pv__IsWorkUserrelayprovider":False,"__relay_internal__pv__IsMergQAPollsrelayprovider":False,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":False,"__relay_internal__pv__StoriesRingrelayprovider":False}
                self.Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'ComposerStoryCreateMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'7338317599553815'})
                pos = self.r.post('https://web.facebook.com/api/graphql/', data=self.Data, cookies={'cookie':self.cookie}, allow_redirects=True).text.replace('\\','')
                if 'Akun Anda dibatasi saat ini' in str(pos): tur = {'status':'failed','id':None,'message':'Your Account Restricted To Post In Group'}
                else:
                    idpost = re.search('"post_id":"(.*?)"',str(pos)).group(1)
                    if 'pending_posts/%s'%(idpost) in str(pos): tur = {'status':'pending','id':idpost,'message':'Pending Post'}
                    elif 'Tidak Dapat Membagikan Postingan' in str(pos): tur = {'status':'failed','id':None,'message':'post has been deleted or there is an error'}
                    else: tur = {'status':'success','id':idpost,'message':None}
            except Exception as e: tur = {'status':'failed','id':None,'message':'Terjadi Kesalahan'}
        return(tur)