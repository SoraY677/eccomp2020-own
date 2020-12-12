
import random
import evaluater as eval


class Harmony:
  '''
  ハーモニー単体を管理するクラス
  '''

  def __init__(self, R_A=0.8, R_P=0.3):
    '''
    初期化
    - @param {float} R_A 選択比率
    - @param {float} R_P 値調整比率
    '''
    self.R_A = R_A
    self.R_P = R_P

  def generate(self, length, alpha, beta):
    '''
    解を生成
    - @param {Integer} length 解の長さ
    - @param {Array} alpha
    - @param {Array} beta

    '''
    # 制約条件を満たす解を生成
    while True:
      x = "".join([str(random.randint(1, 6)) for i in range(length)])
      result = eval.evaluate(x_str=x, mode="constraint", bias_alpha=alpha, bias_beta=beta, valiables=len(x))
      if result.count(0) == len(result):
        break
    # 結果
    self.value = {
        "x": x,
        "objective": eval.evaluate(x_str=x, bias_alpha=alpha, bias_beta=beta, valiables=len(x))
    }

  def renew(self, length, origin_harmony_list, alpha, beta, change_count=1):
    '''
    解の作り変え
    - @param {Integer} length,
    - @param {Array} origin_harmony_list 変更前となるharmonyのリスト
    - @param {Array} alpha
    - @param {Array} beta
    - @param {Number} change_count
    '''

    # 対象となる解を決定
    r = random.randint(0, len(origin_harmony_list) - 1)
    while True:
      # 新規解
      newx = ""
      for i in range(length):
        if random.random() < self.R_A:
          if random.random() < self.R_P:
            # 既存の解を継承
            newx = newx + origin_harmony_list[r].value["x"][i]
          else:
            # 既存の解をすこし変更して継承
            add_num = (int(origin_harmony_list[r].value["x"][i]) - 1 + random.randint(-3, 3)) % 6 + 1
            if add_num < 0:
              add_num += 6
            newx = newx + str(add_num)
        else:
          # ランダムな継承
          newx = newx + str(random.randint(1, 6))

      result = eval.evaluate(x_str=newx, mode="constraint", bias_alpha=alpha, bias_beta=beta, valiables=len(newx))
      if result.count(0) == len(result):
        break

    self.value = {
        "x": newx,
        "objective": eval.evaluate(x_str=newx, bias_alpha=alpha, bias_beta=beta, valiables=len(newx))
    }


class HarmonySearch:
  def __init__(self, SOL_LENGTH, ITERATION=1000, HARMONY_NUM=10):
    '''
    設定
    - @param {Integer} SOL_LENGTH 解の長さ
    - @param {Integer} ITERATION 解探索のループ回数
    - @param {Integer} HARMONY_NUM ハーモニーの数
    '''
    self.harmony_list = [Harmony() for i in range(HARMONY_NUM)]
    self.SOL_LENGTH = SOL_LENGTH
    self.ITERATION = ITERATION

  def initalize(self, alpha, beta):
    '''
    初期化
    - @param {float} alpha
    - @param {float} beta
    '''
    self.alpha = alpha
    self.beta = beta
    for harmony in self.harmony_list:
      harmony.generate(length=self.SOL_LENGTH, alpha=alpha, beta=beta)

  def renew(self):
    '''
    解を新規生成
    '''
    # 新しい解を生成
    new_harmony = Harmony()
    new_harmony.renew(length=self.SOL_LENGTH, origin_harmony_list=self.harmony_list, alpha=self.alpha, beta=self.beta)

    # 最も悪いharmonyを探索
    worst_index = 0
    worst = self.harmony_list[worst_index].value["objective"]  # 最初はとりあえず先頭を対象に
    for harmony_index in range(1, len(self.harmony_list)):
      # 今記録している結果より悪い場合は更新
      if worst < self.harmony_list[harmony_index].value["objective"]:
        worst_index = harmony_index
        worst = self.harmony_list[worst_index].value["objective"]

    # 新たに生成したハーモニーが既存のハーモニーより場合は交換
    if self.harmony_list[worst_index].value["objective"] > new_harmony.value["objective"]:
      self.harmony_list[worst_index] = new_harmony

  def run(self, alpha, beta):
    '''
    解探索を実行する
    @return {String} 探索結果の文字列
    '''
    self.initalize(alpha=alpha, beta=beta)
    for i in range(self.ITERATION):
      self.renew()

    # 最良解を探索
    best_index = 0
    best = self.harmony_list[best_index].value["objective"]  # 最初はとりあえず先頭を対象に
    for harmony_index in range(1, len(self.harmony_list)):
      # 今記録している結果より良い場合は更新
      if best > self.harmony_list[harmony_index].value["objective"]:
        best_index = harmony_index
        best = self.harmony_list[best_index].value["objective"]

    return {
        "x": self.harmony_list[best_index].value["x"],
        "objective": self.harmony_list[best_index].value["objective"]
    }

  def show_result(self, label_str):
    print("-----------------------------")
    print(label_str)
    for harmony in self.harmony_list:
      print(harmony.value)
    print("-----------------------------")
