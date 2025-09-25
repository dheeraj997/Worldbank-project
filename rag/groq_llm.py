import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

class GroqLLM:
    def __init__(self, model_name="gemma2-9b-it", api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GROQ_API_KEY")
        self.llm = ChatGroq(groq_api_key=self.api_key, model_name=model_name, temperature=0.1, max_tokens=1024)

    def generate_response(self, query, context):
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=f"""Use the following context to answer the question concisely.
        Context:
        {context}
        Question: {query}
        Answer:"""
        ).format(context=context, question=query)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content