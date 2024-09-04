from llama_index.core import PromptTemplate

system_prompt=(
    # "You are a assistant whose only goal is to reply to users asking about an SocialBiz ( aka 소셜비즈).\n"
    # "You are friendly able to have normal interactions with the user.\n"
    "You're a friendly agent who answers customer questions  about an SocialBiz ( aka 소셜비즈) based on the contextual information you're given."
)

context_prompt=(
    "Here are the relevant documents for the context given in brackets:\n\n"
    "[{context_str}]"
    "\n\nInstructions:\n"
    "If the answer is not on the above documents, say that the information is not available and do not try to imagine an answer.\n"
    "If the answer is on the above documents, provide detail answer as possible to reply user question below.\n"
    "!!Always include a link to the source and a title where you can read more about the context in the footer of your answer, in a list format of [citation:title](link)."
    "!!The source links you provide must exist in the context."
)

# we don't allow documents under 7 points
choice_select_prompt = PromptTemplate(
    "A list of documents is shown below. Each document has a number next to it along with a summary of the document. "
    "A question is also provided.\n"
    "Respond with the numbers of the documents you should consult to answer the question, in order of relevance, as well as the relevance score. "
    "The relevance score is a number from 1 (low) - 10 (high) based on how relevant you think the document is to the question. Be accurate!\n"
    "Do not include any documents that are not relevant to the question or documents with a score less than 7. \n"
    "Example format: \nDocument 1:\n<summary of document 1>\n\nDocument 2:\n<summary of document 2>\n\n...\n\nDocument 10:\n<summary of document 10>\n"
    "\nQuestion: <question>\nAnswer:\nDoc: 9, Relevance: 7\nDoc: 3, Relevance: 4\nDoc: 7, Relevance: 3\n"
    "\nLet's try this now: \n"
    "{context_str}"
    "\nQuestion: {query_str}"
    "\nAnswer:\n\n"
)


condense_prompt = """
  Given the following conversation between a user and an AI assistant and a follow up question from user,
  rephrase the follow up question to be a standalone question.
  !![ When rephrasing, the language should keep the language of the question ]

  Chat History:
  {chat_history}
  Follow Up Input: {question}
  Standalone question:"""