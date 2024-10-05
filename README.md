# netmiko
netmikoの学習

同ディレクトリ内に[logfile]フォルダを作成
同ディレクトリ内にhost_list.csvを作成
　hostname,ipaddr,user,pass
　Fortigate1,192.168.1.99,admin,12345
　Fortigate2,192.168.1.99,admin,12345


Ext_config-AOS＆comware.py
host,username,password,device_type
192.168.1.10,admin,password1,hp_procurve   # Aruba OS Switch
192.168.1.11,admin,password2,hp_comware    # Comware OS Switch
192.168.1.12,admin,password3,hp_procurve   # Aruba OS Switch
192.168.1.13,admin,password4,hp_comware    # Comware OS Switch

switch_info.csvファイルの読み込み

pandas を使用して、switch_info.csv から各スイッチの接続情報を取得します。
スイッチのホスト名、ユーザー名、パスワード、デバイスタイプが読み込まれます。
get_switch_config関数

netmiko を使用して、スイッチに接続し、構成コマンドを実行して設定情報を取得します。
Aruba OS Switch（hp_procurve）の場合は、show running-config を使用します。
Comware OS Switch（hp_comware）の場合は、display current-configuration を使用します。
取得した構成情報は、各スイッチのIPアドレスに基づいて個別のファイル（例：192.168.1.10_config.txt）に保存されます。
スクリプトの動作

スイッチに対して接続を行い、構成を取得し、それをファイルに保存します。処理が成功すると、各スイッチの構成ファイルが現在のディレクトリに保存されます。
4. 実行方法
switch_info.csv ファイルを作成し、接続するスイッチの情報を入力します。
Pythonスクリプトの中で、switch_info.csv のパスが正しいことを確認します。
スクリプトを実行すると、複数のスイッチから構成情報が取得され、それぞれの構成が個別のファイルに保存されます。
