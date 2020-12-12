import os


class Logger:
  '''
  ログを記録するクラス
  '''

  def __init__(self, file_name):
    '''
    初期化
    ファイル名指定でログ保存先生成
    - @param {str} file_name ファイル名
    '''
    DIR_NAME = "log"
    if os.path.exists(DIR_NAME) is False:
      os.mkdir(DIR_NAME)

    self.FILE_PATH = DIR_NAME + "/" + file_name
    with open(self.FILE_PATH, mode='w') as f:
      f.write("")

  def writingLogFile(self, add_str):
    '''
    追記
    @param {*} add_str 追記内容
    '''
    with open(self.FILE_PATH, mode='a') as f:
      f.write(str(add_str) + "\n")
    pass


if __name__ == "__main__":
  # お試し
  sample = Logger("test.txt")
  for i in range(10):
    sample.writingLogFile(i + 1)
