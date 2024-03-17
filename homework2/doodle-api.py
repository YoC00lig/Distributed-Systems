from fastapi import FastAPI
from typing import Dict, List
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

class Poll(BaseModel):
    id: int
    name: str
    question: str

class Vote(BaseModel):
    id: int
    poll_id: int
    answers: List[int]

class PollManagement:
    def __init__(self):
        self.polls: Dict[int, Poll] = {}
        self.votes: Dict[int, Vote] = {}

    def get_poll_by_id(self, poll_id: int):
        if poll_id in self.polls:
            return self.polls[poll_id]
        raise JSONResponse(status_code=404, detail="Poll not found")

    def add_poll(self, poll: Poll):
        self.polls[poll.id] = poll
        return poll

    def update_poll(self, poll_id: int, poll: Poll):
        if poll_id in self.polls:
            self.polls[poll_id] = poll
            return poll
        raise JSONResponse(status_code=404, detail="Poll not found")

    def delete_poll(self, poll_id: int):
        self.votes = {vote_id: vote for vote_id, vote in self.votes.items() if vote.poll_id != poll_id}
        if poll_id in self.polls:
            del self.polls[poll_id]
            return
        raise JSONResponse(status_code=404, detail="Poll not found")

    def get_votes_for_poll(self, poll_id: int):
        return [vote for vote in self.votes.values() if vote.poll_id == poll_id]

    def create_vote(self, vote: Vote):
        for v in vote.answers:
            if v < 0 or v > 5:
                raise JSONResponse(status_code=400, detail="Invalid vote")
        self.votes[vote.id] = vote
        return vote

    def get_vote(self, poll_id: int, vote_id: int):
        if vote_id in self.votes:
            if self.votes[vote_id].poll_id == poll_id:
                return self.votes[vote_id]
        raise JSONResponse(status_code=404, detail="Vote not found")

    def update_vote(self, poll_id:int, vote_id: int, vote: Vote):
        if vote_id in self.votes:
            if self.votes[vote_id].poll_id == poll_id:
                self.votes[vote_id] = vote
                return vote
        raise JSONResponse(status_code=404, detail="Vote not found")

    def delete_vote(self, poll_id: int, vote_id: int):
        if vote_id in self.votes:
            if self.votes[vote_id].poll_id == poll_id:
                del self.votes[vote_id]
                return
        raise JSONResponse(status_code=404, detail="Vote not found")

    def get_results(self, poll_id: int) -> float:
        total_score, num_of_votes = 0, 0
        for vote in self.votes.values():
            if vote.poll_id == poll_id:
                total_score += sum(vote.answers)
                num_of_votes += len(vote.answers)
        return total_score / num_of_votes if num_of_votes != 0 else 0

poll_manager = PollManagement()

@app.get("/poll")
async def get_polls():
    return list(poll_manager.polls.values())

@app.post("/poll")
async def create_poll(poll: Poll):
    return poll_manager.add_poll(poll)

@app.get("/poll/{poll_id}")
async def get_poll(poll_id: int):
    return poll_manager.get_poll_by_id(poll_id)

@app.put("/poll/{poll_id}")
async def update_poll(poll_id: int, poll: Poll):
    return poll_manager.update_poll(poll_id, poll)

@app.delete("/poll/{poll_id}")
async def delete_poll(poll_id: int):
    poll_manager.delete_poll(poll_id)
    return {}

@app.get("/poll/{poll_id}/vote")
async def get_votes(poll_id: int):
    return poll_manager.get_votes_for_poll(poll_id)

@app.post("/poll/{poll_id}/vote")
async def create_vote(vote: Vote):
    return poll_manager.create_vote(vote)

@app.get("/poll/{poll_id}/vote/{vote_id}")
async def get_vote(poll_id: int, vote_id: int):
    return poll_manager.get_vote(poll_id, vote_id)

@app.put("/poll/{poll_id}/vote/{vote_id}")
async def update_vote(poll_id :int, vote_id: int, vote: Vote):
    return poll_manager.update_vote(poll_id, vote_id, vote)

@app.delete("/poll/{poll_id}/vote/{vote_id}")
async def delete_vote(poll_id: int, vote_id: int):
    poll_manager.delete_vote(poll_id, vote_id)
    return {}

@app.get("/poll/{poll_id}/results")
async def get_vote_results(poll_id: int):
    return {"average": poll_manager.get_results(poll_id)}
