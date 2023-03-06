import json
import pickle

def load_retokenization_model():
	"""
	Model is a pickled dict like 
		{"vectorizer": <vectorizer object>, 
		 "model": <scikit-learn Learner>}
	"""
	with open("../models/baseline_newline_glommer.model", "rb") as f:
		return pickle.load(f)


def extract_features_for_instance(char,
                     left_context,
                     right_context,
                     max_affix_lengths=(4, 4)):
    max_prefix_length, max_suffix_length = max_affix_lengths
    left_affixes = [left_context[-a:] for a in range(1, max_prefix_length + 1)]
    right_affixes = [right_context[:a] for a in range(1, max_suffix_length + 1)]
    feature_dict = {f'prefix_{"".join(lc)}': 1 for lc in left_affixes}
    feature_dict.update({f'suffix_{"".join(rc)}': 1 for rc in right_affixes})
    # feature_dict["char"] = char.lower()
    return feature_dict


def create_features_only(original_lines):
    feature_rows = []
    for orig in original_lines:
        for i, och in enumerate(orig):
            if och == "¶":
                left_context = ["<bos>"] + list(orig[:i])
                right_context = (list(orig[i+1:]) if i < (len(orig) - 1) else []) + ["<eos>"]
                feature_dict = extract_features_for_instance(och, left_context, right_context, max_affix_lengths=(5, 5))
                feature_rows.append(feature_dict)

            else:
                continue
    return feature_rows


def retokenize_w_model(spans, text, vectorizer, model, threshold=0.99):
    features = create_features_only([text])
    if not features:
         return spans
    feats = vectorizer.transform(features)
    prob_predictions = model.predict_proba(feats)
    predictions = [1 if p[1] >= threshold else 0 for p in prob_predictions]
    i = 0
    newline_idx = 0
    retokenized = []
    while i < len(spans) - 2:
        token = spans[i]
        next_token = spans[i+1]

        if isinstance(token, dict):
            for subtoken in token["span"]:
                newline_idx += subtoken[0].count("¶")
            retokenized.append(token)

        elif isinstance(token, tuple):
            if token[0].endswith("¶"):
                pred = predictions[newline_idx]
                if pred == 1:
                    if isinstance(next_token, tuple):
                        new_token = {"span": [token, next_token], 
                                     "repl": token[0] + next_token[0]}
                        retokenized.append(new_token)
                        i += 2
                        continue

            retokenized.append(token)
        i += 1
    return retokenized