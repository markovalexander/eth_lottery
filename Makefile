LOCALHOST ?= http://127.0.0.1
FORK_URL ?= https://eth-mainnet.alchemyapi.io/v2/$(ALCHEMY_KEY)

compile:
	brownie compile

fork-mainnet:
	brownie networks add development mainnet-fork cmd=ganache-cli host=$(LOCALHOST) fork=$(FORK_URL) gas_limit=12000000 accounts=10 mnemonic=brownie port=8545 

testnet-%:
	brownie test --network $(subst testnet-,,$@)

make runnet-%:
	brownie run scripts/deploy.py --network $(subst runnet-,,$@)