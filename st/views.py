from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView # テンプレートタグ
from .forms import AccountForm, AddAccountForm # ユーザーアカウントフォーム
from st.models import Account, MAC
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import os
import re
import subprocess
import pandas as pd

#ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('home'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'st/login.html')


#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))


#ホーム
@login_required
def home(request, pk):
    #post = get_object_or_404(Post, pk=pk)
    #return render(request, 'blog/post_detail.html', {'post': post})
    qs = Account.objects.all()
    params = {"UserID":request.user,"qs":qs}
    return render(request, "st/home.html",params)


#新規登録
class  AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        "add_account_form":AddAccountForm(),
        }

    #Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"st/register.html",context=self.params)

    #Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)
        

        #フォーム入力の有効検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記追加情報
            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # 画像アップロード有無検証from django.shortcuts import render, get_object_or_404

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"st/register.html",context=self.params)

#ユーザー情報を更新
def update(request):
    qs = Account.objects.all()
    params = {"UserID":request.user,"qs":qs}
    return render(request, "st/update.html",params)

#ユーザー情報を表示
def  UserView(request):
    template_name = "st/st-list.html"
    qs = Account.objects.all()
    params = {'message': 'メンバーの一覧', 'qs': qs}
    return render(request, template_name, params)

def ListView(request):
    template_name = "st/st-list2.html"
    ctx = {}
    qs2 = Account.objects.all()
    ctx["object_list"] = qs2

    return render(request, template_name, ctx)

#Macアドレスを取得
def MacView(request):
    template_name = "st/Mac.html"
    qs3 = MAC.objects.all()
    params = {'message': 'MACアドレス一覧', 'qs3': qs3}
    return render(request, template_name, params)


#Macアドレスを表示
def Mac2View(request):
    template_name = "st/Mac.html"
    filename = "syusseki.csv"
    data = pd.read_csv(filename,engine="python")
    MAC.objects.all().delete()

    for row in data.itertuples():
        text = row[1]
        p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
        adress = re.findall(p, text)
        MAC.objects.create(mac=adress)
    
    MAC.objects.filter(mac="[]").delete()
    Adress = []
    records = MAC.objects.all()
    kosuu = len(MAC.objects.all())
    for i in range(0,kosuu,1):
        s = records[i]
        Adress.append(s)
    
    MAC.objects.all().delete()
    for i in range(0,kosuu,1):
        adress1 = Adress[i] 
        adress2 = Adress[i]
        adress2 = str(adress2)
        print(adress2)
        adress2 = re.sub(r'[^0-9a-fA-F]', '', adress2)
        MAC.objects.create(mac=adress1,mac2=adress2)
   
    qs3 = MAC.objects.all()
    params = {'message': 'MACアドレス一覧', 'qs3': qs3}
    return render(request, template_name, params)

#Macアドレスを表示
def Mac3View(request):
    template_name = "st/Mac.html"
    subprocess.run(["chmod", "711", "st/shell/st/syusseki.sh"])
    subprocess.run(["st/shell/st/syusseki.sh","argument"], shell=True)
    filename = "syusseki.csv"
    data = pd.read_csv(filename,engine="python")
    
    for row in data.itertuples():
        text = row[1]
        adress = MAC(mac=text)
        adress.save()

    MAC.objects.all().delete()

    for row in data.itertuples():
        text = row[1]
        p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
        adress = re.findall(p, text)
        MAC.objects.create(mac=adress)
    
    MAC.objects.filter(mac="[]").delete()
    Adress = []
    records = MAC.objects.all()
    kosuu = len(MAC.objects.all())
    for i in range(0,kosuu,1):
        s = records[i]
        Adress.append(s)
    
    MAC.objects.all().delete()
    for i in range(0,kosuu,1):
        adress1 = Adress[i] 
        adress2 = Adress[i]
        adress2 = str(adress2) 
        print(adress2)
        adress2 = re.sub(r'[^0-9a-fA-F]', '', adress2)
        MAC.objects.create(mac=adress1,mac2=adress2)
   
    qs3 = MAC.objects.all()
    params = {'message': 'MACアドレス一覧', 'qs3': qs3}
    return render(request, template_name, params)

#出退勤を確認する
def Syututaikin(request):
    template_name = "st/st-list.html"
    """
    filename = "syusseki.csv"
    data = pd.read_csv(filename,engine="python")
    """

    MAC_adress = []
    kosuum = len(MAC.objects.all())
    records = MAC.objects.all()
    print(kosuum)
    """
    user_records = Account.objects.all().values_list("private_mac_adress" , flat=True)
    """
    user_records = Account.objects.all()
    kosuuu = len(Account.objects.all())
    
    for i in range(0,kosuum,1):
        s = records[i].mac2
        s = s.upper()
        print(s)
        MAC_adress.append(s)

    for i in range(0,kosuuu,1):
        name = user_records[i].last_name
        private = user_records[i].private_mac_adress
        kotei = user_records[i].kotei_mac_adress
        nissu = user_records[i].syusseki_Nissu
        nissu = int(nissu)

        user = Account.objects.get(last_name=name)
        
        """
        user_test = Account.objects.get(last_name="テスト2")
        user_test.first_name = "あかさたな"
        user_test.save()

        for s in range(kosuum):
            MA = MAC_adress[s]
        """
        if private in MAC_adress or kotei in MAC_adress:
            print("いる")
            user.zaisitu_state = "いる"
            user.syusseki_state = "出席"
            user.save()
        else:
            print("いない")
            user.zaisitu_state = "いない"
            user.save()
    
    qs = Account.objects.all()
    params = {'message': 'MACアドレス一覧', 'qs': qs}
    return render(request, template_name, params)

#特定のIPアドレスにPingを送信を表示
def waiView(request):
    template_name = "st/Mac.html"
    subprocess.run(["chmod", "711", "st/shell/st/syusseki2.sh"])
    subprocess.run(["st/shell/st/syusseki2.sh","argument"], shell=True)
    filename = "syusseki.csv"
    data = pd.read_csv(filename,engine="python")
   
    qs3 = MAC.objects.all()
    params = {'message': 'MACアドレス一覧', 'qs3': qs3}
    return render(request, template_name, params)

#特定のIPアドレスにPingを送信を表示
def wai2View(request):
    template_name = "st/Mac.html"
    subprocess.run(["chmod", "711", "st/shell/st/syusseki3.sh"])
    subprocess.run(["st/shell/st/syusseki3.sh","argument"], shell=True)
    filename = "syusseki.csv"
   
    qs3 = MAC.objects.all()
    params = {'message': 'MACアドレス一覧', 'qs3': qs3}
    return render(request, template_name, params)

