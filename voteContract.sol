pragma solidity ^0.4.10;
contract StoreVar {

    uint8 public _myVar;

    function setVar(uint8 _var) public {
        _myVar = _var;
    }

    function getVar() public view returns (uint8) {
        return _myVar;
    }

}