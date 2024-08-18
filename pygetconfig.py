from netmiko import ConnectHandler
from netmiko import SSHDetect
import csv
import datetime
import pandas as pd
#import numpy as np

#ログファイルに付与する日時形式を定義
datetime_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

#ホスト一覧を開く
csv_file = open("host_list.csv", "r", encoding="ms932", errors="", newline="" )
f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

#1行目はヘッダーのためスキップ
header = next(f)

#ホスト一覧を一行ずつ実施
for row in f:

	#コンフィグ取得中のホスト名を表示
	print('Getting Log for ' + row[0])

	#ホスト一覧から接続先設定を読み込む
	my_device = {
	   'device_type': row[4], #autodetect
	   'host':   row[1], #IPアドレスは2カラム目
	   'username': row[2], #ユーザー名は3カラム目
	   'password': row[3], #パスワードは4カラム目
	   'port' : 22, #SSHポートは22固定
	   "session_log": 'netmiko_session.log',
	}

	#ログファイル名を設定(ホスト名+日時)
	logfile = './logfile/' + row[0] + '_' + datetime_now + '.log'	
	
	#対象機器へSSH接続
	net_connect = ConnectHandler(**my_device)
	net_connect.enable()

	#実行コマンド定義
	#command0 = "show system ntp"

	#コマンド実行
	output0 = net_connect.send_command("execute log display", use_textfsm=True)

	# CSVで保存
	df = pd.DataFrame([output0])
	df.to_csv('output0.csv', index=False)

#対象機器から切断
net_connect.disconnect()
print('complete ')
print('------------------------------------------------')


