#!/bin/bash
BIN_FILE="/home/solana/.local/share/solana/install/active_release/bin/solana"
currentEpoch=$($BIN_FILE epoch-info | grep 'Epoch:' | awk '{print $2}')
for i in $(eval echo {240..$currentEpoch}); do  solana inflation rewards <VOTE ACCOUNT> --keypair /home/solana/vote-account-keypair.json --rewards-epoch $i; done
