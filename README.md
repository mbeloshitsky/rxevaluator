Reactive Evaluator
==================

Simple python class for reactive evaluations (Mathematica like).

```pycon
>>> import rxevaluator
>>> rxeval=rxevaluator.ReactiveEvaluator()
>>> rxeval.compile('a=1')
0
>>> rxeval.compile('b=1')
1
>>> rxeval.compile('c=b+a')
2
>>> rxeval.evaluate(0)
Evaluating: a=1
{0: {'a': 1}}
>>> rxeval.evaluate(1)
Evaluating: b=1
{1: {'b': 1}}
>>> rxeval.evaluate(2)
Evaluating: c=b+a
{2: {'c': 2}}
>>> rxeval.compile('a=12')
3
>>> rxeval.evaluate(0)
Evaluating: a=1
{0: {'a': 1}}
```
