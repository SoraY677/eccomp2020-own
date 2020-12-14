# eccomp2020 自分用リポジトリ

## 概要

> EC-Comp2020 problem: Designing a random number sequence to entertain game players. This problem is an N-variable, M-objective, L-constraint problem of creating cognitively unbiased random number sequences.

ゲームなどで用いられる乱数について完全にランダムにしていたとしても人間目ではそう感じないことがよくある。      
そのため、今回のコンペでは **「人間目で見て、より乱数っぽい乱数を生成する」** ことが目的である。  


## リンク系
- [【公式サイト】](https://ec-comp.jpnsec.org/)
- [【概要スライド】](https://docs.google.com/presentation/d/1KvjWgDBc-QAGRwFwR83loD2NwRTQLlhhzqA8KcwedEw/edit)


## 環境
### version
python3.8.5
### install
```bash
$ git clone https://github.com/SoraY677/eccomp2020-own.giteccomp2020.git
$ cd eccomp2020-own
$ pip install -r requirements.txt
```

### common build

```python
# スクリプトから直接解提出
python main.py

# jsonに一度出力してから解提出
python main2.py
```



