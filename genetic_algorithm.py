import random
import evaluater as eval


class GenetictAlgorithm:
  '''
  遺伝的アルゴリズム
  '''

  def __init__(self, ITERATE, SOLUTION_SIZE, POP_NUM=10, MUTATE_PROB=0.01):
    '''
    設定
    - @param {Integer} ITERATE 世代交代数
    - @param {Integer} SOLUTION_SIZE 解の長さ
    - @param {Integer} POP_NUM 解集団の数
    - @param {float} MUTATE_PROB 突然変異の確率
    '''
    self.ITERATE = ITERATE
    self.POP_NUM = POP_NUM
    self.SOLUTION_NUM = SOLUTION_SIZE
    self.MUTATE_PROB = MUTATE_PROB

    pass

  def initialise(self, alpha, beta):
    '''
    初期化
    - @param {Array} alpha
    - @param {Array} beta
    '''
    self.alpha = alpha
    self.beta = beta
    self.population = []

    self.objective_max = 0  # 解集団のうち最も評価値の大きい(悪い)値
    for popi in range(self.POP_NUM):
      # 制約条件を満たす解を用意
      while True:  # それまでループ
        pop = ''.join([str(random.randint(1, 6)) for i in range(self.SOLUTION_NUM)])
        result = eval.evaluate(x_str=pop, bias_alpha=self.alpha, bias_beta=self.beta, mode="constraint", valiables=len(pop))
        if result.count(0) == len(result):
          objective = eval.evaluate(x_str=pop, bias_alpha=self.alpha, bias_beta=self.beta, valiables=len(pop))
          self.population.append({
              'x': pop,
              'objective': objective
          })
          if self.objective_max < objective:
            self.objective_max = objective
          break
    self.objective_max += 1

  def select(self):
    '''
    交叉対象のルーレット選択
    '''
    population_reverse = []  # 解集団の各価値を反転させたもの

    # 解集団の合計点数を出しておく
    objective_sum = 0
    for pop in self.population:
      # 点数が最も低いもの(最良解)から降順になるように
      # 最も高いobjective-各解のobjectiveをして評価値を逆にする
      reverse_objective = self.objective_max - pop['objective']
      population_reverse.append({
          'x': pop['x'],
          'objective': reverse_objective
      })
      objective_sum += reverse_objective

    # 対象探索
    result = []
    for si in range(2):
      prob = random.random()  # ルーレット選択用の確率を算出
      comp_objective_sum = 0  # 比較用のobjective加算変数
      for popi in range(len(population_reverse)):
        comp_objective_sum += population_reverse[popi]['objective']
        # 対象が見つかったら
        if prob < (comp_objective_sum / objective_sum):
          # 一つ目の探索対象として
          objective_sum -= population_reverse[popi]["objective"]
          result.append(population_reverse.pop(popi)['x'])
          break
    return result

  def crossover(self, pos_num):
    '''
    交叉
    - @param {Integer} pos_num 交叉点の数
    '''
    pass

  def mutate(self):
    pass

  def run(self):
    '''
    '''
    pass


if __name__ == "__main__":
  sample = GenetictAlgorithm(
      ITERATE=1000,
      SOLUTION_SIZE=60
  )
  sample.initialise(
      alpha=[2, 2, 2, 2, 2, 27, 5, 0, 0, 1, 0, 0, 1, 0, 0],
      beta=[5, 5, 5, 5, 5, 30, 8, 1, 0, 3, 0, 1, 2, 0, 0])

  sample.select()
