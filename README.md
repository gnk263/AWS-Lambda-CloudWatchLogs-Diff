# AWS-Lambda-CloudWatchLogs-Diff

「Lambdaが無い、かつ、ロググループがある」を満たすロググループの一覧を調べるスクリプトです

## Environment

- Python 3.7

## Usage

```bash
python chcker.py
```

## Delete LogGroups

`checker.py`にある下記のコメントを外せば削除できます。

```python
# 削除する
# delete_log_groups(list(different))
```
