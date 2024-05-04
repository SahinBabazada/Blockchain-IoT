// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DataStorage {
    struct Data {
        address sender;
        string data;
    }

    Data[] public dataList;

    event DataStored(address indexed sender, string data);

    function storeData(string memory _data) external {
        require(bytes(_data).length > 0, "Data cannot be empty"); // Ensure data is not empty

        // Store the data along with the sender's address
        dataList.push(Data(msg.sender, _data));

        // Emit an event to signify data storage
        emit DataStored(msg.sender, _data);
    }

    function getData(uint256 index) external view returns (address, string memory) {
        require(index < dataList.length, "Index out of range");
        return (dataList[index].sender, dataList[index].data);
    }

    function getDataCount() external view returns (uint256) {
        return dataList.length;
    }
}
