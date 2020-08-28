import json
import boto3
from typing import Dict, List

cw_logs_client = client = boto3.client('logs')
lambda_client = boto3.client('lambda')

def main():
    log_groups = get_log_groups()
    log_groups_name = convert(log_groups, 'logGroupName')

    lambda_functions = get_lambda_functions()
    lambda_functions_name = convert(lambda_functions, 'FunctionName')

    # ロググループ名から /aws/lambda/ (12文字)を取り除く
    log_group_name_only = list(map(lambda x: x[12:], log_groups_name))

    # ロググループにあって、Lambdaに無い値を求める
    different = set(log_group_name_only) - set(lambda_functions_name)

    for item in sorted(different):
        print(item)

    print('-----')
    print(f'Log Group: {len(log_group_name_only)}')
    print(f'Lambda   : {len(lambda_functions_name)}')
    print(f'different: {len(different)}')

def get_log_groups(token: str=None) -> List[Dict]:
    option = {
        'logGroupNamePrefix': '/aws/lambda/'
    }
    if token is not None:
        option['nextToken'] = token

    resp = cw_logs_client.describe_log_groups(**option)
    result = resp.get('logGroups', [])

    if 'nextToken' in resp:
        result += get_log_groups(resp['nextToken'])
    return result


def get_lambda_functions(token: str=None) -> List[Dict]:
    option = {}
    if token is not None:
        option['Marker'] = token

    resp = lambda_client.list_functions(**option)
    result = resp.get('Functions', [])

    if 'NextMarker' in resp:
        result += get_lambda_functions(resp['NextMarker'])
    return result


def convert(data: List[Dict], name: str) -> List[str]:
    """
    [{'xxx': 'apple', 'yyy': 'mac'}, {'xxx': 'orange', 'yyy': 'windows'}]
    みたいなDictの配列から
    ['apple', 'orange']
    みたいな特定のKeyの値だけのリストに変換する
    """
    return [x.get(name) for x in data]


if __name__ == "__main__":
    main()
