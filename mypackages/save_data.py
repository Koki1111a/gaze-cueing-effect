import os
import csv
from datetime import datetime

### ファイルへの書き込み ###
def save_to_csv(path_dir, data, file_name=None):
    
    if file_name is None:
        file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # 現在の日時を取得

    if not os.path.exists(path_dir): # ディレクトリがなければ作成
        os.makedirs(path_dir)

    with open(f'{path_dir}/{file_name}.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data) # リストの各行をファイルに書き込む