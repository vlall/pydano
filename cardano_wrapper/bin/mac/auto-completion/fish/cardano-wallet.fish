 function _cardano-wallet
    set -l cl (commandline --tokenize --current-process)
    # Hack around fish issue #3934
    set -l cn (commandline --tokenize --cut-at-cursor --current-process)
    set -l cn (count $cn)
    set -l tmpline --bash-completion-enriched --bash-completion-index $cn
    for arg in $cl
      set tmpline $tmpline --bash-completion-word $arg
    end
    for opt in (cardano-wallet $tmpline)
      if test -d $opt
        echo -E "$opt/"
      else
        echo -E "$opt"
      end
    end
end

complete --no-files --command cardano-wallet --arguments '(_cardano-wallet)'
