import evaluater as eval
import copy
import random
import math
import json
from subprocess import check_output
from typing import List

'''
汎用的な関数を管理
'''


def createVirtualResult(
        x,
        vAlpha,
        vBeta,
        vGamma):
  '''
  仮設定から仮の結果を出力する
  - @param {String} x submitされた結果
  - @param {Array} vAlpha 仮置きα
  - @param {Array} vBeta 仮置きβ
  - @param {Array} vGamma 仮置きγ
  '''
  return {
      "objective": eval.evaluate(x_str=x, bias_alpha=vAlpha, bias_beta=vBeta, bias_gamma=vGamma, valiables=len(x), mode="objective"),
      "constraint": eval.evaluate(x_str=x, bias_alpha=vAlpha, bias_beta=vBeta, bias_gamma=vGamma, valiables=len(x), mode="constraint"),
  }


def submitSolution(x, question_num):
  json_x = json.dumps(x)  # Convert a list into a JSON array
  request_str = "echo '%s' | opt submit --match=" + str(question_num)
  stdout = check_output(  # stdout gets a result in JSON
      request_str % json_x,  # Submit a solution
      shell=True)  # To use pipe, `shell` flag must be turned on
  result = json.loads(stdout.decode("utf-8"))  # Convert a JSON string into dict
  return result


def submitVirtualSolution(x, vAlpha, vBeta, vGamma):
  '''
  解の提出
  - @param {String} x 解:"●●"
  - @return {Object} 結果のオブジェクト
  '''
  result = createVirtualResult(
      x=x,
      vAlpha=vAlpha,
      vBeta=vBeta,
      vGamma=vGamma)
  return result


def adjust(alpha, beta, length, loop_count, MUTATE_PROB=0.05):
  '''
  α,βを調整する処理
  @param {Array} alpha
  @param {Array} beta
  @param {Array} adjust_index 修正対象となるalpha,betaのindex
  '''
  # 新たに生成したαβ
  newAlpha = copy.copy(alpha)
  newBeta = copy.copy(beta)

  f_max = [
      25 * length,
      25 * length / 4,
      25 * length / 4,
      25 * length / 4,
      25 * length / 4,
      length - 1,
      length - 1,
      length - 2,
      length - 3,
      length - 4,
      length - 5,
      length - 4,
      length - 5,
      length - 6,
      length - 7
  ]

  # 修正対象のindex
  adjust_index = random.randint(0, 14)

  # 通常時
  if(random.random() > MUTATE_PROB):
    # 0 の場合 1にする
    if newBeta[adjust_index] == 0:
      newBeta[adjust_index] = 1
    if newAlpha[adjust_index] == 0:
      newAlpha[adjust_index] = 1

    # 指定のindexのαβを修正
    newBeta[adjust_index] *= random.random() * (math.floor(loop_count / (length / 4)) + 1) * 2
    newAlpha[adjust_index] *= random.random() * (math.floor(loop_count / (length / 4)) + 1) * 2

  # 突然変異
  else:
    f_max = [
        25 * length,
        25 * length / 4,
        25 * length / 4,
        25 * length / 4,
        25 * length / 4,
        length - 1,
        length - 1,
        length - 2,
        length - 3,
        length - 4,
        length - 5,
        length - 4,
        length - 5,
        length - 6,
        length - 7
    ]
    newBeta[adjust_index] = random.random() * f_max[adjust_index]
    newAlpha[adjust_index] = random.random() * f_max[adjust_index]

    # αβの大小が逆転していたら、スワップ
  if newBeta[adjust_index] < newAlpha[adjust_index]:
    newBeta[adjust_index], newAlpha[adjust_index] = newAlpha[adjust_index], newBeta[adjust_index]

  return {
      "alpha": newAlpha,
      "beta": newBeta
  }
