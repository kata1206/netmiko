import pandas as pd
from netmiko import ConnectHandler

# スイッチの構成を取得し、ファイルに保存する関数
def get_switch_config(device):
    try:
        # スイッチに接続
        print(f"Connecting to {device['host']} ({device['device_type']})")
        connection = ConnectHandler(**device)
        
        # Aruba OS Switch (ProCurve) の場合は "show running-config"
        if device['device_type'] == 'hp_procurve':
            config = connection.send_command("show running-config")

        # Comware OS Switch の場合は "display current-configuration"
        elif device['device_type'] == 'hp_comware':
            config = connection.send_command("display current-configuration")

        # 構成をファイルに保存
        filename = f"{device['host']}_config.txt"
        with open(filename, 'w') as f:
            f.write(config)

        print(f"Config for {device['host']} saved to {filename}")

        # 接続を終了
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect to {device['host']}: {e}")

# メイン処理
def main():
    # ホスト情報をCSVから読み込み
    hosts_df = pd.read_csv('switch_info.csv')  # CSVファイルを読み込む
    
    # 各スイッチに接続して構成を取得
    for _, row in hosts_df.iterrows():
        device = {
            'device_type': row['device_type'],  # ArubaかComwareか
            'host': row['host'],  # IPアドレス
            'username': row['username'],  # ユーザー名
            'password': row['password'],  # パスワード
        }

        # 構成を取得し、ファイルに保存
        get_switch_config(device)

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()
