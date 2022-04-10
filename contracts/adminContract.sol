// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract Admin {

    struct DAOdata{
        string name;
        uint256 count;
        address admin;
    }

    mapping(address => DAOdata) public sender;

    function createMember(string memory n, uint256 c, address s) public{
        DAOdata memory data = DAOdata({
            name: n,
            count: c,
            admin: s
        });
        sender[s] = data;
    }
}
