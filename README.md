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
CA.SetData(name=name,password=password,birthday=birthday,email=email,gender=gender)
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
L.LoginEmail(email=email,password=password,cookie=True)
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
