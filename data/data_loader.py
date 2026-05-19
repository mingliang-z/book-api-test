import json
import os



def load_test_data(file_name):
    """
       读取测试数据文件
       :param file_name: 文件名，如 'test_data.json'
       :return: 字典
       """
    current_dir = os.path.join(os.path.dirname(__file__))
    file_path = os.path.join(current_dir, file_name)

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)