from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
from pydantic import BaseModel 
from dotenv import load_dotenv 
from agent.agentic_workflow import Graphbuilder
from fastapi.responses import JSONResponse 
import os 
import uvicorn

load_dotenv() 

app=FastAPI()
graph=Graphbuilder(model_provider='openai')
react_app=graph()
png_graph=react_app.get_graph().draw_mermaid_png()
with open('my_graph.png','wb') as f:
    f.write(png_graph)
print(f'Graph saved as my_graph.png in {os.getcwd()}')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origin in prod 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question:str 

@app.post('/query')
async def query_travel_agent(query:QueryRequest):
    """ 
    query from the user end
    """
    try:
        print(query)

        

        # Assuming request is a pydantic object like {question: 'your text'}
        messages={'messages':[query.question]}
        output=react_app.invoke(messages)

        # print("=== RAW OUTPUT ===")
        # print(output)
        # if result is dict with messages
        if isinstance(output,dict) and 'messages' in output:
            final_output=output['messages'][-1].content # Last AI response 

        else:
            final_output=str(output)

        print("=== FINAL OUTPUT ===")
        print(final_output)
        return {'answer':final_output}
    except Exception as e:
        return JSONResponse(status_code=500,content={'error':str(e)})
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    
