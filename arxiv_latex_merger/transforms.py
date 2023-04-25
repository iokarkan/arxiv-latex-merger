from typing import List, Optional

def newcommand(definition: str, num_args: int, args: List[str], default: Optional[str] = None) -> str:
    # print(definition)
    # print(num_args)
    # print(args)
    a = num_args
    b = len(args) + 1 if default else len(args)
    try:
        assert a == b
    except:
        raise AssertionError (f"Could not assert {a}=={b} for {definition} newcommand")
    res = definition
    
    if default:
        args = [default] + args
        
    for i, arg in enumerate(args, start=1):
        res = res.replace(f"{{#{i}}}", arg)
        res = res.replace(f"#{i}", arg)
    
    return res

def defcommand(definition: str, num_args: int, args: List[str]) -> str:
    res = definition
    for i, arg in enumerate(args, start=1):
        res = res.replace(f"{{#{i}}}", arg)
        res = res.replace(f"#{i}", arg)
    return res


if __name__ == "__main__":
    assert newcommand("this is #1", 0, []) == "this is #1"
    assert newcommand("this is #1", 1, ["test"]) == "this is test"
    assert newcommand("this is #1 and #2", 1, [], default="default") == "this is default and #2"

    assert newcommand("This is the Wikibook about LaTeX supported by {#1} and {#2}!", 2, ["lots of users", "John Doe"]) == "This is the Wikibook about LaTeX supported by lots of users and John Doe!"
    assert newcommand("This is the Wikibook about LaTeX supported by {#1} and {#2}!", 2, ["John Doe"], default="Wikimedia") == "This is the Wikibook about LaTeX supported by Wikimedia and John Doe!"
    assert newcommand("This is the Wikibook about LaTeX supported by #1 and #2!", 2, ["John Doe"], default="Wikimedia") == "This is the Wikibook about LaTeX supported by Wikimedia and John Doe!"
    
    assert defcommand("\mathbb C", 2, []) == "\mathbb C"
    assert defcommand("\mathbb C", 2, []) == "\mathbb C"
    assert defcommand("\mathbb #1", 2, ["C"]) == "\mathbb C"
    
    assert defcommand("\\psx #1 \\psy #2", 2, ["a", "b"]) == "\\psx a \\psy b"

