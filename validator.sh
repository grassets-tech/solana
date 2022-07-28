exec solana-validator \
    --identity ~/validator-keypair.json \
    --vote-account ~/vote-account-keypair.json \
    --ledger ~/validator-ledger \
    --rpc-port 8899 \
    --full-rpc-api \
    --no-untrusted-rpc \
    --dynamic-port-range 11000-11100 \
    --entrypoint entrypoint.mainnet-beta.solana.com:8001 \
    --entrypoint entrypoint2.mainnet-beta.solana.com:8001 \
    --entrypoint entrypoint3.mainnet-beta.solana.com:8001 \
    --entrypoint entrypoint4.mainnet-beta.solana.com:8001 \
    --entrypoint entrypoint5.mainnet-beta.solana.com:8001 \
    --expected-genesis-hash 5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d \
    --wal-recovery-mode skip_any_corrupted_record \
    --limit-ledger-size 50000000 \
    --no-port-check \
    --skip-poh-verify  \
    --full-snapshot-interval-slots 25000 \
    --incremental-snapshots \
    --log ~/solana-validator.log \
    --expected-shred-version 51382 \
    --no-snapshot-fetch \
    --trusted-validator J7oy93PqMNMy6AxWowuWZgaBiLMEW2tzvn4jTzRvKTQ4 \
    --trusted-validator 2uxEHizFmmnLekKG2LZJwxNabhpymEYfdVCpgDxjt87m \
    --trusted-validator E9XZMQKPoWAFw9Q1YckTEN5BF2N1cRaFFkUmkS4u7EMG \
    --trusted-validator EpnKvQsJEfftMXcJPWJBq2fT5SvPuc6NXj154hM92wpz \
    --trusted-validator D6AjfG1PzzzDAubmVoqH4iFHDSvwJbMmPNByvK9jdYRm \
    --trusted-validator 7Np41oeYqPefeNQEHSv1UDhYrehxin3NStELsSKCT4K2 \
    --trusted-validator GdnSyH3YtwcxFvQrVVJMm1JhTS4QVX7MFsX56uJLUfiZ \
    --trusted-validator DE1bawNcRJB9rVm3buyMVfr8mBEoyyu73NBovf2oXJsJ \
    --trusted-validator CakcnaRDHka2gXyfbEd2d3xsvkJkqsLw2akB3zsN1D2S \
