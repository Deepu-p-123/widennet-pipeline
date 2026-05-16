import os, csv

contracts = [
    {
        "label": 1,
        "solc_version": "0.8.0",
        "source_code": """
pragma solidity ^0.8.0;
contract Reentrancy {
    mapping(address => uint) public balances;
    function deposit() public payable { balances[msg.sender] += msg.value; }
    function withdraw() public {
        uint bal = balances[msg.sender];
        require(bal > 0);
        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent);
        balances[msg.sender] = 0;
    }
}"""
    },
    {
        "label": 1,
        "solc_version": "0.8.0",
        "source_code": """
pragma solidity ^0.8.0;
contract TimestampDep {
    uint public lastWinner;
    function play() public {
        if (block.timestamp % 2 == 0) {
            lastWinner = block.timestamp;
        }
    }
}"""
    },
    {
        "label": 0,
        "solc_version": "0.8.0",
        "source_code": """
pragma solidity ^0.8.0;
contract SafeContract {
    mapping(address => uint) private balances;
    bool private locked;
    modifier noReentrant() {
        require(!locked);
        locked = true;
        _;
        locked = false;
    }
    function deposit() public payable { balances[msg.sender] += msg.value; }
    function withdraw() public noReentrant {
        uint bal = balances[msg.sender];
        require(bal > 0);
        balances[msg.sender] = 0;
        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent);
    }
}"""
    },
    {
        "label": 0,
        "solc_version": "0.8.0",
        "source_code": """
pragma solidity ^0.8.0;
contract SimpleStorage {
    uint private value;
    function set(uint v) public { value = v; }
    function get() public view returns (uint) { return value; }
}"""
    },
    {
        "label": 1,
        "solc_version": "0.8.0",
        "source_code": """
pragma solidity ^0.8.0;
contract VulnBank {
    mapping(address => uint) public bal;
    function deposit() public payable { bal[msg.sender] += msg.value; }
    function withdraw(uint amount) public {
        require(bal[msg.sender] >= amount);
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok);
        bal[msg.sender] -= amount;
    }
}"""
    },
    {
        "label": 0,
        "solc_version": "0.8.0",
        "source_code": """
pragma solidity ^0.8.0;
contract Counter {
    uint public count;
    function increment() public { count += 1; }
    function decrement() public { require(count > 0); count -= 1; }
    function reset() public { count = 0; }
}"""
    },
]

os.makedirs("data", exist_ok=True)
with open("data/contracts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["source_code", "label", "solc_version"])
    writer.writeheader()
    for c in contracts:
        writer.writerow(c)

print(f"Created data/contracts.csv with {len(contracts)} contracts")