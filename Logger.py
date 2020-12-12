import os
import codecs


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
    with codecs.open(self.FILE_PATH, 'w', 'utf_8') as f:
      f.write("")

  def writingLogFile(self, add_str):
    '''
    追記
    @param {*} add_str 追記内容
    '''
    with codecs.open(self.FILE_PATH, 'a', 'utf_8') as f:
      f.write(str(add_str))
    pass
