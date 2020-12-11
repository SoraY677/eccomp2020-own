import sys
import copy
import time
from common import submitSolution, adjust
from genetic_algorithm import GenetictAlgorithm
# from harmony_search import HarmonySearch

SOLUTION_LENGTH = 60  # 解の長さ
SEARCH_MAX = 100  # 解提出回数の限界値

if __name__ == "__main__":
  # 最良値/ 初手はめちゃくちゃ大きくしておく
  best_objective = sys.maxsize
  # αβを初期化
  alpha = [2, 2, 2, 2, 2, 27, 5, 0, 0, 1, 0, 0, 1, 0, 0]
  beta = [5, 5, 5, 5, 5, 30, 8, 1, 0, 3, 0, 1, 2, 0, 0]
  # αβの一時退避先 / とりあえず同じものを入れておく
  alpha_tmp = copy.copy(alpha)
  beta_tmp = copy.copy(beta)
  # 探索手法定義
  # GA
  search = GenetictAlgorithm(
      ITERATE=100,
      SOLUTION_SIZE=SOLUTION_LENGTH,
      CROSSOVER_NUM=1
  )
  # ハーモニーサーチ
  # search = HarmonySearch(
  #     SOL_LENGTH=SOLUTION_LENGTH,
  #     ITERATION=1000,
  #     HARMONY_NUM=100
  # )

  vAlpha = [5, 6, 4, 3, 3, 27, 2, 0, 0, 0, 0, 0, 1, 0, 0]
  vBeta = [20, 10, 6, 7, 8, 30, 4, 0, 2, 5, 0, 0, 4, 1, 1]
  vGamma = [3, 3, 3, 3, 3, 1, 1, 3, 10, 4, 4, 4, 4, 4, 4]

  # 解提出限界までループ
  for i in range(SEARCH_MAX):
    # 時間計測
    start = time.time()

    # 現条件で最も評価値の高い結果を算出
    solution = search.run(alpha=alpha, beta=beta)

    # 解を提出し、結果を取得
    result = submitSolution(x=solution["x"], vAlpha=vAlpha, vBeta=vBeta, vGamma=vGamma)

    # 結果をもとに、αβ値の反映
    # 悪い場合
    if(best_objective <= result["objective"]):
      # αβを戻す
      alpha = copy.copy(alpha_tmp)
      beta = copy.copy(beta_tmp)
    # 良い場合
    else:
      # 最良情報を更新
      best_objective = result["objective"]
      best_x = solution["x"]

    # 前のαβを記録しておく
    alpha_tmp = copy.copy(alpha)
    beta_tmp = copy.copy(beta)

    # αβ値を変更
    adjust_result = adjust(alpha=alpha, beta=beta, length=SOLUTION_LENGTH)
    alpha = adjust_result["alpha"]
    beta = adjust_result["beta"]

    end = time.time()

    print("処理時間:")
    print(end - start)

  print("======================================")
  print("[result]")
  print("alpha-----")
  print(alpha_tmp)
  print("beta-----")
  print(beta_tmp)
  print("solve----")
  print("x:")
  print(best_x)
  print("objective:")
  print(best_objective)
