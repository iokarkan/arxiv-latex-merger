def ket(bra):
    bracket_map = {
        '(': ')',
        '[': ']',
        '{': '}'
    }
    return bracket_map.get(bra)

def find_matching_bracket(s, start, bra="{"):
    open_braces = 1
    for i, c in enumerate(s[start + 1:]):
        if c == bra:
            open_braces += 1
        elif c == ket(bra):
            open_braces -= 1
        if open_braces == 0:
            return start + 1 + i
    return -1