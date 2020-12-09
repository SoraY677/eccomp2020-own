import evaluater as eval
import copy

'''
汎用的な関数を管理
'''


def createVirtualResult(
        x="",
        vAlpha=[2, 2, 2, 2, 2, 27, 5, 0, 0, 1, 0, 0, 1, 0, 0],
        vBeta=[5, 5, 5, 5, 5, 30, 8, 1, 0, 3, 0, 1, 2, 0, 0],
        vGamma=[3, 3, 3, 3, 3, 1, 1, 3, 10, 4, 4, 4, 4, 4, 4]):
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


def submitSolution(x):
  '''
  解の提出
  - @param {String} x 解:"●●"
  - @return {Object} 結果のオブジェクト
  '''
  result = createVirtualResult(
      x=x
  )
  return result


def adjust(alpha, beta, adjust_index):
  '''
  α,βを調整する処理
  @param {Array} alpha
  @param {Array} beta
  @param {Array} adjust_index 修正対象となるalpha,betaのindex
  '''
  # 新たに生成したαβ
  newAlpha = copy.copy(alpha)
  newBeta = copy.copy(beta)

  # 指定のindexのαβを指定の値に変更
  newAlpha[adjust_index] = 0.8
  newBeta[adjust_index] = 0.6

  return {
      "alpha": newAlpha,
      "beta": newBeta
  }
