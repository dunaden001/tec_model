SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir -p /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R dev_user /commandhistory \
    && echo "$SNIPPET" >> "/home/dev_user/.zshrc"

# This section starts zsh if in an interactive terminal. The check for an interactive
# terminal is important because otherwise it causes the devcontainer build to hang for
# 10 seconds. See link for more info:
# https://github.com/microsoft/vscode-remote-release/issues/6114#issuecomment-1003948271
echo 'if [ -t 1 ]; then
    bash -c zsh
fi'  >> /home/dev_user/.bashrc

echo "
# 'lcl' command alias for running the backend locally for dev/testing/debugging.
alias lcl='/workspaces/drip_backend/stack_tools.sh -s local -c deploy'" >> /home/dev_user/.zshrc


# This is copying the custom dunaden zsh theme into the oh.my.zsh themes dir.
cp .devcontainer/dunaden.zsh-theme /home/dev_user/.oh-my-zsh/themes/dunaden.zsh-theme
# This changes the theme to the dunaden theme.
sed -i -e 's/ZSH_THEME="devcontainers"/ZSH_THEME="dunaden"/g' /home/dev_user/.zshrc

pipx inject poetry poetry-plugin-export
poetry config virtualenvs.in-project true
# Installs the python requirements which are needed for editing Intellisense etc.
# pip3 install -r dev_requirements.txt
poetry lock --no-update
poetry install
