import os 
import json 
from langchain_tavily import TavilySearch 
from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper

class GooglePlaceSearchTool:
    def __init__(self,api_key:str):
        self.places_wrapper=GooglePlacesAPIWrapper(gplaces_api_key=api_key)
        self.places_tool =GooglePlacesTool(api_wrapper=self.places_wrapper)

    def google_search_attractions(self,place:str)->dict:
        """
        search for attractions in the specified place using GooglePlaces API
        """
        return self.places_tool.run(f'top attractive places in and around {place}')
    
    def google_search_restaurants(self, place: str)-> dict:
        """ 
        searches for available restaurents in the specified place using Google Places API
        """
        return self.places_tool.run(f'what are the top 10 restaurents and eateries in and around {place}?')
    
    def google_search_activity(self,place:str)-> dict:
        """ 
        searches for popular activites in the specified place using GOoglePlace API
        """
        return self.places_tool.run(f'Activities in and around {place}')
    
    def google_search_transportation(self,place:str)-> dict:
        """ 
        searches for available modes of transportation in the specified place 
        """
        return self.places_tool.run(f'What are the different modes of transportations available in {place}')
    

class TaviltyPlaceSearchTool:
    def __init__(self):
        pass 

    def tavily_search_attractions(self,place:str)-> dict:
        """ 
        Searches for attractions in the specified place using TavilySearch
        """
        tavily_tool=TavilySearch(topic='general',include_answer='advanced')
        result=tavily_tool.invoke({{'query'}: f"top attractive places in and around {place}"})
        if isinstance(result,dict) and result.get('answer'):
            return result['answer']
        return result 
    
    def tavily_search_restaurents(self,place:str)-> dict:
        """ 
        Searches for available restaurents in the specified place using Tavily search
        """
        tavily_tool=TavilySearch(topic='general',include_answer='advanced')
        result=tavily_tool.invoke({'query':f'what are the top 10 restaurents and eateries in and around {place}'})
        if isinstance(result,dict) and result.get('answer'):
            return result['answer']
        return result 
    
    def tavily_search_activity(self,place:str)-> dict:
        """ 
        Searches for popular activities in the specified place using TavilySearch
        """
        tavily_tool=TavilySearch(topic='general',include_answer='advanced')
        result=tavily_tool.invoke({'query':f'activities in and around {place} '})
        if isinstance(result,dict) and result.get('answer'):
            return result['answer']
        return result
    
    def tavily_search_transporation(self,place:str)->dict:
        """ 
        Searches for available modes of transportation in the specified place using TavilySearch
        """
        tavily_tool=TavilySearch(topic='general',include_answer='advanced')
        result=tavily_tool.invoke({'query':f'what are the different modes of transportations avaialbe in {place}'})
        if isinstance(result,dict) and result.get('answer'):
            return result['answer']
        return result
