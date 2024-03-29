clear && solana stakes ~/vote-account-keypair.json   ; \
echo "Balance: $(solana balance ~/validator-keypair.json)"   ; \
echo "Balance account: $(solana balance ~/vote-account-keypair.json)"   ; \
solana epoch-info   ; \
solana block-production   | grep -e " Identity\|$(solana-keygen pubkey ~/validator-keypair.json)" ; \
solana validators   | grep -e "Identity\|9FXD1NXrK6xFU8i4gLAgjj2iMEWTqJhSuQN8tQuDfm2e" ; \
echo "running: "$(curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1, "method":"getVersion"}' http://localhost:8899 | jq -r '.result."solana-core"' ); \
echo "installed: "$(solana -V)
