from netmiko import ConnectHandler
import csv
import datetime

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
	   'device_type': 'fortinet_ssh', #デバイスはcisco固定
	   'host':   row[1], #IPアドレスは2カラム目
	   'username': row[2], #ユーザー名は3カラム目
	   'password': row[3], #パスワードは4カラム目
	   'port' : 22, #SSHポートは22固定
	}

	#ログファイル名を設定(ホスト名+日時)
	logfile = './logfile/' + row[0] + '_' + datetime_now + '.log'	
	
	#対象機器へSSH接続
	net_connect = ConnectHandler(**my_device)
	net_connect.enable()

	#SSH不可の場合 > telnet
	#telnet不可の場合 > skipして次のホストへ
	
	#実行コマンド定義
	command0 = "get system status | grep Hostname"
	command1 = "show system ntp"
	command2 = "show system dns"

	#コマンド実行
	output0 = net_connect.send_command(command0, use_textfsm=True)
	output1 = net_connect.send_command(command1)
	output2 = net_connect.send_command(command2)

	#コマンド実行結果をLog出力
	with open(logfile, 'w') as f:
		print('------------------------------------------------', file=f)
		print(output0, file=f)
		print('------------------------------------------------', file=f)
		print(output1, file=f)
		print('------------------------------------------------', file=f)
		print(output2, file=f)
		print('------------------------------------------------', file=f)
	
	#対象機器から切断
	net_connect.disconnect()

	print('complete ')
	print('------------------------------------------------')


