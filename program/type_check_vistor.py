from visitor.SimpleLangParser import SimpleLangParser
from visitor.SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

  def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))

    if isinstance(left_type, BoolType) or isinstance(right_type, BoolType):
        raise TypeError(f"Cannot use booleans in arithmetic operations: {left_type} {ctx.op.text} {right_type}")

    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

    raise TypeError("Unsupported operand types for * or /: {} and {}".format(left_type, right_type))

  def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))

    if isinstance(left_type, BoolType) or isinstance(right_type, BoolType):
        raise TypeError(f"Cannot use booleans in arithmetic operations: {left_type} {ctx.op.text} {right_type}")

    if isinstance(left_type, StringType) and isinstance(right_type, StringType) and ctx.op.text == '+':
        return StringType()

    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

    raise TypeError(f"Unsupported operand types for {ctx.op.text}: {left_type} and {right_type}")
  
  def visitInt(self, ctx: SimpleLangParser.IntContext):
    return IntType()

  def visitFloat(self, ctx: SimpleLangParser.FloatContext):
    return FloatType()

  def visitString(self, ctx: SimpleLangParser.StringContext):
    return StringType()

  def visitBool(self, ctx: SimpleLangParser.BoolContext):
    return BoolType()

  def visitParens(self, ctx: SimpleLangParser.ParensContext):
    return self.visit(ctx.expr())

  def visitModExpr(self, ctx: SimpleLangParser.ModExprContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))

    if isinstance(left_type, IntType) and isinstance(right_type, IntType):
        return IntType()
    else:
        raise TypeError(f"Unsupported operand types for %: {left_type} and {right_type}")

  def visitEqExpr(self, ctx: SimpleLangParser.EqExprContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))

    if type(left_type) != type(right_type):
        raise TypeError(f"Cannot compare different types with ==: {left_type} and {right_type}")
    return BoolType()
