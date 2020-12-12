import random
import copy
import evaluater as eval


class GenetictAlgorithm:
  '''
  遺伝的アルゴリズム
  '''

  def __init__(
          self,
          ITERATE,
          SOLUTION_SIZE,
          ELITE_NUM=1,
          POP_NUM=10,
          MUTATE_PROB=0.01,
          CROSSOVER_NUM=1):
    '''
    設定
    - @param {Integer} ITERATE 世代交代数
    - @param {Integer} SOLUTION_SIZE 解の長さ
    - @param {Integer} ELITE_NUM エリート保存方式の対象数
    - @param {Integer} POP_NUM 解集団の数
    - @param {float} MUTATE_PROB 突然変異の確率
    - @param {Integer} CROSSOVER_NUM 交叉点の数
    '''
    self.ITERATE = ITERATE
    self.POP_NUM = POP_NUM
    self.SOLUTION_SIZE = SOLUTION_SIZE
    self.MUTATE_PROB = MUTATE_PROB
    self.CROSSOVER_NUM = CROSSOVER_NUM
    self.ELITE_NUM = ELITE_NUM

  def initialise(self, alpha, beta):
    '''
    初期化
    - @param {Array} alpha
    - @param {Array} beta
    '''
    self.alpha = alpha
    self.beta = beta
    self.population = []

    for popi in range(self.POP_NUM):
      # 制約条件を満たす解を用意
      while True:  # それまでループ
        pop = ''.join([str(random.randint(1, 6)) for i in range(self.SOLUTION_SIZE)])
        result = eval.evaluate(x_str=pop, bias_alpha=self.alpha, bias_beta=self.beta, mode="constraint", valiables=len(pop))
        if result.count(0) == len(result):
          objective = eval.evaluate(x_str=pop, bias_alpha=self.alpha, bias_beta=self.beta, valiables=len(pop))
          self.population.append({
              'x': pop,
              'objective': objective
          })
          break

    # 評価値で昇順ソートしておく
    self.population = sorted(self.population, key=lambda pop: pop['objective'])

  def select(self):
    '''
    交叉対象のルーレット選択
    '''
    population_reverse = []  # 解集団の各価値を反転させたもの

    # 解集団の合計点数を出しておく
    objective_sum = 0
    objective_max = self.population[-1]['objective']
    for pop in self.population:
      # 点数が最も低いもの(最良解)から降順になるように
      # 最も高いobjective-各解のobjectiveをして評価値を逆にする
      reverse_objective = objective_max - pop['objective'] + 1
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

  def crossover(self, individual1, individual2):
    '''
    交叉
    - @param {str} individual1 交叉対象となる解1
    - @param {str} individual2 交叉対象となる解2
    '''
    # 交叉点を決める配列を生成
    pos_list = [i for i in range(1, self.SOLUTION_SIZE)]  # [::self.CROSSOVER_NUM]
    random.shuffle(pos_list)
    pos_list = pos_list[:self.CROSSOVER_NUM]
    pos_list.sort()

    target = 0  # 対象となる解候補 / 最初は1
    target_list = [individual1, individual2]
    target_index = 0  # 探索対象となる交叉点配列の要素
    new_x = ""
    for i in range(self.SOLUTION_SIZE):
      if target_index < len(pos_list):  # オーバーフロー対策
        # 交叉点に行き着いたら反転
        if i == pos_list[target_index]:
          target = (target + 1) % 2
          target_index += 1
      # 解を生成
      new_x += target_list[target][i]

    return new_x

  def mutate(self, individual):
    '''
    突然変異
    - @param {str} individual 突然変異対象の解
    '''
    new_x = ''
    for i in range(len(individual)):
      if random.random() < self.MUTATE_PROB:
        new_x += str(random.randint(1, 6))
      else:
        new_x += individual[i]

    return new_x

  def run(self, alpha, beta):
    '''
    一連の処理を実行
    - @param {Array} alpha
    - @param {Array} beta
    '''
    self.initialise(alpha=alpha, beta=beta)

    for ite_i in range(self.ITERATE):
      new_population = []

      # エリート保存戦略
      for i in range(0, self.ELITE_NUM):
        new_population.append(copy.copy(self.population[i]))

      # 交叉と突然変異
      for i in range(self.ELITE_NUM, self.POP_NUM):
        # 制約条件を満たすまで実行
        while True:
          crossover_target = self.select()
          result = self.crossover(crossover_target[0], crossover_target[1])
          result = self.mutate(result)
          # 制約条件が全て0だったらループから抜ける
          constraint = eval.evaluate(x_str=result, bias_alpha=alpha, bias_beta=beta, valiables=len(result), mode="constraint")
          if constraint.count(0) == len(constraint):
            # 新規解集団に追加
            new_population.append({
                'x': result,
                'objective': eval.evaluate(x_str=result, bias_alpha=alpha, bias_beta=beta, bias_gamma=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], valiables=len(result))
            })
            break

      self.population = copy.copy(new_population)
      # 評価値で昇順ソートしておく
      self.population = sorted(self.population, key=lambda pop: pop['objective'])

    return self.population[0]
