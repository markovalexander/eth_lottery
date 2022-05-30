import pytest
from brownie import network

from src.constants import LOCAL_CHAINS
from src.scripts.lottery import deploy_lottery


@pytest.fixture()
def lottery_contract():
    return deploy_lottery()

@pytest.fixture()
def check_local_chain():
    if network.show_active() not in LOCAL_CHAINS:
        pytest.skip()
