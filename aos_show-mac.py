import pandas as pd
from netmiko import ConnectHandler

# Aruba OS SwitchからMACアドレステーブルを取得する関数
def get_mac_address_table(connection):
    # MACアドレステーブルを取得するコマンド
    output = connection.send_command("show mac-address")
    
    # 各行を改行で分割
    lines = output.splitlines()

    # MACアドレステーブルのデータを格納するリスト
    mac_table = []

    # データ行の解析 (適切なデータ行を探して処理する)
    for line in lines:
        parts = line.split()
        if len(parts) == 3:  # ArubaのMACテーブルは4つの項目に分かれているはず
            mac_address = parts[0].replace('-', '')  # ハイフンを削除
            port = parts[1]         # ポート番号
            vlan = parts[2]         # VLAN ID
            
            # リストに追加
            mac_table.append({
                'MAC Address': mac_address,
                'Port': port,
                'VLAN': vlan
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
    # Aruba OS Switchの接続情報
    device = {
        "device_type": "aruba_procurve_telnet",  # Aruba 2530はProCurveコマンドセットに対応
        "ip": "192.168.1.208",  # スイッチのIPアドレス
        "username": "admin",  # ユーザー名
        "password": "12345",  # パスワード
        "port": 23, 
        "secret": "12345",
    }

    # スイッチに接続
    connection = ConnectHandler(**device)
    
    # MACアドレステーブルを取得
    mac_table = get_mac_address_table(connection)
    
    # 接続を終了
    connection.disconnect()
    
    # MACアドレステーブルをCSVに保存
    save_to_csv(mac_table, 'mac_address_table.csv')

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()
