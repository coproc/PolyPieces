egrep "^(#|>>>) " README.md | sed "s/^>>> //" > src/README_commands.py
