egrep "^(#|>>>) " README.md | sed "s/^>>> //" > src/README.py
