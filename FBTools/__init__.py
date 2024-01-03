Version = 1.0

import requests
from .Login       import LoginCookie, LoginEmail, LoginPhone
from .GetToken    import TokenEAAG, TokenEAAB, TokenEAAD, TokenEAAC, TokenEAAF, TokenEABB
from .GetInfo     import GetInfoProfile, GetInfoPage, GetInfoGroup
from .Automation1 import PostToFeed, PostToGroup, CommentToPost, ReactToPost, ShareToFeed, ShareToGroup
from .Privacy     import PostPrivacy, PhotoPrivacy, AlbumPrivacy

global_cookie = False
global_requests = False

class Start():

    #--> New Session
    def __init__(self, cookie=False, email=False, phone=False, password=False):

        global global_cookie, global_requests
        self.user_agent_windows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        self.user_agent_android = 'Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36'
        self.r = requests.Session()

        if cookie:
            cookies = LoginCookie(self.r, self.user_agent_windows, cookie)
            if cookies: self.cookie = cookies
            else: self.cookie = False

        elif email and password:
            cookies = LoginEmail(self.r, self.user_agent_android, email,password)
            if cookies: self.cookie = cookies
            else: self.cookie = False

        elif phone and password:
            cookies = LoginPhone(self.r, self.user_agent_android, phone,password)
            if cookies: self.cookie = cookies
            else: self.cookie = False

        else: self.cookie = False

        global_cookie = self.cookie
        global_requests = self.r

    #--> Get Token
    def TokenEAAG(self): return(TokenEAAG(self.r, self.cookie))
    def TokenEAAB(self): return(TokenEAAB(self.r, self.cookie))
    def TokenEAAD(self): return(TokenEAAD(self.r, self.cookie))
    def TokenEAAC(self): return(TokenEAAC(self.r, self.cookie))
    def TokenEAAF(self): return(TokenEAAF(self.r, self.cookie))
    def TokenEABB(self): return(TokenEABB(self.r, self.cookie))

    #--> Get Information
    def GetInfoProfile(self, profile):
        if not profile: return({'status':'failed','message':'GetInfoProfile() must have "profile" parameter'})
        else: return(GetInfoProfile(r=self.r, cookie=self.cookie, profile=profile))
    def GetInfoPage(self, page):
        if not page: return({'status':'failed','message':'GetInfoPage() must have "page" parameter'})
        else: return(GetInfoPage(r=self.r, cookie=self.cookie, page=page))
    def GetInfoGroup(self, group):
        if not group: return({'status':'failed','message':'GetInfoGroup() must have "group" parameter'})
        else: return(GetInfoGroup(r=self.r, cookie=self.cookie, group=group))

    #--> Post
    def PostToFeed(self, group=None, text=None, url=None, tag=None, privacy=None):
        PTF = PostToFeed(r=self.r, cookie=self.cookie, group=group, text=text, url=url, tag=tag, privacy=privacy)
        return(PTF.Execute())
    def PostToGroup(self, group=None, text=None, url=None, tag=None, privacy=None):
        PTF = PostToGroup(r=self.r, cookie=self.cookie, group=group, text=text, url=url, tag=tag, privacy=privacy)
        return(PTF.Execute())

    #--> Comment
    def CommentToPost(self, post=None, text=None, photo=None, tag=None):
        CTP = CommentToPost(r=self.r, cookie=self.cookie, post=post, text=text, photo=photo, tag=tag)
        return(CTP.Execute())

    #--> React
    def ReactToPost(self, post=None, react=None):
        RTP = ReactToPost(r=self.r, cookie=self.cookie, post=post, react=react)
        return(RTP.Execute())

    #--> Share
    def ShareToFeed(self, post=None, group=None, text=None, tag=None, privacy=None):
        PTF = ShareToFeed(r=self.r, cookie=self.cookie, post=post, group=group, text=text, tag=tag, privacy=privacy)
        return(PTF.Execute())
    def ShareToGroup(self, post=None, group=None, text=None, tag=None, privacy=None):
        PTF = ShareToGroup(r=self.r, cookie=self.cookie, post=post, group=group, text=text, tag=tag, privacy=privacy)
        return(PTF.Execute())

    #--> Change Privacy
    def PostPrivacy(self, post=None, privacy=3):
        PP = PostPrivacy(r=self.r, cookie=self.cookie, post=post, privacy=privacy)
        return(PP.Execute())
    def PhotoPrivacy(self, photo=None, privacy=3):
        PP = PhotoPrivacy(r=self.r, cookie=self.cookie, photo=photo, privacy=privacy)
        return(PP.Execute())
    def AlbumPrivacy(self, album=None, privacy=3):
        AP = AlbumPrivacy(r=self.r, cookie=self.cookie, album=album, privacy=privacy)
        return(AP.Execute())