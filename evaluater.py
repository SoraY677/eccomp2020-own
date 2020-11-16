#!/bin/env python
import json
import os
import sys
from traceback import format_exc

from jsonschema import validate, ValidationError
from scipy.stats import chi2
import yaml


variable_jsonschema_template = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "A random number sequence to evaluate bias",
  "type": "string",
  "minLength": %d,
  "maxLength": %d,
  "pattern": "^[1-6]*$"
}"""


def variable_jsonschema(dim):
  return json.loads(variable_jsonschema_template % (dim, dim))


def chisq(hist, dim):
  # type: (Dict[int], int) -> float
  """Chi-square of a given histgram."""
  n = sum(hist.values())
  bin = 6**dim
  m = n / bin
  chisq = sum((v - m) * (v - m) / m for v in hist.values())
  chisq += m * (bin - len(hist))  # zeros
  return chisq


def histgram(seq, begin=0, end=100, dim=1, step=1, pattern=lambda x: x):
  # type: (str, float, float, int, int, Func) -> Dict[int]
  """Count the occurence of patterns in a given sequence."""
  count = {}
  length = len(seq)
  for i in range(length * begin // 100, length * end // 100 - dim, step):
    p = pattern(seq[i: i + dim])
    if p in count:
      count[p] += 1
    else:
      count[p] = 1
  return count


def f1(seq):
  # type: (str) -> float
  """F1: Chi-square of the whole sequence."""
  hist = histgram(seq, 0, 100, 1)
  return chisq(hist, 1)


def f2(seq):
  # type: (str) -> float
  """F2: Chi-square of the first quarter sequence."""
  hist = histgram(seq, 0, 30, 1)
  return chisq(hist, 1)


def f3(seq):
  # type: (str) -> float
  """F3: Chi-square of the second quarter sequence."""
  hist = histgram(seq, 23, 53, 1)
  return chisq(hist, 1)


def f4(seq):
  # type: (str) -> float
  """F4: Chi-square of the third quarter sequence."""
  hist = histgram(seq, 47, 77, 1)
  return chisq(hist, 1)


def f5(seq):
  # type: (str) -> float
  """F5: Chi-square of the forth quarter sequence."""
  hist = histgram(seq, 70, 100, 1)
  return chisq(hist, 1)


def f6(seq):
  # type: (str) -> float
  """F6: Count odd-even pairs."""
  hist = histgram(seq, dim=2, pattern=lambda s: (int(s[0]) + int(s[1])) % 2)
  return hist.get(1, 0)


def f7(seq):
  # type: (str) -> int
  """F7: Count two-streaks."""
  hist = histgram(seq, dim=2, pattern=lambda s: s[0] == s[1])
  return hist.get(True, 0)


def f8(seq):
  # type: (str) -> int
  """F8: Count three-streaks."""
  hist = histgram(seq, dim=3, pattern=lambda s: (
      s[0] == s[1] and s[0] == s[2]
  ))
  return hist.get(True, 0)


def f9(seq):
  # type: (str) -> int
  """F9: Count four-streaks."""
  hist = histgram(seq, dim=4, pattern=lambda s: (
      s[0] == s[1] and s[0] == s[2] and s[0] == s[3]
  ))
  return hist.get(True, 0)


def f10(seq):
  # type: (str) -> int
  """F10: Count two-pairs.
  Possible sequences:
  XXYY, XYXY, XYYX
  where X != Y
  """
  hist = histgram(seq, dim=4, pattern=lambda s: (
      (s[0] == s[1] and s[2] == s[3] and s[0] != s[2])  # XXYY
      or (s[0] == s[2] and s[1] == s[3] and s[0] != s[1])  # XYXY
      or (s[0] == s[3] and s[1] == s[2] and s[0] != s[1])  # XYYX
  ))
  return hist.get(True, 0)


def f11(seq):
  # type: (str) -> int
  """F11: Count full houses.
  Possible sequences:
  XXYYY, XYXYY, XYYXY, XYYYX, YXXYY, YXYXY, YXYYX, YYXXY, YYXYX, YYYXX
  where X != Y
  """
  hist = histgram(seq, dim=5, pattern=lambda s: (
      (s[0] == s[1] and s[0] != s[2] and s[2] == s[3] and s[2] == s[4])  # XXYYY
      or (s[0] == s[2] and s[0] != s[1] and s[1] == s[3] and s[1] == s[4])  # XYXYY
      or (s[0] == s[3] and s[0] != s[1] and s[1] == s[2] and s[1] == s[4])  # XYYXY
      or (s[0] == s[4] and s[0] != s[1] and s[1] == s[2] and s[1] == s[3])  # XYYYX
      or (s[1] == s[2] and s[1] != s[0] and s[0] == s[3] and s[0] == s[4])  # YXXYY
      or (s[1] == s[3] and s[1] != s[0] and s[0] == s[2] and s[0] == s[4])  # YXYXY
      or (s[1] == s[4] and s[1] != s[0] and s[0] == s[2] and s[0] == s[3])  # YXYYX
      or (s[2] == s[3] and s[2] != s[0] and s[0] == s[1] and s[0] == s[4])  # YYXXY
      or (s[2] == s[4] and s[2] != s[0] and s[0] == s[1] and s[0] == s[3])  # YYXYX
      or (s[3] == s[4] and s[3] != s[0] and s[0] == s[1] and s[0] == s[2])  # YYYXX
  ))
  return hist.get(True, 0)


def f12(seq):
  # type: (str) -> int
  """F12: Count 3 in 4.
  Possible sequences:
  XXYX, XYXX
  where X != Y
  """
  hist = histgram(seq, dim=4, pattern=lambda s: (
      s[0] == s[3] and (
          (s[0] == s[1] and s[0] != s[2])  # XXYX
          or (s[0] != s[1] and s[0] == s[2])  # XYXX
      )
  ))
  return hist.get(True, 0)


def f13(seq):
  # type: (str) -> int
  """F13: Count 3 in 5.
  Possible sequences:
  XXYZX, XYXZX, XYZXX
  where X != Y and X != Z
  """
  hist = histgram(seq, dim=5, pattern=lambda s: (
      s[0] == s[4] and (
          (s[0] == s[1] and s[0] != s[2] and s[0] != s[3])  # XXYZX
          or (s[0] != s[1] and s[0] == s[2] and s[0] != s[3])  # XYXZX
          or (s[0] != s[1] and s[0] != s[2] and s[0] == s[3])  # XYZXX
      )
  ))
  return hist.get(True, 0)


def f14(seq):
  # type: (str) -> int
  """F14: Count 4 in 6.
  Possible sequences:
  XXXYZX, XXYXZX, XXYZXX, XYXXZX, XYXZXX, XYZXXX
  where X != Y and X != Z
  """
  hist = histgram(seq, dim=6, pattern=lambda s: (
      s[0] == s[5] and (
          (s[0] == s[1] and s[0] == s[2] and s[0] != s[3] and s[0] != s[4])  # XXXYZX
          or (s[0] == s[1] and s[0] != s[2] and s[0] == s[3] and s[0] != s[4])  # XXYXZX
          or (s[0] == s[1] and s[0] != s[2] and s[0] != s[3] and s[0] == s[4])  # XXYZXX
          or (s[0] != s[1] and s[0] == s[2] and s[0] == s[3] and s[0] != s[4])  # XYXXZX
          or (s[0] != s[1] and s[0] == s[2] and s[0] != s[3] and s[0] == s[4])  # XYXZXX
          or (s[0] != s[1] and s[0] != s[2] and s[0] == s[3] and s[0] == s[4])  # XYZXXX
      )
  ))
  return hist.get(True, 0)


def f15(seq):
  # type: (str) -> int
  """F15: Count 4 in 7.
  Possible sequences:
  XXXYZWX, XXYXZWX, XXYZXWX, XXYZWXX, XYXXZWX, XYXZXWX, XYXZWXX, XYZXXWX, XYZXWXX, XYZWXXX
  where X != Y and X != Z and X != W
  """
  hist = histgram(seq, dim=7, pattern=lambda s: (
      s[0] == s[6] and (
          (s[0] == s[1] and s[0] == s[2] and s[0] != s[3] and s[0] != s[4] and s[0] != s[5])  # XXXYZWX
          or (s[0] == s[1] and s[0] != s[2] and s[0] == s[3] and s[0] != s[4] and s[0] != s[5])  # XXYXZWX
          or (s[0] == s[1] and s[0] != s[2] and s[0] != s[3] and s[0] == s[4] and s[0] != s[5])  # XXYZXWX
          or (s[0] == s[1] and s[0] != s[2] and s[0] != s[3] and s[0] != s[4] and s[0] == s[5])  # XXYZWXX
          or (s[0] != s[1] and s[0] == s[2] and s[0] == s[3] and s[0] != s[4] and s[0] != s[5])  # XYXXZWX
          or (s[0] != s[1] and s[0] == s[2] and s[0] != s[3] and s[0] == s[4] and s[0] != s[5])  # XYXZXWX
          or (s[0] != s[1] and s[0] == s[2] and s[0] != s[3] and s[0] != s[4] and s[0] == s[5])  # XYXZWXX
          or (s[0] != s[1] and s[0] != s[2] and s[0] == s[3] and s[0] == s[4] and s[0] != s[5])  # XYZXXWX
          or (s[0] != s[1] and s[0] != s[2] and s[0] == s[3] and s[0] != s[4] and s[0] == s[5])  # XYZXWXX
          or (s[0] != s[1] and s[0] != s[2] and s[0] != s[3] and s[0] == s[4] and s[0] == s[5])  # XYZWXXX
      )
  ))
  return hist.get(True, 0)


def g(dim, seq, pplb, ppub):
  # type: (int, str, float, float) -> float
  """G_d: Chi-square of a d-dimentional sequence."""
  hist = histgram(seq, dim=dim, step=dim)
  df = 6**dim - 1
  lb = chi2.ppf(pplb, df)
  ub = chi2.ppf(ppub, df)
  p = chisq(hist, dim)
  return max(lb - p, p - ub, 0)


def make_error_function(feature_func, alpha, beta, gamma):
  def error_func(x):
    feat = feature_func(x)
    return gamma * max(alpha - feat, feat - beta, 0)

  return error_func


def load_config(ctx, value):
  """Load `ctx.default_map` from a file.
  :param ctx: Click context
  :param value: File name
  :return dict: Loaded config
  """
  config_path = os.path.expanduser(value)
  if not os.path.exists(config_path):
    ctx.default_map = {}
  else:
    with open(config_path) as cfg:
      ctx.default_map = yaml.safe_load(cfg)
  return value


def json_list(ctx, param, value):
  """Load a list from a JSON string.
  :param value: JSON string
  :return list: Loaded list
  """
  if type(value) is str:
    value = json.loads(value)
  if type(value) is not list:
    ctx.fail("Invalid option: %s=%s, which must be list or str." % (param.name, value))
  return value


def main(
        x_str,
        bias_alpha,
        bias_beta,
        bias_gamma,
        valiables):

  feature_funcs = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15]
  errs = [None] + [  # The first element is a placeholder to make index start with 1
      make_error_function(
          feature_funcs[i],
          bias_alpha[i],
          bias_beta[i],
          bias_gamma[i]
      ) for i in range(15)]

  def f(ixs, x):
    return sum(errs[i](x) for i in ixs)

  # x_str = kwargs['file'].readline()
  x = json.loads(x_str)
  validate(x, variable_jsonschema(valiables))

  objs = [f(i, x) for i in [[j for j in range(1, 16)]]]
  cons = [g(d, x, [0.1], [0.9]) for i, d in enumerate([j for j in range(1, 13)])]
  return {
      'objective': None if len(objs) == 0 else objs[0] if len(objs) == 1 else objs,
      'constraint': None if len(cons) == 0 else cons[0] if len(cons) == 1 else cons,
      'error': None
  }


def evaluate(x_str="",
             bias_alpha=[2, 2, 2, 2, 2, 27, 5, 0, 0, 1, 0, 0, 1, 0, 0],
             bias_beta=[5, 5, 5, 5, 5, 30, 8, 1, 0, 3, 0, 1, 2, 0, 0],
             bias_gamma=[3, 3, 3, 3, 3, 1, 1, 3, 10, 4, 4, 4, 4, 4, 4],
             valiables=50):
  try:
    result = main(x_str=x_str,
                  bias_alpha=bias_alpha,
                  bias_beta=bias_beta,
                  bias_gamma=bias_gamma,
                  valiables=valiables)   # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
  except Exception as e:
    result = {
        'objective': None,
        'constraint': None,
        'error': str(e)
    }
  return result


if __name__ == "__main__":
  evaluate()
  sys.exit(1)
