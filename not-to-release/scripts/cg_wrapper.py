#!/usr/bin/env python3

import subprocess
from collections import defaultdict

class ConllSentence:
    def __init__(self, lineno, comments, words):
        self.lineno = lineno
        self.comments = comments
        self.words = words
    def from_text(lineno, lines):
        cm = []
        wd = []
        for line in lines:
            if line.startswith('#'):
                cm.append(line.rstrip())
            else:
                wd.append(line.rstrip().split('\t'))
        return ConllSentence(lineno, cm, wd)
    def to_cg(self):
        def gen_word(wd):
            wform = f'"<{wd[1]}>"'
            ret = []
            for upos in wd[3].split('|'):
                ls = [f'"{wd[2]}"', 'upos:'+upos] # lemma, upos
                if wd[4] != '_':
                    ls.append('xpos:'+wd[4]) # xpos
                if wd[5] != '_':
                    ls += wd[5].split('|') # feats
                if wd[7] != '_':
                    ls.append('@' + wd[7]) # deprel
                if wd[6] == '_':
                    ls.append(f'#{wd[0]}->{wd[0]}') # no head
                else:
                    ls.append(f'#{wd[0]}->{wd[6]}') # head
                ret.append('\t' + ' '.join(ls))
            return wform, ret
        cohorts = {}
        for wd in self.words:
            if not wd[0].isdigit():
                # TODO: empty nodes, tokenization stuff
                continue
            wform, reading = gen_word(wd)
            num = int(wd[0])
            if num in cohorts:
                if cohorts[num][0] != wform:
                    raise ValueError(f'Sentence beginning on line {self.lineno} has inconsistent surface form for token {num}: {cohorts[num][0]} vs {wform}')
                reading = cohorts[num][1] + reading
            cohorts[num] = (wform, reading)
        found = set(cohorts.keys())
        exp = set(range(1, len(cohorts)+1))
        if exp != found:
            miss = exp - found
            if miss:
                raise ValueError(f'Sentence beginning on line {self.lineno} has a gap: word {min(miss)} expected but not found')
            add = found - exp
            raise ValueError(f'Sentence beginning on line {self.lineno} has unexpected word id {min(add)}.')
        ret = []
        for k in sorted(cohorts.keys()):
            ret.append(cohorts[k][0] + '\n' + '\n'.join(cohorts[k][1]))
        return '\n'.join(ret)
    def update_cg(self, lines):
        # TODO: inserted cohorts, changed lemmas, changed surface forms
        new = defaultdict(list)
        for line in lines:
            if not line.startswith('\t'):
                continue
            tags = line.split()
            wid = None
            upos = '_'
            xpos = '_'
            feats = []
            deps = []
            head = '_'
            for t in tags:
                if t.startswith('upos:'):
                    upos = t[5:]
                elif t.startswith('xpos:'):
                    xpos = t[5:]
                elif '=' in t:
                    feats.append(t)
                elif t.startswith('@'):
                    deps.append(t[1:])
                elif '->' in t:
                    wid, head = t[1:].split('->')
                    if head == wid:
                        head = '_'
            new[wid].append([upos, xpos, feats, deps or ['_'], head])
        new_words = []
        done = []
        for wd in self.words:
            if wd[0] not in new:
                new_words.append(wd)
            elif wd[0] in done:
                continue
            else:
                for reading in new[wd[0]]:
                    for dep in reading[3]:
                        new_words.append([
                            wd[0], # ID
                            wd[1], # FORM
                            wd[2], # LEMMA
                            reading[0] or '_', # UPOS
                            reading[1] or '_', # XPOS
                            '|'.join(reading[2]) or '_', # FEATS
                            reading[4] or '_', # HEAD
                            dep or '_', # DEPREL
                            wd[8], # DEPS
                            wd[9], # MISC
                        ])
        self.words = new_words
    def to_conllu(self):
        return '\n'.join(self.comments) + '\n' + '\n'.join('\t'.join(w) for w in self.words) + '\n'

def process(grammar, infile, outfile):
    proc = subprocess.Popen(['vislcg3', '-g', grammar],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            encoding='utf-8')
    startline = 0
    cur = []
    sents = []
    for i, line in enumerate(infile, 1):
        if not line.strip():
            if cur:
                sents.append(ConllSentence.from_text(startline, cur))
                cur = []
        else:
            if not cur:
                startline = i
            cur.append(line)
    if cur:
        sents.append(ConllSentence.from_text(startline, cur))
    text_sents = []
    # TODO: this should work streaming, but something hangs for some reason
    for s in sents:
        text_sents.append(s.to_cg() + '\n<STREAMCMD:FLUSH>')
    out, err = proc.communicate('\n'.join(text_sents))
    for s, o in zip(sents, out.split('<STREAMCMD:FLUSH>')):
        s.update_cg(o.splitlines())
        outfile.write(s.to_conllu() + '\n')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('Run a CG grammar on a CoNLL-U file')
    parser.add_argument('grammar_file', action='store')
    parser.add_argument('input_file',
                        type=argparse.FileType('r', encoding='utf-8'),
                        help='Use - for stdin')
    parser.add_argument('output_file',
                        type=argparse.FileType('w', encoding='utf-8'),
                        help='Use - for stdout')
    args = parser.parse_args()
    process(args.grammar_file, args.input_file, args.output_file)
    args.input_file.close()
    args.output_file.close()
