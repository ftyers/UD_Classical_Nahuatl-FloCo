#!/bin/bash

python3 process-codex.py ../books/Book_05_-_The_Omens.txt | python3 tag-codex.py > input.conllu
./cg_wrapper.py parser.cg3 input.conllu output.conllu
