// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LilfatfrankDAO is ERC721URIStorage, Ownable {
    
    uint256 public tokenCounter;
    mapping(string => string) public levels;
    mapping(address => uint256) tokens;
    
    constructor()  ERC721("lilfatfrank", "LFF") {
        tokenCounter = 0;
    }

    function setLevels(string memory name, string memory uri) public onlyOwner{
        levels[name] = uri;
    }

    function setURI(uint256 itemno, string memory tokenURI) public onlyOwner{
        _setTokenURI(itemno,tokenURI);
    }

    function createCollectible(string memory tokenURI,address to) public onlyOwner returns (uint256) {
        uint256 newItemid = tokenCounter;
        _safeMint(msg.sender, newItemid);
        _setTokenURI(newItemid,tokenURI);
        safeTransferFrom(msg.sender,to,newItemid);
        tokens[to] = newItemid;
        tokenCounter = tokenCounter + 1;
        return newItemid;
    }

    function getTokennid(address to) public view onlyOwner returns(uint256){
        return tokens[to];
    }

}