from promptflow import tool
import tiktoken

def getTokens(text: str, model: str):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(text))
    return num_tokens


@tool
def buildRAG(modelName: str, maxOutputTokens: int, startingMessage: str,
                   ragSystemMsg: str, ragChatHistory: list, question: str, results: list[dict[str, str]]) -> int:

    maxTokensForRag = (maxOutputTokens * -1) - getTokens(ragSystemMsg, modelName) - getTokens(startingMessage, modelName) - getTokens(question, modelName)

    for entry in ragChatHistory:
        maxTokensForRag = maxTokensForRag - getTokens(entry['inputs']['question'], modelName)
        maxTokensForRag = maxTokensForRag - getTokens(entry['outputs']['answer'], modelName)

    if modelName == "gpt-35-turbo":
        maxTokensForRag = maxTokensForRag + 4096
    elif modelName == "gpt-35-turbo-16k":
        maxTokensForRag = maxTokensForRag + 16384
    elif modelName == "gpt-4":
        maxTokensForRag = maxTokensForRag + 8192
    elif modelName == "gpt-4-32k":
        maxTokensForRag = maxTokensForRag + 32768
    else:
        raise Exception("Invalid model name")

    snippets = []

    print("Max tokens for RAG: " + str(maxTokensForRag));

    for result in results:
        snippet = "\n\nExcert from '" + result['FileName'] + "': " + result['Text']

        if(getTokens(snippet, modelName) < maxTokensForRag):
            snippets.append(snippet)
            maxTokensForRag = maxTokensForRag - getTokens(snippet, modelName)
        else:
            break

    snippetString = ""
    for snippet in snippets:
        snippetString += snippet
    
    return snippetString
