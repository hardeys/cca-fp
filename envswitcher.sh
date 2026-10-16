
useClaude() {
    export UV_PROJECT_ENVIRONMENT=.claudeenv
    source .claudeenv/bin/activate
    echo "Using .claudeenv"
}

usePython(){
    export UV_PROJECT_ENVIRONMENT=.pyenv
    source .pyenv/bin/activate
    echo "Using .pyenv"
}

useNone(){
    deactivate 2>/dev/null          # ignore the error if nothing is active
    unset UV_PROJECT_ENVIRONMENT
    echo "No environment active"
}