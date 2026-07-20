from backend.services.llm_service import LLMService
from backend.services.search_service import SearchService
from backend.models.rag import RAGResponse, RAGRequest
from backend.models.search import SearchRequest
from backend.utils.prompt_builder import build_prompt
from backend.config import MAX_CHUNKS_PER_DOCUMENT
from collections import defaultdict
import json,re

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

        grouped_results = defaultdict(list)

        for result in search_results:
            grouped_results[result.metadata.file_name].append(result)

        balanced_results = []

        for document_results in grouped_results.values():
            balanced_results.extend(document_results[:MAX_CHUNKS_PER_DOCUMENT])
        balanced_results.sort(key=lambda result: result.distance)

        prompt = build_prompt(
            search_results=balanced_results,
            query=request.query
        )

        response = self.llm_service.generate_response(prompt)

        try:
            match = re.search(r"\{.*\}", response, re.DOTALL)

            if not match:
                raise ValueError("No JSON found.")

            data = json.loads(match.group())

            answer = data["answer"]
            confidence = max(
                0,
                min(100, int(data["confidence"]))
            )

        except Exception:
            answer = response
            confidence = None

        if not request.include_sources:
            return RAGResponse(answer = answer,confidence=confidence)

        return RAGResponse(answer = answer,confidence=confidence,sources = balanced_results)






