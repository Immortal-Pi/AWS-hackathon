# from fastapi import FastAPI 
# from fastapi.middleware.cors import CORSMiddleware
# from utils.save_to_document import save_document
# from starlette.responses import JSONResponse
# from pydantic import BaseModel 
# from dotenv import load_dotenv 
# from agent.agentic_workflow import Graphbuilder
# from fastapi.responses import JSONResponse 
# import os 

# load_dotenv() 

# app=FastAPI()
# graph=Graphbuilder(model_provider='openai')
# react_app=graph()
# png_graph=react_app.get_graph().draw_mermaid_png()
# with open('my_graph.png','wb') as f:
#     f.write(png_graph)
# print(f'Graph saved as my_graph.png in {os.getcwd()}')
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # set specific origin in prod 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class QueryRequest(BaseModel):
#     question:str 

# @app.post('/query')
# async def query_travel_agent(query:QueryRequest):
#     """ 
#     query from the user end
#     """
#     try:
#         print(query)

        

#         # Assuming request is a pydantic object like {question: 'your text'}
#         messages={'messages':[query.question]}
#         output=react_app.invoke(messages)

#         # print("=== RAW OUTPUT ===")
#         # print(output)
#         # if result is dict with messages
#         if isinstance(output,dict) and 'messages' in output:
#             final_output=output['messages'][-1].content # Last AI response 

#         else:
#             final_output=str(output)

#         print("=== FINAL OUTPUT ===")
#         print(final_output)
#         return {'answer':final_output}
#     except Exception as e:
#         return JSONResponse(status_code=500,content={'error':str(e)})
    

# app.py — AgentCore entrypoint (no FastAPI needed)

import json, os
from dotenv import load_dotenv
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from agent.agentic_workflow import Graphbuilder

load_dotenv()

app = BedrockAgentCoreApp()

# --- build your graph once per container (warm-start friendly) ---
_graph_builder = Graphbuilder(model_provider="openai")
_react_app = _graph_builder()

# Optional: write the graph image (use /tmp on Lambda)
try:
    png = _react_app.get_graph().draw_mermaid_png()
    with open("/tmp/my_graph.png", "wb") as f:
        f.write(png)
    print(f"Graph saved at /tmp/my_graph.png")
except Exception as e:
    print(f"Graph render skipped: {e}")

def _extract_question(payload: dict) -> str:
    """
    Accepts either:
      - {"question": "..."}   (direct invoke)
      - API Gateway proxy event with JSON body containing {"question": "..."}
    """
    # API Gateway (REST/HTTP) proxy event?
    if "body" in payload and isinstance(payload["body"], (str, bytes)):
        try:
            body = json.loads(payload["body"])
        except Exception:
            body = {}
        return body.get("question")

    # Direct invoke (e.g., Lambda test event)
    return payload.get("question")

def _ok(body: dict, status_code: int = 200, cors: bool = True):
    # API Gateway-compatible response
    headers = {"Content-Type": "application/json"}
    if cors:
        headers.update({
            "Access-Control-Allow-Origin": "*",           # tighten in prod
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
        })
    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(body)
    }

@app.entrypoint
def invoke(payload):
    """
    AgentCore entrypoint. Deploy this file as a Lambda function behind API Gateway.
    POST /query with {"question": "..."} will hit this entrypoint.
    """
    try:
        q = _extract_question(payload)
        if not q:
            return _ok({"error": "Missing 'question' in request."}, 400)

        # Your original message format
        messages = {"messages": [q]}
        output = _react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output and output["messages"]:
            final = output["messages"][-1].content
        else:
            final = str(output)

        return _ok({"answer": final})
    except Exception as e:
        # Log full details to CloudWatch; return generic error to client
        print("Error:", repr(e))
        return _ok({"error": str(e)}, 500)
    

if __name__ == "__main__":
    app.run()