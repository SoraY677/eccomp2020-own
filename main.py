import evaluater as eval

if __name__ == "__main__":
  for i in range(1):
    # 現条件で最も評価値の高い結果を算出
    result = eval.evaluate(x_str='"31552264665432613134314646226624645162511461153216"')
    # 解を提出し、結果を取得

    # 結果をもとに、αβ値の反映
    print(result)
    # αβ値を変更
