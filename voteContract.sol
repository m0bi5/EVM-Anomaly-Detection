pragma solidity ^0.4.10;
contract StoreVar {

    struct candidate_vote_count {
        uint8 candidate_id;
        uint8 vote_count;
    }

    candidate_vote_count[4] candidates;

    function create_candidates() public {
       for (uint8 i = 0; i < 4; i++) {
           candidates[i].candidate_id = i+1;
           candidates[i].vote_count = 0;
       }
    }

    function get_candidates(uint8 id) public returns (uint8 cid, uint64 votes) {
       return (id,candidates[id].vote_count);
    }

    function cast_vote(uint id) public  {
        candidates[id].vote_count += 1;
    }

}