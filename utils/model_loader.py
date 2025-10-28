import os 
from dotenv import load_dotenv
from typing import Literal, Optional, Any 
from pydantic import BaseModel, Field 
# from utils.config_loader import load_config 
from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI 
from utils.config_loader import load_config
from langchain_aws import ChatBedrockConverse
from utils.bedrock_profile import _bedrock_via_profile


class ConfigLoader():
    def __init__(self):
         print(f'Loaded config.....')
         self.config=load_config()

    def __getitem__(self,key):
        return self.config[key]
    


class ModelLoader(BaseModel):
    model_provider: Literal['groq','openai','claude_4','claude_4.5'] = 'groq'
    config: Optional[ConfigLoader]=Field(default=None, exclude=True)

    def model_post_init(self,__context: Any)-> None:
        self.config=ConfigLoader()

    class Config:
        arbitrary_types_allowed=True

    def load_llm(self):
        """ 
        Load and return LLM model 
        """
        print('LLM loading...')
        print(f'Loading model from provider: {self.model_provider}')

        if self.model_provider=='groq':
            print('Loading LLM from Groq ....')
            groq_api_key=os.getenv('GROQ_API_KEY')
            model_name=self.config['llm']['groq']['model_name']
            llm=ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider=='openai':
            print('Loading LLM from Azure-OpenAI.....')
            model_name=self.config['llm']['openai']['model_name']
            llm=AzureChatOpenAI(
                azure_deployment=model_name,
                api_key=os.getenv('AZURE_OPENAI_GPT_4O_API_KEY'),
                azure_endpoint=self.config['llm']['openai']['end_point'],
                api_version=self.config['llm']['openai']['api_version']
            )
        elif self.model_provider == 'claude_4':
            print('Loading Claude Sonnet 4 from Amazon Bedrock.....')
            region = self.config['llm']['bedrock'].get('region', os.getenv('AWS_REGION', 'us-east-1'))
            arn    = self.config['llm']['claude_sonnet_4']['inference_profile_ARN']
            llm = _bedrock_via_profile(region, arn)
            return llm
            

        elif self.model_provider == 'claude_4.5':
            print('Loading Claude Sonnet 4.5 from Amazon Bedrock.....')
            arn    = self.config['llm']['claude_sonnet_4.5']['inference_profile_ARN']
            region = self.config['llm']['bedrock'].get('region', os.getenv('AWS_REGION', 'us-east-1'))
            model_id = self.config['llm']['claude_sonnet_4.5']['model_id']  # e.g. "anthropic.claude-3-5-sonnet-20241022-v2:0"
            llm = ChatBedrockConverse(
                # model_id="anthropic.claude-3-5-sonnet-latest-v1:0",
                region_name=region,
                inference_profile_arn=arn
            #     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            #     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            #    # aws_session_token=...,
                # temperature=...,
                # max_tokens=...,
                # other params...
            )
            # llm = _llm_from_bedrock_profile(region, arn)
        return llm


