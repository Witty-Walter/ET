from core.llm_manager import get_llm
from core.retriever import two_stage_retrieve
from engines.spec_compliance.schemas import ComplianceScore
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class GeneratedQuestions(BaseModel):
    questions: list[str] = Field(description="List of 3-5 critical questions")

class GeneratedAnswers(BaseModel):
    answers: list[str] = Field(description="Answers to the specific questions")

class EvaluationResult(BaseModel):
    score_pct: float = Field(description="Compliance score between 0.0 and 100.0")
    reasoning: str = Field(description="Explanation for the score")

def evaluate_narrative_compliance(topic: str) -> ComplianceScore:
    """
    Implements Bidirectional QA (QuestEval approach) for narrative text.
    1. Retrieve baseline chunk and submittal chunk.
    2. Generate questions from Baseline.
    3. Answer questions from Submittal.
    4. Score similarity.
    """
    # 1. Retrieve the narrative clauses for the topic
    # In a real app we'd filter by doc_id (baseline vs submittal) but we mock the split here
    # by taking the top 2 results and assuming one is baseline and one is submittal
    relevant_docs = two_stage_retrieve(f"{topic} requirements", k_initial=10, k_final=2)
    
    if len(relevant_docs) < 2:
        return ComplianceScore(
            score_pct=0.0,
            questions=[],
            answers=[],
            reasoning="Not enough documents found to compare baseline and submittal."
        )
        
    baseline_text = relevant_docs[0].page_content
    submittal_text = relevant_docs[1].page_content
    
    llm = get_llm(temperature=0.0)
    
    # 2. Generate questions from Baseline
    q_llm = llm.with_structured_output(GeneratedQuestions)
    q_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an engineering auditor. Generate 3-5 critical questions based on the requirements in this baseline text."),
        ("human", "{text}")
    ])
    q_result = (q_prompt | q_llm).invoke({"text": baseline_text})
    questions = q_result.questions
    
    # 3. Answer questions using Submittal
    a_llm = llm.with_structured_output(GeneratedAnswers)
    a_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the following questions using ONLY the provided submittal text. If the text does not contain the answer, say 'Not found'."),
        ("human", "Submittal Text:\n{text}\n\nQuestions:\n{questions}")
    ])
    a_result = (a_prompt | a_llm).invoke({
        "text": submittal_text,
        "questions": "\n".join([f"- {q}" for q in questions])
    })
    answers = a_result.answers
    
    # 4. Score
    e_llm = llm.with_structured_output(EvaluationResult)
    e_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a strict compliance judge. Review the original baseline requirements and the submittal's answers to the critical questions. Score how well the submittal complies with the baseline on a scale of 0 to 100. Provide your reasoning."),
        ("human", "Baseline Text:\n{baseline}\n\nQuestions Asked:\n{questions}\n\nSubmittal Answers:\n{answers}")
    ])
    
    e_result = (e_prompt | e_llm).invoke({
        "baseline": baseline_text,
        "questions": "\n".join(questions),
        "answers": "\n".join(answers)
    })
    
    return ComplianceScore(
        score_pct=e_result.score_pct,
        questions=questions,
        answers=answers,
        reasoning=e_result.reasoning
    )
