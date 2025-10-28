import os 
from utils.place_info_search import GooglePlaceSearchTool, TaviltyPlaceSearchTool 
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv



class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.google_api_key=os.getenv('GPLACE_API_KEY')
        self.google_places_search=GooglePlaceSearchTool(self.google_api_key)
        self.tavily_search=TaviltyPlaceSearchTool()
        self.place_search_tool_list=self.__setup_tools()

    def __setup_tools(self)-> List:
        """ 
        Setup all tools for the place search tool
        """ 
        @tool 
        def search_housing(place:str)-> str:
           """ 
           Search housing of a place
           """
           try:
               attraction_result=self.google_places_search.google_search_housing(place)
               if attraction_result:
                   return f'Following are the housing of {place} as suggested by google: {attraction_result}'
           except Exception as e:
               tavily_result=self.tavily_search.tavily_search_housing(place)
               return f'Google cannot find the details due to {e}. \n Following are the housing of {place}:{tavily_result}'
           
        @tool 
        def search_restaurents(place:str)->  str:
            """
            Search for restaurents of a place 
            """    
            try:
               restaurent_result=self.google_places_search.google_search_restaurants(place)
               if restaurent_result:
                   return f"Following are the restaurents of {place} as suggested by google: {restaurent_result}"
            except Exception as e:
                tavily_result=self.tavily_search.tavily_search_restaurents(place)
                return f"Google cannot find the details due to {e}. \n Following are the restaurents of {place}:{tavily_result}"
            
        
        @tool
        def search_activities(place:str)-> str:
            """ 
            search activities of a place 
            """
            try:
                activities_result=self.google_places_search.google_search_activity(place)
                if activities_result:
                    return f"Follwing are the activities in and around {place} as suggested by google:{activities_result}"
            except Exception as e:
                tavily_result=self.tavily_search.tavily_search_activity(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the activities of {place}: {tavily_result}"

        @tool
        def search_transportation(place:str)-> str:
            """ 
            Search transportation of a place
            """    
            try:
                transportation_results=self.google_places_search.google_search_transportation(place)
                if transportation_results:
                    return f"Following are the modes of transportation available is {place} as suggested by google: {transportation_results}"
            except Exception as e:
                tavily_results=self.tavily_search.tavily_search_transporation(place)
                return f"Google cannot find the details due to {e}. \n Following are the transportation available in {place}: {tavily_results}"
            
        @tool
        def search_legal_requirements(place:str)->str:
            """ 
            search for legal requirements for user question around the palce
            """
            try:
                legal_results=self.tavily_search.tavily_search_transporation(place)
                if legal_results:
                    return f"Following are the legal advice for {place} as suggested by tavily: {legal_results}"
            except Exception as e:
                legal_results=self.tavily_search.tavily_search_transporation(place)
                return f"Following are the legal advice for {place} as suggested by tavily: {legal_results}"

        return [search_housing,search_restaurents,search_activities,search_transportation,search_legal_requirements]