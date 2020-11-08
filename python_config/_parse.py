import ast
import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def parse(code: str) -> Dict:
    tree = ast.parse(code)
    assert isinstance(tree, ast.Module)

    def unsupported(value, msg):
        return RuntimeError(f"Unsupported AST ({ast.dump(value)}): {msg}")

    def parse_reference(expr: ast.expr) \
            -> str:
        if isinstance(expr, ast.Name):
            return expr.id
        elif isinstance(expr, ast.BinOp):
            return \
                f"{parse_reference(expr.left)}/{parse_reference(expr.right)}"
        elif isinstance(expr, ast.Attribute):
            return f"{parse_reference(expr.value)}.{expr.attr}"
        raise unsupported(expr,
                          "reference should be Name, BinOp, or Attribute")

    def parse_expr(expr: ast.expr) -> Any:
        if isinstance(expr, ast.Constant):
            return expr.value
        elif isinstance(expr, ast.Num):
            return expr.n
        elif isinstance(expr, ast.Str):
            return expr.s
        elif isinstance(expr, ast.Bytes):
            return expr.s
        elif isinstance(expr, ast.NameConstant):
            return expr.value
        elif isinstance(expr, ast.JoinedStr):
            # TODO
            return "".join(map(str, expr.values))
        elif isinstance(expr, ast.Ellipsis):
            return Ellipsis
        elif isinstance(expr, ast.Name) or \
                isinstance(expr, ast.Attribute) or \
                isinstance(expr, ast.BinOp):
            return f"@/{parse_reference(expr)}"
        elif isinstance(expr, ast.Call):
            if len(expr.args) > 0:
                raise unsupported(expr, "Only keyword arguments are allowed")
            out = {
                kwarg.arg: parse_expr(kwarg.value) for kwarg in expr.keywords
            }
            out["type"] = parse_reference(expr.func)
            return out
        elif isinstance(expr, ast.List):
            return [
                parse_expr(elt) for elt in expr.elts
            ]
        elif isinstance(expr, ast.Dict):
            return {
                parse_expr(key): parse_expr(value)
                for key, value in zip(expr.keys, expr.values)
                if key is not None
            }
        elif isinstance(expr, ast.UnaryOp):
            assert isinstance(expr.op, ast.USub)
            return - parse_expr(expr.operand)
        raise unsupported(expr, "expr should be Constant, Name, or Attribute")

    def parse_stmt(stmt: ast.stmt) -> Tuple[str, Any]:
        if not isinstance(stmt, ast.Assign):
            raise unsupported(stmt, "body should be assignment")
        vars = stmt.targets
        if len(vars) != 1:
            raise unsupported(stmt, "#targets should be 1")
        var = vars[0]
        if not isinstance(var, ast.Name):
            raise unsupported(var, "target should be Name")
        key = var.id
        return key, parse_expr(stmt.value)

    out = {}
    for stmt in tree.body:
        key, value = parse_stmt(stmt)
        out[key] = value
    return out
