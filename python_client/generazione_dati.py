import os
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM


def init_model():
    return OllamaLLM(
        base_url="http://ollama:11434",
        model="llama3"
    )

def get_prompt_template():
    return PromptTemplate(
        input_variables=["argomento"],
        template="Scrivi il seguente documento: {argomento}, tono professionale, lingua italiana."
    )

def run_chain(prompt, llm, input_data):
    chain = prompt | llm
    return chain.invoke(input_data)

def salva_output(text, filename="outputs/output.txt"):
    os.makedirs("outputs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(text))
    print(f"\n💾 Output salvato in '{filename}'")

def main():
    llm = init_model()
    prompt = get_prompt_template()
    input_data = {"argomento": "Estratto conto"}
    risposta = run_chain(prompt, llm, input_data)
    print("\n🧠 Risposta generata:\n")
    print(risposta)
    salva_output(risposta)

if __name__ == "__main__":
    main()
