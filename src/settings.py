from pydantic import BaseSettings
from web3 import Web3


class LotterySettings(BaseSettings):
    account_id: str = 'testing_acc'
    key_hash: str = '0x2ed0feb3e7fd2022120aa84fab1945545a9f2ffc9076fd6156fa96eaff4c1311'
    fee: int = Web3.toWei(0.1, 'ether')

    class Config:
        env_prefix = 'LOTTERY_'

class MocksSettings(BaseSettings):
    decimals: int = 8
    initial_value: int = 2000 * 10 ** 8

    class Config:
        env_prefix = 'MOCKS_'
