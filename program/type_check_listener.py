from listener.SimpleLangListener import SimpleLangListener
from listener.SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def enterMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    pass

  def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]

    if isinstance(left_type, BoolType) or isinstance(right_type, BoolType):
      self.errors.append(f"Cannot use booleans in arithmetic operations: {left_type} {ctx.op.text} {right_type}")
      self.types[ctx] = None
      return

    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for * or /: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
    pass

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]

    if isinstance(left_type, BoolType) or isinstance(right_type, BoolType):
        self.errors.append(f"Cannot use booleans in arithmetic operations: {left_type} {ctx.op.text} {right_type}")
        self.types[ctx] = None
        return

    if isinstance(left_type, StringType) and isinstance(right_type, StringType) and ctx.op.text == '+':
        self.types[ctx] = StringType()
        return

    if not self.is_valid_arithmetic_operation(left_type, right_type):
        self.errors.append(f"Unsupported operand types for + or -: {left_type} and {right_type}")
        self.types[ctx] = None
        return

    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def exitModExpr(self, ctx: SimpleLangParser.ModExprContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
        self.errors.append(f"Unsupported operand types for %: {left_type} and {right_type}")
        self.types[ctx] = None
    else:
        self.types[ctx] = IntType()

  def exitEqExpr(self, ctx: SimpleLangParser.EqExprContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if type(left_type) != type(right_type):
        self.errors.append(f"Cannot compare different types with ==: {left_type} and {right_type}")
        self.types[ctx] = None
    else:
        self.types[ctx] = BoolType()

  def is_valid_arithmetic_operation(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False
