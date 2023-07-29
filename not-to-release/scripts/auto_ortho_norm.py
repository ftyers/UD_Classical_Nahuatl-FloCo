"""
Run this script whenever you ahve new conllu files and want to re-generate them
with automatic orthographic normalizations from the seq2seq model. You will
need to have OpenNMT-py installed (sorry).

"""
from pathlib import Path
import re
import requests
import os

os.system("sh start_onmt_server.sh")


word_id_pattern = re.compile("^[0-9]+\t")
misc_norm_pattern = re.compile("Norm=\*[^\|]+")


def autonorm(tokens):
	"""
    Automatically normalize orthography for a word
    """
	inp = [{"src": token, "id": i+1} for i, token in enumerate(tokens)]
	response = requests.post(
		"http://127.0.0.1:5000/normalizer/translate", 
		json=inp
	).json()
        
	return [item["tgt"].replace(' ', '') for item in response[0]]


def reformat_token_for_onmt(word):
    return " ".join(list(word))


def main(path_to_conllu):
    book = path_to_conllu.split("/")[-1].split(".")[0]

    with open(path_to_conllu) as f:
        conllu_txt = [line.strip("\n") for line in f.readlines()]
        
    words_to_norm = []
    for line in conllu_txt:
        if re.search(word_id_pattern, line) and ("Norm=*" in line or "AutoNormed=True" in line):
            word_form = line.split("\t")[1]
            words_to_norm.append(reformat_token_for_onmt(word_form))
    if not words_to_norm:
        return []
    normed = autonorm(words_to_norm)

    return_lines = []
    for i, word in enumerate(words_to_norm):
        return_lines.append(f"0\t1\t{word.replace(' ', '')}\t{normed[i]}")

    return return_lines
    
def uniq_norm_list(norm_list):
    seen = set([])
    new_norm_list = []
    for line in norm_list:
        _, _, word, _ = line.split("\t")
        if word in seen:
            continue
        else:
            new_norm_list.append(line)
            seen.update({word})
    return new_norm_list
    

if __name__ == "__main__":
    import glob
    new_norm_entries = []
    for book in glob.glob("../conllu/*conllu"):
        new_norm_entries.extend(main(book))
    
    print("\n".join(uniq_norm_list(new_norm_entries)))



