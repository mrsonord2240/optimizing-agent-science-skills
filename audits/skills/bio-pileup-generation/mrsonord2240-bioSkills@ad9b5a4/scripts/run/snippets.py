"""Extract the Skill's python code blocks VERBATIM from the copied SKILL.md / usage-guide.md and load their functions.
Nothing is re-typed: functions are exec'd from the markdown text via ast (imports + FunctionDef only, so module-level
example calls such as `counts = allele_counts('input.bam', ...)` are not executed here)."""
import ast, os, re, textwrap

SK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill")


def python_blocks(md):
    txt = open(os.path.join(SK, md), encoding="utf-8").read()
    return re.findall(r"```python\n(.*?)```", txt, flags=re.S)


def load_functions(md):
    """return dict name -> function, from all python blocks of md (later definitions of a name overwrite earlier)."""
    ns = {}
    for blk in python_blocks(md):
        tree = ast.parse(blk)
        keep = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
        mod = ast.Module(body=keep, type_ignores=[])
        exec(compile(mod, md, "exec"), ns)
    import types
    return {k: v for k, v in ns.items() if isinstance(v, types.FunctionType)}


def block_containing(md, needle):
    for b in python_blocks(md):
        if needle in b:
            return b
    raise KeyError(needle)
