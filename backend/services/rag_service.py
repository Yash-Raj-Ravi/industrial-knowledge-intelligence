from backend.services.llm_service import LLMService
from backend.services.search_service import SearchService
from backend.models.rag import RAGResponse, RAGRequest
from backend.models.search import SearchRequest
from backend.utils.prompt_builder import build_prompt

class RAGService:
    def __init__(
        self,
        search_service: SearchService,
        llm_service: LLMService,
    ):
        self.search_service = search_service
        self.llm_service = llm_service

    def answer_query(self,request:RAGRequest) -> RAGResponse:
        search_request = SearchRequest(query=request.query,
                                        top_k=request.top_k)
        search_response = self.search_service.search(search_request)
        search_results = search_response.results
        if not search_results:
            return RAGResponse(answer = "No relevant information was found in the indexed documents.")

    # Extract only the retrieved chunk texts for prompt construction.
        chunks = [result.text for result in search_results]
        prompt = build_prompt(chunks=chunks,query=request.query)
        answer = self.llm_service.generate_response(prompt)

        if not request.include_sources:
            return RAGResponse(answer = answer)

        return RAGResponse(answer = answer,sources = search_results)



