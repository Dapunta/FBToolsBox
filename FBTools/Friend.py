import re, json
from .Tools import ConvertURL, GetData

DefaultUAWindows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
HeadersGet  = lambda i=DefaultUAWindows : {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Cache-Control':'max-age=0','Pragma':'akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-get-request-id,akamai-x-get-nonces,akamai-x-get-client-ip,akamai-x-feo-trace','Sec-Ch-Prefers-Color-Scheme':'light','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':i,'Viewport-Width':'924'}
HeadersPost = lambda i=DefaultUAWindows : {'Accept':'*/*','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.facebook.com','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':i}

def AddFriend(r, cookie, id):
    try:
        url = ConvertURL(id)
        req = r.get(url, headers=HeadersGet(), cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        Data = GetData(req)
        id_target = re.search(r'"userID":"(.*?)"',str(req)).group(1)
        Var = {"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,tap_search_bar,1704286545928,343492,190055527696468,,","friend_requestee_ids":[id_target],"refs":[None],"source":"profile_button","warn_ack_for_ids":[],"actor_id":Data['__user'],"client_mutation_id":"1"},"scale":2}
        Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'FriendingCometFriendRequestSendMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'7033797416660129'})
        pos = r.post('https://web.facebook.com/api/graphql/', data=Data, cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        if 'OUTGOING_REQUEST' in str(pos): tur = {'status':'success','id':id_target,'message':None}
        elif 'ARE_FRIENDS' in str(pos): tur = {'status':'failed','id':id_target,'message':'Account Has Been Friend'}
        else: tur = {'status':'failed','id':id_target,'message':'Account Spam or Cookie Invalid'}
    except Exception as e: tur = {'status':'failed','id':None,'message':'ID Not Found or Cookie Invalid'}
    return(tur)

def UnFriend(r, cookie, id):
    try:
        url = ConvertURL(id)
        req = r.get(url, headers=HeadersGet(), cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        Data = GetData(req)
        id_target = re.search(r'"userID":"(.*?)"',str(req)).group(1)
        Var = {"input":{"source":"bd_profile_button","unfriended_user_id":id_target,"actor_id":Data['__user'],"client_mutation_id":"1"},"scale":2}
        Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'FriendingCometUnfriendMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'8752443744796374'})
        pos = r.post('https://web.facebook.com/api/graphql/', data=Data, cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        if 'friend_remove' in str(pos) and 'unfriended_person' in str(pos): tur = {'status':'success','id':id_target,'message':None}
        elif 'friend_remove' in str(pos) and 'CRITICAL' in str(pos): tur = {'status':'failed','id':id_target,'message':'You Are Not Friend'}
        else: tur = {'status':'failed','id':id_target,'message':'Account Spam or Cookie Invalid'}
    except Exception as e: tur = {'status':'failed','id':None,'message':'ID Not Found or Cookie Invalid'}
    return(tur)

def Follow(r, cookie, id):
    try:
        url = ConvertURL(id)
        req = r.get(url, headers=HeadersGet(), cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        Data = GetData(req)
        id_target = re.search(r'"userID":"(.*?)"',str(req)).group(1)
        Var = {"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1704288389007,528507,190055527696468,,","is_tracking_encrypted":False,"subscribe_location":"PROFILE","subscribee_id":id_target,"tracking":None,"actor_id":Data['__user'],"client_mutation_id":"1"},"scale":2}
        Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'CometUserFollowMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'7308940305817568'})
        pos = r.post('https://web.facebook.com/api/graphql/', data=Data, cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        if '"subscribe_status":"IS_SUBSCRIBED"' in str(pos): tur = {'status':'success','id':id_target,'message':None}
        else: tur = {'status':'failed','id':id_target,'message':'Account Spam or Cookie Invalid'}
    except Exception as e: tur = {'status':'failed','id':None,'message':'ID Not Found or Cookie Invalid'}
    return(tur)

def UnFollow(r, cookie, id):
    try:
        url = ConvertURL(id)
        req = r.get(url, headers=HeadersGet(), cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        Data = GetData(req)
        id_target = re.search(r'"userID":"(.*?)"',str(req)).group(1)
        Var = {"action_render_location":"WWW_COMET_FRIEND_MENU","input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1704297349400,575,190055527696468,,","is_tracking_encrypted":False,"subscribe_location":"PROFILE","tracking":None,"unsubscribee_id":id_target,"actor_id":Data['__user'],"client_mutation_id":"1"},"scale":2}
        Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'CometUserUnfollowMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'6729032730553492'})
        pos = r.post('https://web.facebook.com/api/graphql/', data=Data, cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        if '"subscribe_status":"CAN_SUBSCRIBE"' in str(pos): tur = {'status':'success','id':id_target,'message':None}
        else: tur = {'status':'failed','id':id_target,'message':'Account Spam or Cookie Invalid'}
    except Exception as e: tur = {'status':'failed','id':None,'message':'ID Not Found or Cookie Invalid'}
    return(tur)

def Block(r, cookie, id):
    try:
        url = ConvertURL(id)
        req = r.get(url, headers=HeadersGet(), cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        Data = GetData(req)
        id_target = re.search(r'"userID":"(.*?)"',str(req)).group(1)
        Var = {"collectionID":None,"hasCollectionAndSectionID":False,"input":{"blocksource":"PROFILE","should_apply_to_later_created_profiles":False,"user_id":id_target,"actor_id":Data['__user'],"client_mutation_id":"1"},"scale":2,"sectionID":None,"isPrivacyCheckupContext":False}
        Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'ProfileCometActionBlockUserMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'6962402657213220'})
        pos = r.post('https://web.facebook.com/api/graphql/', data=Data, cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        if 'CRITICAL' in str(pos): tur = {'status':'failed','id':id_target,'message':'You Just Unblocked It'}
        elif 'user_block' in str(pos): tur = {'status':'success','id':id_target,'message':None}
        else: tur = {'status':'failed','id':id_target,'message':'Account Spam or Cookie Invalid'}
    except Exception as e: tur = {'status':'failed','id':None,'message':'ID Not Found or Cookie Invalid'}
    return(tur)

def UnBlock(r, cookie, id):
    try:
        req = r.get('https://www.facebook.com/', headers=HeadersGet(), cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        Data = GetData(req)
        Var = {"input":{"block_action":"UNBLOCK","setting":"USER","target_id":id,"actor_id":Data['__user'],"client_mutation_id":"1"},"profile_picture_size":36}
        Data.update({'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'BlockingSettingsBlockMutation','variables':json.dumps(Var),'server_timestamps':True,'doc_id':'6009824239038988'})
        pos = r.post('https://web.facebook.com/api/graphql/', data=Data, cookies={'cookie':cookie}, allow_redirects=True).text.replace('\\','')
        if '"UNBLOCK"' in str(pos): tur = {'status':'success','id':id,'message':None}
        else: tur = {'status':'failed','id':id,'message':'Account Spam or Cookie Invalid'}
    except Exception as e: tur = {'status':'failed','id':None,'message':'ID Not Found or Cookie Invalid'}
    return(tur)