# ��������� ������ �2
# ������ �4
# ������ � MultiIndex. ������� ������������� ������ � ���������� ������ �� ��������� .xs().

import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process JSON file with MultiIndex")
    parser.add_argument("--path", type=str, default='data.json', help="Input JSON file path")
    args = parser.parse_args()

    df = pd.read_json(args.path)
    df.set_index(["region", "category", "id"], inplace=True)
    
    # ������ �� ����� �������
    selected_data = df.xs("North", level="region")
    print(selected_data.head())
