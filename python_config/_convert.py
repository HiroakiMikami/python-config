from typing import Dict


def convert(config: Dict) -> str:
    out = ""

    def convert_expr(value):
        if isinstance(value, dict) and "type" in value:
            funcname = value["type"]
            out = f"{funcname}("
            for key, value in value.items():
                if key == "type":
                    continue
                out += f"{key}={convert_expr(value)}"
            out += ")"
            return out
        elif isinstance(value, str) and value.startswith("@/"):
            return value[2:]
        elif isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, list):
            return "[" + ", ".join([convert_expr(elt) for elt in value]) + "]"
        elif isinstance(value, dict):
            return "{" + ",".join([
                f"'{key}': {convert_expr(value)}"
                for key, value in value.items()]) + "}"
        return str(value)

    for key, value in config.items():
        out += f"{key} = {convert_expr(value)}\n"
    return out
