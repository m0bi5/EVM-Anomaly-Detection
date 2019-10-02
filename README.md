# EVM Vote Mismatch Detection

## Problem
EVMs are prone to clip on memory manipulatory [1] used to spoof the vote casted. For example, if a voter votes for a candidate A, the EVM registers a vote for another candidate B (choice stored in the clip on memory). Another problem there exists is the use of dishonest displays [1] to fool the voter's choices. For example, the voter may feel like he's casting the vote for candidate A but infact the vote would be registered for another candidate B (party symbol displayed were swapped for both candidates). 

## Solution
Both the above mentioned problems occur due to the difference between the physical press of the button and the registered vote. We propose a mechanism that would record a video of the buttons pressed on the EVM and keep track of the vote count on an immutable database - blockchain. During the time of counting votes, the officials can juxtapose the count from the EVM with the count on the blockchain (fed from video data). This is a simple and effective solution to the problem.

## Approach
A camera will be placed at an optimal position from the EVM to record the position of the finger when the vote is casted. The feed is processed in real time using image processing algorithms (OpenCV). Once the vote is recognised by the algorithm, an API call is made from the microcontroller attached to the camera. A transaction request is sent out to the Azure Blockchain service and the vote is stored in the blockchain. 

[1] https://indiaevm.org/evm_tr2010-jul29.pdf
