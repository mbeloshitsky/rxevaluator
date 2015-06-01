import ast
from copy import deepcopy

class NamesXtractor(ast.NodeTransformer):

	def __init__(self):
		ast.NodeTransformer.__init__(self)
		self.acc = []

	def accumulated(self):
		return self.acc

	def visit_Name(self, node):
		self.acc.append(node.id)

class IoXtractor(ast.NodeTransformer):

	def __init__(self):
		ast.NodeTransformer.__init__(self)
		self.inputs  	= []
		self.outputs 	= []
		self.inputs2 	= [] 

	def io(self):
		if len(self.outputs) != 0:
			return self.inputs, self.outputs
		else:
			return self.inputs2, []

	def visit_Name(self, node):
		self.inputs2.append(node.id)

	def visit_Assign(self, node):
		inv  = NamesXtractor()
		outv = NamesXtractor()
		inv.visit(node.value)
		self.inputs += inv.accumulated()
		for t in node.targets:
			outv.visit(t)
		self.outputs += outv.accumulated()

class ReactiveEvaluator(object):

	def __init__(self):
		self._exprs = []
		self._ctx   = {}


	def evaluate(self, expr_id):
		results = {}
		exprs = [self._exprs[expr_id]]
		while len(exprs) > 0:
			prev = deepcopy(self._ctx)
			for expr in exprs:
				print("Evaluating: %s" % expr[0])
				exec(expr[0], self._ctx)
				exec_res = {}
				for outp in expr[1][1]:
					exec_res[outp] = self._ctx[outp]
				results[expr[2]] = exec_res
			changed = set()
			for k,v in self._ctx.items():
				if k in prev and prev[k] != v:
					changed.add(k)
			exprs = []
			for ex in self._exprs:
				inputs = ex[1][0]
				for inp in inputs:
					if inp in changed:
						exprs.append(ex)
		return results


	def compile(self, expr_str, expr_id=None):
		ioex = IoXtractor()
		ioex.visit(ast.parse(expr_str))
		if expr_id == None:
			expr_id = len(self._exprs)
			self._exprs.append((expr_str, ioex.io(), expr_id))
		else:
			self._exprs[expr_id] = (expr_str, ioex.io(), expr_id)
		return expr_id
