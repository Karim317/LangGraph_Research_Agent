from dotenv import load_dotenv
from .states import GenerateAnalystsState,InterviewState,ResearchGraphState
from typing import Literal     
from langgraph.graph import END 
from langchain_core.messages import AIMessage
from langgraph.types import Send
from langchain_core.messages import HumanMessage

load_dotenv()

def should_continue(state:GenerateAnalystsState)->Literal["create_analyst","dummy"]: 

    human_analyst_feedback=state.get("human_analyst_feedbacck",None)

    if human_analyst_feedback:
        return "create_analyst"

    return "dummy"

def route_messages(state:InterviewState , name: str = "expert"):
     messages= state["messages"]
     max_num_turns= state.get("max_num_turns",2)

     num_responses= len([m for m in messages if isinstance(m, AIMessage) and m.name == name])

     if(num_responses > max_num_turns):
         return"save_interview"

     return "ask_ question"

def initiate_all_messages(state:ResearchGraphState):
    human_analyst_feedback = state.get("human_analyst_feedback")

    if human_analyst_feedback:
        return "create analysts"
    else:
        topic = state["topic"]
        return[
            Send("conduct_interview",{
                "analyst":analyst,
                "messages":[HumanMessage(content=f"so you said you were writing an article on {topic}")]
            })for analyst in state["analysts"]
                ]
