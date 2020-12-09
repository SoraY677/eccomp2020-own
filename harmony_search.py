import random
from harmony import Harmony

LENGTH = 50
HARMONY_NUM = 10


class HarmonySearch:
  def __init__(self, alpha, beta):
    self.harmony_list = [Harmony() for i in range(HARMONY_NUM)]
    self.alpha = alpha
    self.beta = beta
    for harmony in self.harmony_list:
      harmony.generate(length=LENGTH, alpha=self.alpha, beta=self.beta)

  def renew(self):
    new_harmony = Harmony()
    new_harmony.renew(length=LENGTH, origin_harmony_list=self.harmony_list, alpha=self.alpha, beta=self.beta)

    # 最も悪いharmonyを探索
    worst_index = 0
    worst = self.harmony_list[worst_index].value["objective"]
    for harmony_index in range(1, len(self.harmony_list)):
      # 今記録している結果より悪い場合は更新
      if worst < self.harmony_list[harmony_index].value["objective"]:
        worst_index = harmony_index
        worst = self.harmony_list[worst_index].value["objective"]

    # 新たに生成したハーモニーが既存のハーモニーより場合は交換
    if self.harmony_list[worst_index].value["objective"] > new_harmony.value["objective"]:
      self.harmony_list[worst_index] = new_harmony

  def show_result(self, label_str):
    print("-----------------------------")
    print(label_str)
    for harmony in self.harmony_list:
      print(harmony.value)
    print("-----------------------------")


if __name__ == "__main__":
  hs = HarmonySearch([3, 3, 3, 3, 3, 29, 6, 1, 0, 2, 0, 1, 1, 0, 0], [3, 3, 3, 3, 3, 29, 6, 1, 0, 2, 0, 1, 1, 0, 0])
  hs.show_result("origin")
  for i in range(100000):
    hs.renew()
  hs.show_result("after")
