#!/usr/bin/env bash
# install-aliases.sh — Install shell aliases for GB AI Brain commands
set -euo pipefail

ALIAS_FILE="${HOME}/.gb-ai-brain-aliases"

cat > "$ALIAS_FILE" << 'EOF'
# GB AI Brain — shell aliases
# Source this file in your .bashrc / .zshrc:
#   [ -f ~/.gb-ai-brain-aliases ] && source ~/.gb-ai-brain-aliases

alias gb-mcp='install-mcp-servers'
alias gb-skills='install-skills'
alias gb-brain='gb-ai-brain'

# systemd user service shortcuts
alias gb-mcp-status='systemctl --user status gb-mcp-servers.service'
alias gb-mcp-run='systemctl --user start gb-mcp-servers.service'
alias gb-skills-status='systemctl --user status gb-skills.service'
alias gb-skills-run='systemctl --user start gb-skills.service'
alias gb-timers='systemctl --user list-timers "gb-*"'
EOF

echo "Aliases written to $ALIAS_FILE"
echo ""
echo "To activate, add this line to your shell rc file:"
echo "  [ -f ~/.gb-ai-brain-aliases ] && source ~/.gb-ai-brain-aliases"
