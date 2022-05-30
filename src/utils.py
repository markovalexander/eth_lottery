from typing import Optional

from brownie import LinkTokenMock, MockV3Aggregator, VRFCoordinatorMock, accounts, config, interface, network
from brownie.network.account import Account
from brownie.network.contract import Contract, ProjectContract
from brownie.network.transaction import TransactionReceipt

from src.constants import CONTRACT_2_MOCK, FORKED_LOCAL_CHAINS, LOCAL_CHAINS
from src.settings import LotterySettings, MocksSettings

mock_settings = MocksSettings()
lottery_settings = LotterySettings()

def get_account(account_id: Optional[str] = None, index: int = 0) -> Account:
    if network.show_active() in LOCAL_CHAINS + FORKED_LOCAL_CHAINS:
        return accounts[index]
    if account_id:
        return accounts.load(account_id)

def get_contract(contract_name: str) -> ProjectContract:
    """
        Grab contract address from brownie config or deploy mocked versions
    """
    deployed_contracts = CONTRACT_2_MOCK[contract_name]
    if network.show_active() in LOCAL_CHAINS:
        if len(deployed_contracts) == 0:
            deploy_mocks()

        contract = deployed_contracts[-1]
        return contract

    contract_address = config['networks'][network.show_active()][contract_name]
    contract = Contract.from_abi(deployed_contracts._name, address=contract_address, abi=deployed_contracts.abi)  # pylint: disable=protected-access
    return contract

def deploy_mocks():
    account = get_account(account_id=lottery_settings.account_id)

    MockV3Aggregator.deploy(mock_settings.decimals, mock_settings.initial_value, {'from': account})
    link_token = LinkTokenMock.deploy({'from': account})
    VRFCoordinatorMock.deploy(link_token.address, {'from': account})

def fund_with_link(
    contract_address: str,
    account: Optional[Account] = None,
    link_token: Optional[ProjectContract] = None,
    amount: int = 100000000000000000,
) -> TransactionReceipt:  # 0.1 LINK
    account = account if account else get_account(account_id=lottery_settings.account_id)
    link_token = link_token if link_token else get_contract("link_token")
    link_token_contract = interface.LinkTokenMockInterface(link_token.address)
    tx: TransactionReceipt = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract!")
    return tx
