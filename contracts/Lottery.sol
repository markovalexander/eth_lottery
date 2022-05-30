// SPDX-License-Identifier: MIT

pragma solidity >=0.8.3;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable, VRFConsumerBase {
    // payable - can recieve money
    address payable[] public participants;
    address payable public lastWinner;
    uint256 public randomResult;

    uint256 entranceFee;

    AggregatorV3Interface internal eth2usdPriceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    event RequestedRandomness(bytes32 requestId);
    uint256 public fee;
    bytes32 public keyHash;

    constructor(
        address _public_price_feed_address,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) VRFConsumerBase(_vrfCoordinator, _link) {
        entranceFee = 50 * (10**18);
        eth2usdPriceFeed = AggregatorV3Interface(_public_price_feed_address);

        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN, "lottery is not open!");
        require(
            msg.value >= getEntranceFee(),
            "Entrance fee is large then sent amount of ETH"
        );
        participants.push(payable(msg.sender)); // msg is an object availiable inside payable methods
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "lottery must be closed!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner reset {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId);

        uint256 winner_idx = randomResult % participants.length;
        lastWinner = participants[winner_idx];
        lastWinner.transfer(address(this).balance);
    }

    function getLatestPrice() internal view returns (uint256) {
        (, int256 price, , , ) = eth2usdPriceFeed.latestRoundData();
        uint8 decimals = eth2usdPriceFeed.decimals();

        uint256 adjustedUSDPrice = uint256(price) * (10**(18 - decimals)); // price * (10 ** 18)
        return adjustedUSDPrice;
    }

    // view is a free value function that makes no change in blockchain
    function getEntranceFee() public view returns (uint256) {
        uint256 adjustedUSDPrice = getLatestPrice();

        // we get here {50 * 10 ** 18} / {x * 10 ** 18} * 10 ** 18 = entranceFee * 10 ** 18
        uint256 priceToEnter = (entranceFee * 10**18) / adjustedUSDPrice;
        return priceToEnter;
    }

    modifier reset() {
        _;
        participants = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "randomness is needed only to calculate winner!"
        );
        require(randomness > 0, "random not found");
        randomResult = randomness;
    }
}
