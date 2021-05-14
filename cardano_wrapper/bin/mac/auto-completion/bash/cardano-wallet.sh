_cardano-wallet()
{
    local CMDLINE
    local IFS=$'\n'
    CMDLINE=(--bash-completion-index $COMP_CWORD)

    for arg in ${COMP_WORDS[@]}; do
        CMDLINE=(${CMDLINE[@]} --bash-completion-word $arg)
    done

    COMPREPLY=( $(cardano-wallet "${CMDLINE[@]}") )
}

complete -o filenames -F _cardano-wallet cardano-wallet
