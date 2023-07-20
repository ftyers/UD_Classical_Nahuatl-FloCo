from os import system
from pathlib import Path
from sys import argv
import re

word_id_pattern = re.compile("^[0-9]+\t")
misc_norm_pattern = re.compile("Norm=\*[^\|]+")
model_path = "../models/normalization_model__step_11878.pt"
src_filepath = "/tmp/floco_onmt_norm_words.txt"
output_filepath = "/tmp/floco_onmt_norm_out_{booktitle}.preds"


if len(argv) >= 3:
    USE_CACHED_NORMS = True
else:
    USE_CACHED_NORMS = False


translate_cmd = (
    "onmt_translate "
    "-model {model_path} "
    "-src {src_filepath} "
    "-output {output_filepath} "
    "--replace_unk -verbose"
)


def reformat_token_for_onmt(word):
    return " ".join(list(word))


def main(path_to_conllu):
    book = path_to_conllu.split("/")[-1].split(".")[0]
    output_fp = output_filepath.format(booktitle=book)

    with open(path_to_conllu) as f:
        conllu_txt = [line.strip("\n") for line in f.readlines()]
        
    indices_to_norm, word_forms = [], []
    for i, line in enumerate(conllu_txt):
        if re.search(word_id_pattern, line) and ("Norm=*" in line or "AutoNormed=True" in line):
            word_form = line.split("\t")[1]
            indices_to_norm.append(i)
            word_forms.append(word_form)

    with open(src_filepath, "w") as fout:
        fout.write("\n".join(
            [reformat_token_for_onmt(w) for w in word_forms]
        ))
    
    #
    # System call to onmt since its not straightforward to call directly from Python.
    #
    
    if USE_CACHED_NORMS is False or Path.exists(Path(output_fp)) is False:
        translate(output_fp)
    
    with open(output_fp) as f:
        preds = [w.strip("\n").replace(" ", "") for w in f]

    for i, line in enumerate(conllu_txt):
        if i in indices_to_norm:
            pred = preds[indices_to_norm.index(i)]
            split_line = line.split("\t")
            if len(pred) >= len(split_line[1]) * 1.5:
                print(line)
                break
            split_line[-1] = re.sub(
                misc_norm_pattern, f"Norm={pred}|AutoNormed=True", split_line[-1]
            )

            print("\t".join(split_line))
        else:
            print(line)

def translate(output_fpath):
    system(translate_cmd.format(
        model_path=model_path, 
        src_filepath=src_filepath, 
        output_filepath=output_fpath
        )
    )

if __name__ == "__main__":
    path_to_conllu = argv[1]
    main(path_to_conllu)


