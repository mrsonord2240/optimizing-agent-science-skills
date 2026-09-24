"""Extract the Skill's python code blocks VERBATIM from the copied SKILL.md / usage-guide.md and load their functions.
Nothing is re-typed: functions are exec'd from the markdown text via ast (imports + FunctionDef only, so module-level
example calls such as `counts = allele_counts('input.bam', ...)` are not executed here)."""
import ast, os, re, sys, textwrap

SK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill")


def python_blocks(md):
    txt = open(os.path.join(SK, md), encoding="utf-8").read()
    return re.findall(r"```python\n(.*?)```", txt, flags=re.S)


def load_functions(md):
    """return dict name -> function, from all python blocks of md (later definitions of a name overwrite earlier)."""
    ns = {}
    helpers = os.path.join(SK, "examples")
    if os.path.isfile(os.path.join(helpers, "pileup_helpers.py")):
        sys.path.insert(0, helpers)
    for blk in python_blocks(md):
        tree = ast.parse(blk)
        keep = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
        mod = ast.Module(body=keep, type_ignores=[])
        exec(compile(mod, md, "exec"), ns)
    import types
    functions = {k: v for k, v in ns.items() if isinstance(v, types.FunctionType)}
    # The final source ships its substantial helpers as importable examples
    # rather than duplicating them inline in the Markdown.  Load that exact
    # packaged module for the historical regression harnesses.
    if os.path.isfile(os.path.join(helpers, "pileup_helpers.py")):
        from pileup_helpers import allele_counts, allele_frequency, find_variants, pileup_text
        functions.update({
            "allele_counts": allele_counts,
            "allele_frequency": allele_frequency,
            "find_variants": find_variants,
            "pileup_text": pileup_text,
        })
    return functions


def block_containing(md, needle):
    for b in python_blocks(md):
        if needle in b:
            return b
    raise KeyError(needle)
