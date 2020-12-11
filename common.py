import evaluater as eval
import copy
import random

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


def submitSolution(x, vAlpha, vBeta, vGamma):
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


def adjust(alpha, beta, length):
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
  adjust_index = random.randint(0, 14)
  # 指定のindexのαβを指定の値に変更
  newBeta[adjust_index] = random.randint(0, f_max[adjust_index])
  newAlpha[adjust_index] = random.randint(0, newAlpha[adjust_index])

  return {
      "alpha": newAlpha,
      "beta": newBeta
  }
