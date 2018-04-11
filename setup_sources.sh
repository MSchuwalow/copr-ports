#!/bin/bash

for spec in */*.spec; do
    d=$(dirname $spec)
    for source in $(spectool --list-files $spec | awk '{print $2}'); do
        sourcebase=$(basename "$source")
        echo "Processing ${sourcebase}"
        #[ -h $d/$sourcebase ] || continue
        git annex whereis "$d/$sourcebase" 2>/dev/null | grep -q " web:" && continue
        git annex addurl --file "$d/$sourcebase" "$source"
    done
done