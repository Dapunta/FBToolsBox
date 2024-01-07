# FBToolsBox
Facebook Automation Tools  
Author  : [**Dapunta Khurayra X**](https://www.facebook.com/Dapunta.Khurayra.X)  
Library : [**FBToolsBox**](https://github.com/Dapunta/FBToolsBox)  
Release : 01/01/2024  
Last Update : 07/01/2024  
Version : 0.0.2  
Python  : 3.10 - 3.12  
<br>  
<br>

## Installation
```python
pip install fbtoolsbox
```
<br>  
<br>  
<br>

## Features
After Finishing Reading The Documentation,  
See The [**Instructions**](#instructions-for-use) For Usage
1. Login via Cookie, Email, and Phone
   - [Login Cookie](#login-with-cookie)
   - [Login Email](#login-with-email--password)
   - [Login Phone](#login-with-phone--password)
2. Get Access Token `EAAG`, `EAAB`, `EAAD`, `EAAC`, `EAAF` and `EABB`
   - [Token EAAG](#get-access-token)
   - [Token EAAB](#get-access-token)
   - [Token EAAD](#get-access-token)
   - [Token EAAC](#get-access-token)
   - [Token EAAC](#get-access-token)
   - [Token EABB](#get-access-token)
3. Get Information of Profile, Page, and Group
   - [Info Profile](#get-info-profile)
   - [Info Page](#get-info-page)
   - [Info Group](#get-info-group)
4. Automation 1 
   - [Post To Feed](#post-to-feed)
   - [Post To Group](#post-to-group)
   - [Comment To Post](#comment-to-post)
   - [React To Post](#react-to-post)
   - [Share To Feed](#share-to-feed)
   - [Share To Group](#share-to-group)
5. Change Privacy
   - [Post](#post-privacy)
   - [Photo](#photo-privacy)
   - [Album](#album-privacy)
6. Friend Option
   - [Add Friend](#friend-option)
   - [Unfriend](#friend-option)
   - [Follow](#friend-option)
   - [Unfollow](#friend-option)
   - [Block](#friend-option)
   - [Unblock](#friend-option)
<br>  
<br>
<br>

## Create Account
```python
from FBTools.CreateAccount import CreateAccount

name = 'Input Your Name Here'
password = 'Input Your Password Here'
birthday = '25/12/1995' # DD/MM/YYYY
email = 'examplename@example.com'
gender = 1 # 1=Male, 0=Female
CA = CreateAccount()
CA.SetData(name=name, password=password, birthday=birthday, email=email, gender=gender)
CA.Create()
```
Parameter  
>name : Name You Want To Create (string, default=None)  
password : Password You Want To Create (string, default=None)  
birthday : Birth Date You Want To Set (string, default=None)  
email : Email You Want To Register (string, default=None)  
phone : Phone You Want To Register (string, default=None)  
gender : Gender You Want To Set (bool, default=0 -> female)  
<br> 
<br> 
<br>

## Login

#### Parameter
```python
cookie   = 'datr=nxbaxnynx; sb=axn...' # Input Your Cookie Here
email    = 'dapuntaxayonara@gmail.com' # Input Your Email Here
phone    = '6282245780524'             # Input Your Phone Here
password = 'satusampaidelapan'         # Input Your Password Here
```

#### Login With Cookie
```python
from FBTools import Start
FB = Start(cookie=cookie)
```

#### Login With Email & Password
```python
from FBTools import Start
FB = Start(email=email, password=password)
```

#### Login With Phone & Password
```python
from FBTools import Start
FB = Start(phone=phone, password=password)
```
<br>  
<br>  
<br>

## Instructions For Use
If you want to use **one cookie** (single cookie) to run this tools, put [```LoginCookie```](#login-with-cookie) or [```LoginEmail```](#login-with-email--password) or [```LoginPhone```](#login-with-phone--password) on top, or put it in a different def (make your own ```def login()```)
```python
from FBTools import Start

def Login():
    cok = input('Input Your Cookie : ')
    FB = Start(cookie=cok) #--> Single Cookie
    if FB.IsValid:
        BotComment(FB)
    else:
        exit('Cookie Invalid')

def BotComment(FB):
    post = input('Input ID Post : ')
    comt = input('Write Comment : ')
    loop = int(input('How Many : '))
    for i in range(loop):
        Comment = FB.CommentToPost(post=post, text=comt)
        print(Comment)

if __name__ == '__main__':
   Login()
```
If you want to use **many cookies** (multi cookies) to run this tools, put [```LoginCookie```](#login-with-cookie) or [```LoginEmail```](#login-with-email--password) or [```LoginPhone```](#login-with-phone--password) in the same function as the next object call                  
```python
from FBTools import Start

list_cookie = ['cookie1','cookie2','cookie3','cookie4']
id_target   = '1827084332'

def BotFollow():
   for cok in list_cookie:
      FB = Start(cookie=cok) #--> Multi Cookies
      FO = FB.Follow(id_target)
      print(FO)

if __name__ == '__main__':
   BotFollow()
```
<br>  
<br>  
<br>

## Get Access Token
```python
TokenEAAG = FB.TokenEAAG()
TokenEAAB = FB.TokenEAAB()
TokenEAAD = FB.TokenEAAD()
TokenEAAC = FB.TokenEAAC()
TokenEAAF = FB.TokenEAAF()
TokenEABB = FB.TokenEABB()
```
<br>  
<br>  
<br>

## Get Info Account, Page, Group

#### Parameter
```python
# Must Be Included
target_profile = '100000198243102'               # ID/URL Profile Target (string, default=False)
target_page    = '100044426739616'               # ID/URL Page Target (string, default=False)
target_group   = '1824553201274304'              # ID/URL Group Target (string, default=False)
```

#### Get Info Profile
```python
profile = FB.GetInfoProfile(target_profile)
print(profile.id)
print(profile.username)
print(profile.name)
print(profile.short_name)
print(profile.gender)
print(profile.work)
print(profile.education)
print(profile.current_city)
print(profile.hometown)
print(profile.relationship)
print(profile.birthday)
print(profile.language)
print(profile.website)
print(profile.github)
print(profile.instagram)
print(profile.friend)
print(profile.follower)
```

#### Get Info Page
```python
page = FB.GetInfoPage(target_page)
print(page.id)
print(page.username)
print(page.name)
print(page.follower)
print(page.category)
```

#### Get Info Group
```python
group = FB.GetInfoGroup(target_group)
print(group.id)
print(group.username)
print(group.name)
print(group.privacy)
print(group.membership)
print(group.admin)
print(group.moderator)
print(group.member)
print(group.new_member)
print(group.post_last_day)
print(group.post_last_month)
print(group.visibility)
print(group.history)
print(group.description)
```
<br>  
<br>  
<br>

## Auto Post

#### Parameter
```python
# Must Be Included
text    = 'Hello! Test Bot Post'                             # Caption (string, default=None)
group   = '1824553201274304'                                 # Group ID (string, default=None)
# 'group' must include if post to group
# You must post at least 1 text or 1 photo

# Optional
url     = ['https://e.top4top.io/p_2916o42201.jpg']          # Picture URL (list, default=None)
tag     = ['1827084332','100000415317575','100000200420913'] # Friend ID You Want To Tag (list, default=None)
privacy = 1 # 1=Public, 2=Friends, 3=OnlyMe                  # Post Privacy (int, default=None)
```

#### Post To Feed
```python
Post = FB.PostToFeed(text=text, url=url, tag=tag, privacy=privacy)
```

#### Post To Group
```python
Post = FB.PostToGroup(group=group, text=text, url=url, tag=tag, privacy=privacy)
```

#### Return
```python
{'status':'success','id':idpost,'message':None}
{'status':'pending','id':idpost,'message':'Pending Post'}
{'status':'failed','id':None,'message':'cookie invalid'}
{'status':'failed','id':None,'message':"Don't Create Same/Duplicate Post"}
{'status':'failed','id':None,'message':'Your Account Restricted To Post In Group'}
{'status':'failed','id':None,'message':'Terjadi Kesalahan'}
```
<br>  
<br>  
<br>

## Auto Comment

#### Parameter
```python
# Must Be Included
post   = 'Facebook.com/6929777330379375'                    # ID/URL Post Target (string, default=None)
text   = 'Hello! Test Bot Comment'                          # Caption (string, default=None)
# You must comment at least 1 text or 1 photo

# Optional
photo  = 'https://e.top4top.io/p_2916o42201.jpg'            # Picture URL (string, default=None)
tag    = ['1827084332','100000415317575','100000200420913'] # Friend ID You Want To Tag (list, default=None)
```

#### Comment To Post
```python
Comment = FB.CommentToPost(post=post, text=text, photo=photo, tag=tag)
```

#### Return
```python
{'status':'success','id':comment_id,'message':None}
{'status':'failed','id':None,'message':'cookie invalid'}
{'status':'failed','id':None,'message':'Spam Or Something Else'}
{'status':'failed','id':None,'message':'Terjadi Kesalahan'}
```
<br>  
<br>  
<br>

## Auto React

#### Parameter
```python
# Must Be Included
post   = 'Facebook.com/6929777330379375'                            # ID/URL Post Target (string, default=None)
react  = 5 # 1=Like, 2=Love, 3=Haha, 4=Wow, 5=Care, 6=Sad, 7=Angry  # Reaction Type (int, default=2=Love)
```

#### React To Post
```python
Reaction = FB.ReactToPost(post=post, react=react)
```

#### Return
```python
{'status':'success','react_type':react_type,'message':None}
{'status':'failed','react_type':react_type,'message':'Spam Or Something Else'}
{'status':'failed','react_type':react_type,'message':'Terjadi Kesalahan'}
```
<br>  
<br>  
<br>

## Auto Share

#### Parameter
```python
# Must Be Included
post    = 'Facebook.com/6929777330379375'                    # ID/URL Post You Want To Share (string, default=None)
group   = '1824553201274304'                                 # Group ID (string, default=None)
# 'group' must include if share to group

# Optional
text    = 'Hello! Test Bot Share'                            # Caption (string, default=None)
tag     = ['1827084332','100000415317575','100000200420913'] # Friend ID You Want To Tag (list, default=None)
privacy = 1 # 1=Public, 2=Friends, 3=OnlyMe                  # Share Privacy (int, default=None)
```

#### Share To Feed
```python
Share = FB.ShareToFeed(post=post, text=text, tag=tag, privacy=privacy)
```

#### Share To Group
```python
Share = FB.ShareToGroup(post=post, group=group, text=text, tag=tag, privacy=privacy)
```

#### Return
```python
{'status':'success','id':idshare,'message':None}
{'status':'pending','id':idshare,'message':'Pending Post'}
{'status':'failed','id':None,'message':"Don't Create Same/Duplicate Post"}
{'status':'failed','id':None,'message':'post has been deleted or there is an error'}
{'status':'failed','id':None,'message':'Your Account Restricted To Post In Group'}
{'status':'failed','id':None,'message':'Terjadi Kesalahan'}
```
<br>  
<br>  
<br>

## Change Privacy

#### Parameter
```python
# Must Be Included
post    = '10217059556200871'                  # ID/URL Post  You Want To Change Privacy (string, default=None)
photo   = '10214228940637251'                  # ID/URL Photo You Want To Change Privacy (string, default=None)
album   = '146803788687013'                    # ID/URL Album You Want To Change Privacy (string, default=None)
privacy = 3 # 1=Public, 2=Friends, 3=OnlyMe    # Selected Privacy (int, default=3)
```

#### Post Privacy
```python
Privacy = FB.PostPrivacy(post=post, privacy=privacy)
```

#### Photo Privacy
```python
Privacy = FB.PhotoPrivacy(photo=photo, privacy=privacy)
```

#### Album Privacy
```python
Privacy = FB.AlbumPrivacy(album=album, privacy=privacy)
```

#### Return
```python
{'status':'success','id':id,'privacy':privacy,'message':None}
{'status':'failed','id':id,'privacy':None,'message':'Spam Or Something'}
{'status':'failed','id':None,'privacy':None,'message':'Something Went Wrong'}
```
<br>  
<br>  
<br>

## Friend Option

### Parameter
```python
id_target = '1827084332'    # ID Profile You Want To Give Action (string, default=False)
```

#### Add Friend
```python
AD = FB.AddFriend(id_target)
```

#### Unfriend
```python
UF = FB.UnFriend(id_target)
```

#### Follow
```python
FO = FB.Follow(id_target)
```

#### Unfollow
```python
UO = FB.UnFollow(id_target)
```

#### Block
```python
BL = FB.Block(id_target)
```

#### Unblock
```python
UB = FB.UnBlock(id_target)
```

#### Return
```python
{'status':'success','id':id_target,'message':None}
{'status':'failed','id':id_target,'message':'Account Spam or Cookie Invalid'}
{'status':'failed','id':None,'message':'ID Not Found or Cookie Invalid'}
```
<br>  
<br>  
<br>

## Account Settings
<br>

### 2 Factor Authentication
`Parameter`
```python
active   = True # True=On, False=Off    # 2FA Option (bool, default=None)
password = 'acumalaka99'                # Account Password (string, default=None)
```
`Code`
```python
A2F = FB.Authentication(active=active, password=password)
```
`Return`
```python
{'status':'success','key':Key2FA,'recovery':RecoveryCode,'message':None}
{'status':'failed','key':None,'recovery':None,'message':'Wrong Password'}
{'status':'failed','key':None,'recovery':None,'message':'Account Spam'}
{'status':'failed','key':None,'recovery':None,'message':'Failed To Authenticate'}
{'status':'failed','key':None,'recovery':None,'message':'Unknown Error'}
```
<br>

### Check Application
`Code`
```python
APP = FB.CheckApp()
```
`Return`
```python
{'active':[ActiveApps],'expired':[ExpiredApps]}
```
<br>

### Profile Guard
`Code`
```python
PG = FB.ProfileGuard(True) # True=On, False=Off
```
`Return`
```python
{'status':'active','message':None}
{'status':'inactive','message':None}
{'status':'failed','message':'Token EAAG Invalid, Please Remove Your 2FA'}
{'status':'failed','message':'Error, Something Went Wrong'}
```
<br>