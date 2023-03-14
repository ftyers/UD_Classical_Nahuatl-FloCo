"""
TODO: add heuristic checks so we can ensure well-formedness as we make the rule files larger.
"""
from collections import Counter

def validate_retokenisation_file():
    with open("retokenisation.tsv") as f:
        rows = [r.strip("\n").split("\t") for r in f if not r.startswith("#")]
    broken = False
    for row in rows:
        if len(row) != 2:
            continue # prob throw an error
        l, r = row
        l_char_freqs = {ch:f for ch, f in Counter(l).items() if ch not in "¶ "}
        r_char_freqs = {ch:f for ch, f in Counter(r).items() if ch not in "· "}
        if l_char_freqs != r_char_freqs:
            print(l, "\t", r)
            broken = True
    if broken:
        return 0
    else:
        return 1
        

if __name__ == "__main__":
    print("validating retokenisation file...")
    retokenisation_validated = validate_retokenisation_file()
    if retokenisation_validated:
        print("retokenisation.tsv ✅")
    else:
        print("retokenisation.tsv ❌")