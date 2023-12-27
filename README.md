# FBTools
Facebook Automation Tools  
>Python 3.10 - 3.12   
<br>

## Installation
```python
pip install FBTools
```
<br>  
<br>

### Create Account
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

### Login Cookies
```python
from FBTools.Login import Login

cookie = 'Input Cookie Here'
L = Login()
L.LoginCookie(cookie=cookie)
```
Parameter  
>cookie : Your Facebook Cookie (string, default=None)
<br>  
<br>

### Login Email & Password
```python
from FBTools.Login import Login

email = 'Input Email Here'
password = 'Input Password Here'
L = Login()
L.LoginEmail(email=email, password=password, cookie=True)
```
Parameter
>email    : Your Facebook Email (string, default=None)  
password : Your Facebook Password (string, default=None)  
cookie   : Return Cookies After Execute (bool, default=False)
<br>  
<br>

### Get Access Token
```python
from FBTools.GetToken import GetToken

cookie = 'Input Cookie Here'
GT = GetToken(cookie=cookie)
TokenEAAG = GT.TokenEAAG()
TokenEAAB = GT.TokenEAAB()
TokenEAAD = GT.TokenEAAD()
TokenEAAC = GT.TokenEAAC()
TokenEAAF = GT.TokenEAAF()
TokenEABB = GT.TokenEABB()
```
Parameter  
>cookie : Your Facebook Cookie (string, default=None)

Note  
>If you have logged in with cookies/email on Login(), you don't need to provide cookie parameters
<br>  
<br>

### Get Info Account
```python
from FBTools.GetInfo import GetInfoAccount

cookie = 'Input Cookie Here'
target = 'Input ID Target Here'

GIA = GetInfoAccount(cookie=cookie, target=target)
Profile = GIA.GetInfoProfile(general=True, friend=True, followers=True)

id         = Profile['id']
username   = Profile['username']
name       = Profile['name']
short_name = Profile['short_name']
hometown   = Profile['hometown']
location   = Profile['location']
friend     = Profile['friend']
followers  = Profile['followers']
```
Parameter  
>cookie : Your Facebook Cookie (string, default=None)  
target : ID/Username/URL Target Profile (string, default='me')  
general : Get General Information [id,username,name,shortname,hometown,location] (bool, default=True)  
friend : Get The Number Of Friends [friend] (bool, default=False)  
followers : Get The Number Of Followers [followers] (bool, default=False)  

Note  
>If you have logged in with cookies/email on Login(), you don't need to provide cookie parameters
<br>  
<br>

## Auto Post

### Parameter
```python
# Must Be Included
text    = 'Hello! Test Bot Post'                             # Caption (string, default=None)
group   = '1824553201274304'                                 # Group ID (string, default=None)
# 'group' must include if post to group
# You must post at least 1 text or photo

# Optional
cookie  = 'Input Your Cookie Here'                           # Cookie (string, default=None)
url     = ['https://e.top4top.io/p_2916o42201.jpg']          # Picture URL (list, default=None)
tag     = ['1827084332','100000415317575','100000200420913'] # Friend ID You Want To Tag (list, default=None)
privacy = 1 # 1=Public, 2=Friends, 3=OnlyMe                  # Post Privacy (int, default=None)
```

### Post To Feed
```python
from FBTools import AutoPost as AP

Post = AP.PostToFeed(cookie=cookie, text=text, url=url, tag=tag, privacy=privacy)
Exec = Post.Execute()
```

### Post To Group
```python
from FBTools import AutoPost as AP

Post = AP.PostToGroup(cookie=cookie, group=group, text=text, url=url, tag=tag, privacy=privacy)
Exec = Post.Execute()
```

### Return
```python
{'status':'success','id':idpost,'message':None}
{'status':'pending','id':idpost,'message':'Pending Post'}
{'status':'failed','id':None,'message':"Don't Create Same/Duplicate Post"}
{'status':'failed','id':None,'message':'Your Account Restricted To Post In Group'}
{'status':'failed','id':None,'message':'Terjadi Kesalahan'}
```

Note  
>If you have logged in with cookies/email on Login(), you don't need to provide cookie parameters
<br>  
<br>

## Auto Comment

### Parameter
```python
# Must Be Included
post   = 'Facebook.com/6929777330379375'                    # ID/URL Post Target (string, default=None)
text   = 'Hello! Test Bot Comment'                          # Caption (string, default=None)
# You must comment at least 1 text or photo

# Optional
cookie = 'Input Your Cookie Here'                           # Cookie (string, default=None)
photo  = 'https://e.top4top.io/p_2916o42201.jpg'            # Picture URL (string, default=None)
tag    = ['1827084332','100000415317575','100000200420913'] # Friend ID You Want To Tag (list, default=None)
```

### Comment To Post
```python
from FBTools import AutoComment as AC

Comment = AC.CommentToPost(cookie=cookie, post=post, text=text, photo=photo, tag=tag)
Exec = Comment.Execute()
```

### Return
```python
{'status':'success','id':comment_id,'message':None}
{'status':'failed','id':None,'message':'Spam Or Something Else'}
{'status':'failed','id':None,'message':'Terjadi Kesalahan'}
```

Note  
>If you have logged in with cookies/email on Login(), you don't need to provide cookie parameters
<br>  
<br>

## Auto React

### Parameter
```python
# Must Be Included
post   = 'Facebook.com/6929777330379375'                            # ID/URL Post Target (string, default=None)
react  = 2 # 1=Like, 2=Love, 3=Haha, 4=Wow, 5=Care, 6=Sad, 7=Angry  # Reaction Type (int, default=2=Love)

# Optional
cookie = 'Input Your Cookie Here'                                   # Cookie (string, default=None)
```

### React To Post
```python
from FBTools import AutoReact as AR

Reaction = AR.ReactToPost(cookie=cookie, post=post, react=react)
Exec = Reaction.Execute()
```

### Return
```python
{'status':'success','react_type':react_type,'message':None}
{'status':'failed','react_type':react_type,'message':'Spam Or Something Else'}
{'status':'failed','react_type':react_type,'message':'Terjadi Kesalahan'}
```

Note  
>If you have logged in with cookies/email on Login(), you don't need to provide cookie parameters
<br>  
<br>

