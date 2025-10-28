# --- add near your imports in utils/model_loader.py ---
import inspect, json, os, boto3
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

try:
    from langchain_aws import ChatBedrockConverse
    _HAS_CONVERSE = True
except Exception:
    _HAS_CONVERSE = False

def _bedrock_via_profile(region: str, profile_arn: str):
    """Return an LLM that truly uses an Inference Profile ARN, regardless of LC AWS version."""
    # Try ChatBedrockConverse with inference_profile_arn if supported
    if _HAS_CONVERSE and "inference_profile_arn" in inspect.signature(ChatBedrockConverse).parameters:
        return ChatBedrockConverse(region_name=region, inference_profile_arn=profile_arn)

    # Final fallback: minimal adapter using boto3 Converse API with inferenceProfileArn
    bedrock = boto3.client("bedrock-runtime", region_name=region)

    class BedrockProfileChat(BaseChatModel):
        def _generate(self, messages: list[BaseMessage], **kwargs) -> AIMessage:
            system = None
            convo = []
            for m in messages:
                if isinstance(m, SystemMessage):
                    system = m.content
                elif isinstance(m, HumanMessage):
                    convo.append({"role": "user", "content": [{"type": "text", "text": m.content}]})
                else:
                    # treat all other roles as assistant text
                    text = getattr(m, "content", "") or ""
                    convo.append({"role": "assistant", "content": [{"type": "text", "text": text}]})

            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": convo or [{"role": "user", "content": [{"type": "text", "text": "Hello"}]}],
                "max_tokens": 1024,
            }
            if system:
                body["system"] = system

            resp = bedrock.converse(  # converse route supports profiles
                inferenceProfileArn=profile_arn,
                input={"messages": [{"role": m["role"], "content": m["content"]} for m in body["messages"]]},
                additionalModelRequestFields={"anthropic_version": "bedrock-2023-05-31"},
                # You can add guardrails / tool config here if needed
            )
            # Extract text from response (unified format)
            out_msgs = resp.get("output", {}).get("message", {}).get("content", [])
            text = "".join(block.get("text", "") for block in out_msgs if "text" in block)
            return AIMessage(content=text)

        @property
        def _llm_type(self) -> str:
            return "bedrock-profile-chat"

    return BedrockProfileChat()