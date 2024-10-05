import pandas as pd
from netmiko import ConnectHandler

# HP 5130スイッチからMACアドレステーブルを取得する関数
def get_mac_address_table(connection):
    # MACアドレステーブルを取得するコマンド
    output = connection.send_command("display mac-address")
    
    # 各行を改行で分割
    lines = output.splitlines()

    # MACアドレステーブルのデータを格納するリスト
    mac_table = []

    # データ行の解析
    for line in lines:
        parts = line.split()
        if len(parts) >= 4:  # 各行にMACアドレス, VLAN, State, Portが含まれている場合
            mac_address = parts[0].replace('-', '')  # ハイフンを削除
            port = parts[-1].replace('GE1/0/', '')  # 'GE1/0/' を削除
            
            # リストに追加 (VLAN ID とStateは削除)
            mac_table.append({
                'MAC Address': mac_address,
                'Port': port
            })

    return mac_table

# MACアドレステーブルをCSVファイルに保存する関数
def save_to_csv(mac_table, filename):
    # pandasのDataFrameに変換
    df = pd.DataFrame(mac_table)
    
    # CSVファイルとして保存
    df.to_csv(filename, index=False)
    print(f"MAC address table saved to {filename}")

# メイン処理
def main():
    # HP 5130スイッチの接続情報
    device = {
        "device_type": "hp_comware",  # HP 5130スイッチはComwareを使用
        "ip": "192.168.1.208",  # スイッチのIPアドレス
        "username": "admin",  # ユーザー名
        "password": "12345",  # パスワード
        "port": 23, 
        "secret": "12345",
    }

    try:
        # スイッチに接続
        print(f"Connecting to {device['host']}")
        connection = ConnectHandler(**device)
        
        # MACアドレステーブルを取得
        mac_table = get_mac_address_table(connection)
        
        # 接続を終了
        connection.disconnect()
        
        # MACアドレステーブルをCSVに保存
        save_to_csv(mac_table, 'mac_address_table.csv')
        
    except Exception as e:
        print(f"Failed to connect to {device['host']}: {e}")

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()
