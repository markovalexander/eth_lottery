from time import sleep
from typing import Optional

from brownie import Lottery, config, network
from brownie.network.contract import ProjectContract
from brownie.network.gas.strategies import GasNowStrategy
from brownie.network.transaction import TransactionReceipt

from src.constants import TEST_NETS
from src.settings import LotterySettings
from src.utils import fund_with_link, get_account, get_contract

lottery_settings = LotterySettings()
gas_strategy = GasNowStrategy('fast')

def deploy_lottery():
    if network.show_active() not in TEST_NETS:
        account = get_account(account_id=lottery_settings.account_id)
        lottery = Lottery.deploy(
            get_contract('eth_usd_price_feed').address,
            get_contract('vrf_coordinator').address,
            get_contract('link_token').address,
            lottery_settings.fee,
            lottery_settings.key_hash,
            {'from': account},
            publish_source=config['networks'][network.show_active()].get('verify', False),
        )
    else:
        lottery = Lottery[-1]
    return lottery

def start_lottery(lottery: Optional[ProjectContract] = None) -> TransactionReceipt:
    account = get_account(account_id=lottery_settings.account_id)

    if lottery is None:
        lottery = Lottery[-1]

    start_lottery_trx = lottery.startLottery({"from": account, 'gas_strategy': gas_strategy})
    start_lottery_trx.wait(1)
    return start_lottery_trx

def enter_lottery(lottery: Optional[ProjectContract] = None) -> TransactionReceipt:
    account = get_account(account_id=lottery_settings.account_id)

    if lottery is None:
        lottery = Lottery[-1]

    value = lottery.getEntranceFee() + 10 ** 8
    entrance_trx = lottery.enter({'from': account, 'value': value, 'gas_strategy': gas_strategy})
    entrance_trx.wait(1)
    return entrance_trx

def end_lottery(lottery: Optional[ProjectContract] = None):
    account = get_account(account_id=lottery_settings.account_id)

    if lottery is None:
        lottery = Lottery[-1]

    # fund the contract
    fund_with_link(lottery.address)

    ending_transaction = lottery.endLottery({"from": account, 'gas_strategy': gas_strategy})
    ending_transaction.wait(1)
    sleep(180)
    print(f"{lottery.lastWinner()} is the new winner!")
