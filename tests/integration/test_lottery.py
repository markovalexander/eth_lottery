import time

from src.utils import fund_with_link, get_account


def test_can_pick_winner(check_local_chain, lottery_contract):
    # Arrange (by fixtures)

    account = get_account()
    lottery_contract.startLottery({"from": account})
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    fund_with_link(lottery_contract)
    lottery_contract.endLottery({"from": account})
    time.sleep(60)
    assert lottery_contract.lastWinner() == account
    assert lottery_contract.balance() == 0
