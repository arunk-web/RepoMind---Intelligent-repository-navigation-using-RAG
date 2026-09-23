from app.retrieve import retrieve_chunks
from app.llm import get_answer_from_llm
from ragas import evaluate
from ragas.metrics import faithfulness, AnswerRelevancy
from datasets import Dataset
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
import time


load_dotenv()

import os

questions = [
    {
        "question": "How does path generation work?",
        "ground_truth": "The generate_unique_path function creates a random UUID using uuid.uuid4(), converts it to a string, and joins it with the given base path (mainpath) using os.path.join to produce a unique folder path."
        },


    {
        "question": "What does the clone_repository function do?",
        "ground_truth": "The clone_repository function generates a unique local path using generate_unique_path, then uses GitPython's git.Repo.clone_from to clone the given repository URL into that unique path, and returns the final path."
        },

    {
        "question": "How are functions extracted from a Python file?",
        "ground_truth": "The extract_chunk function reads a Python file's content, parses it into an AST using ast.parse, then iterates through the top-level nodes checking for FunctionDef instances. For each function found, it extracts the corresponding source lines using the function's lineno and end_lineno."
    },

    {
        "question": "How are class methods distinguished from standalone functions during chunking?",
        "ground_truth": "When a ClassDef node is found at the top level, the code loops through its body separately to find FunctionDef nodes representing methods, and names them using the format ClassName.method_name, keeping them distinct from standalone functions."
    },
    {
        "question": "What embedding model is used and how are embeddings generated for chunks?",
        "ground_truth": "The project uses the HuggingFace sentence-transformers model BAAI/bge-small-en-v1.5. The generate_embedding_for_chunks function loops through a list of chunks and generates an embedding for each chunk's code using model.encode, storing it back into the chunk dictionary."
    }
]

all_questions = []
all_answers = []
all_contexts = []
all_ground_truth = []

all_retrival_time = []
all_generation_time = []

for items in questions:
    question = items["question"]
    ground_truth = items["ground_truth"]

    start = time.time()
    chunk = retrieve_chunks(question)
    end = time.time()

    retrival_time = end-start

    all_retrival_time.append(retrival_time)

    context = "\n\n".join(chunk["documents"][0])

    start = time.time()
    answer = get_answer_from_llm(question , context)
    end = time.time()

    generation_time = end-start
    all_generation_time.append(generation_time)

    all_questions.append(question)
    all_answers.append(answer)
    all_contexts.append([context])
    all_ground_truth.append(ground_truth)


print("total processed: ", len(all_questions))
print(all_answers[0])



data = {
    "question": all_questions,
    "answer" : all_answers,
    "contexts" : all_contexts,
    "ground_truth" : all_ground_truth
}

dataset = Dataset.from_dict(data)

evaluate_llm = ChatGroq(model="openai/gpt-oss-120b" , api_key=os.getenv("GROQ_API_KEY"));
evaluator_embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
answer_relevancy_metric = AnswerRelevancy(strictness=1)

result = evaluate(dataset , metrics=[faithfulness , answer_relevancy_metric], llm=evaluate_llm, embeddings=evaluator_embeddings)


print(result)
print(all_generation_time)
print(all_retrival_time)

avg_retrival = sum(all_retrival_time)/len(all_retrival_time)
avg_generation = sum(all_generation_time)/len(all_generation_time)

print("avg retrival time:", avg_retrival)
print("avg generation time: " , avg_generation)
print("avg total response: ", avg_generation + avg_retrival)