import random
import evaluater as eval


R_A = 0.8  # 選択比率
R_P = 0.3  # 値調整比率

BAND_WIDTH = 0.1


class Harmony:

  def generate(self, length, alpha, beta):
    while True:
      x = "".join([str(random.randint(1, 6)) for i in range(length)])
      result = eval.evaluate(x_str=x, mode="constraint", bias_alpha=alpha, bias_beta=beta)
      if result.count(0) == len(result):
        break
    self.value = {
        "x": x,
        "objective": eval.evaluate(x_str=x, bias_alpha=alpha, bias_beta=beta)
    }

  def renew(self, length, origin_harmony_list, alpha, beta, change_count=1):

    x = ""

    for i in range(length):
      if random.random() < R_A:
        r = random.randint(0, len(origin_harmony_list) - 1)
        if random.random() < R_P:
          x = x + origin_harmony_list[r].value["x"][i]
        else:
          add_num = (int(origin_harmony_list[r].value["x"][i]) - 1 + random.randint(-3, 3)) % 6 + 1
          if add_num < 0:
            add_num += 6
          x = x + str(add_num)
      else:
        x = x + str(random.randint(1, 6))

    self.value = {
        "x": x,
        "objective": eval.evaluate(x_str=x, bias_alpha=alpha, bias_beta=beta)
    }
