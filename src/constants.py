from brownie import LinkTokenMock, MockV3Aggregator, VRFCoordinatorMock

FORKED_LOCAL_CHAINS = ['mainnet-fork', 'mainnet-fork-dev']
TEST_NETS = ['rinkeby', 'kovan']
LOCAL_CHAINS = ['ganache-local', 'development']

CONTRACT_2_MOCK = {
    'eth_usd_price_feed': MockV3Aggregator,
    'vrf_coordinator': VRFCoordinatorMock,
    'link_token':  LinkTokenMock,
}
