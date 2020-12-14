import sys
import copy
import time
import math
from common import submitVirtualSolution, adjust, submitSolution
from genetic_algorithm import GenetictAlgorithm
# from harmony_search import HarmonySearch
from Logger import Logger

if __name__ == "__main__":
  sys_start = time.time()

  print("[input]")
  print("問題番号:")
  QUESTION_NUM = int(input())
  print("解の長さ:")
  SOLUTION_LENGTH = int(input())
  print("提出回数:")
  SEARCH_MAX = int(input())
  print("------------------------------")

  logger = Logger(str(QUESTION_NUM) + ".md")
  logger.writingLogFile(
      "# 問題概要 \n" +
      "- 問題番号:" + str(QUESTION_NUM) + "\n" +
      "- 解の長さ:" + str(SOLUTION_LENGTH) + "\n" +
      "- 提出回数:" + str(SEARCH_MAX) + "\n" +
      "-------------------------------------\n"
  )

  # 最良値/ 初手はめちゃくちゃ大きくしておく
  best_objective = sys.maxsize

  magnification = math.floor(SOLUTION_LENGTH / 60)
  # αβを初期化
  base_alpha = [2, 2, 2, 2, 2, 27, 5, 0, 0, 1, 0, 0, 1, 0, 0]
  alpha = [item * magnification for item in base_alpha]
  base_beta = [5, 5, 5, 5, 5, 30, 8, 1, 0, 3, 0, 1, 2, 0, 0]
  beta = [item * magnification for item in base_beta]

  logger.writingLogFile(
      "# 初期のバイアス\n" +
      "- α:" + str(alpha) + "\n" +
      "- β:" + str(beta) + "\n" +
      "---\n"
  )

  # αβの一時退避先 / とりあえず同じものを入れておく
  alpha_tmp = copy.copy(alpha)
  beta_tmp = copy.copy(beta)

  # 探索手法定義
  # GA
  ITERATION = 100
  MUTATE_PROB = 0.01
  search = GenetictAlgorithm(
      ITERATE=ITERATION,
      SOLUTION_SIZE=SOLUTION_LENGTH,
      CROSSOVER_NUM=magnification,
      MUTATE_PROB=MUTATE_PROB
  )

  logger.writingLogFile(
      "# 手法\n" +
      "**遺伝的アルゴリズム** \n"
      "- 遺伝回数" + str(ITERATION) + "\n" +
      "- 交叉点数:" + str(magnification) + "\n" +
      "- 突然変異率:" + str(MUTATE_PROB) + "\n" +
      "---\n"
  )

  # 解提出限界までループ
  for i in range(SEARCH_MAX):

    print("[" + str(i + 1) + "回目]")
    # 時間計測
    start = time.time()

    # 現条件で最も評価値の高い結果を算出
    solution = search.run(alpha=alpha, beta=beta)

    result = submitSolution(x=int(solution["x"]), question_num=QUESTION_NUM)
    print(result)

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
      print("objective更新！:" + str(best_objective))

    # 前のαβを記録しておく
    alpha_tmp = copy.copy(alpha)
    beta_tmp = copy.copy(beta)

    # αβ値を変更
    adjust_result = adjust(alpha=alpha, beta=beta, length=SOLUTION_LENGTH, loop_count=i, search_max=SEARCH_MAX)
    alpha = adjust_result["alpha"]
    beta = adjust_result["beta"]

    end = time.time()

    print("処理時間:" + str(end - start))
    print("-----------------------")
    logger.writingLogFile(
        "## [" + str(i + 1) + "回目]\n" +
        "- α:" + str(alpha_tmp) + "\n" +
        "- β:" + str(beta_tmp) + "\n" +
        "- 結果:" + str(result) + "\n"
        "- 処理時間:" + str(end - start) + "\n"
        "---\n"
    )

  sys_end = time.time()

  print("======================================")
  print("[result]")
  print("処理時間:" + str(sys_end - sys_start))
  print("-----------------")
  print("alpha :" + str(alpha_tmp))
  print("-----------------")
  print("beta :" + str(beta_tmp))
  print("-----------------")
  print("solve")
  print("x:")
  print(best_x)
  print("objective:")
  print(best_objective)

  logger.writingLogFile(
      "# result \n" +
      "- 処理時間:" + str(sys_end - sys_start) + "\n" +
      "- α :" + str(alpha_tmp) + "\n" +
      "- β :" + str(beta_tmp) + "\n" +
      "---\n"
      "【x】\n" +
      str(best_x) + "\n" +
      "【objective】\n" +
      str(best_objective) + "\n")
