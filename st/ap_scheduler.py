from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
import os
import re
import subprocess
import pandas as pd 
import datetime
from st.models import Account, MAC


def MAC_atsume():# 任意の関数名
    # ここに定期実行したい処理を記述する
    print("MACアドレス取得")
    subprocess.run(["chmod", "711", "st/shell/st/syusseki.sh"])
    subprocess.run(["st/shell/st/syusseki.sh","argument"], shell=True)
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
    
    #出退勤の登録
    MAC_adress = []
    kosuum = len(MAC.objects.all())
    records = MAC.objects.all()

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
        
        if private in MAC_adress or kotei in MAC_adress:
            print("いる")
            user.zaisitu_state = "いる"
            user.syusseki_state = "出席"
            user.save()
        else:
            print("いない")
            user.zaisitu_state = "いない"
            user.save()
   
   
def nissu():
    user_records = Account.objects.all()
    kosuuu = len(Account.objects.all())

    for i in range(0,kosuuu,1):
        name = user_records[i].last_name
        syusseki = user_records[i].syusseki_state
        nissu = user_records[i].syusseki_Nissu
        nissu = int(nissu)

        user = Account.objects.get(last_name=name)

        if syusseki == "出席":
            nissu += 1
            user.syusseki_Nissu = nissu
            user.save()

def reset():
    user_records = Account.objects.all()
    kosuuu = len(Account.objects.all())
    print("リセット")

    for i in range(0,kosuuu,1):
        name = user_records[i].last_name
        syusseki = user_records[i].syusseki_state
        user = Account.objects.get(last_name=name)
        user.syusseki_state = "欠席"
        user.save()

def nissu_reset():
    dt_now = datetime.datetime.now()
    day = dt_now.day
    print("リセット判定")
    if (day==5):
        user_records = Account.objects.all()
        kosuuu = len(Account.objects.all())
        print("日数リセット")

        for i in range(0,kosuuu,1):
            name = user_records[i].last_name
            nissu = user_records[i].syusseki_Nissu
            user = Account.objects.get(last_name=name)
            print(user.syusseki_Nissu)
            user.syusseki_Nissu = 0
            print(name)
            user.save()

def start():
  scheduler = BackgroundScheduler()
  scheduler.add_job(MAC_atsume, 'interval' , minutes=20)# 毎分20分ごとに実行
  scheduler.add_job(nissu, 'cron' , hour=23 ,minute=30)# 23時30分に実行
  scheduler.add_job(reset, 'cron' , hour=23 ,minute=55)# 23時55分に実行
  scheduler.add_job(nissu_reset, 'cron' , hour=15 ,minute=48)# 23時55分に実行
  scheduler.start()