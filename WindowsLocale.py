import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PyPDF2 import PdfReader
import json
import os
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

#keyaleatoria: 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

def confirmar_chave():
    
    global api_key
    
    api_key = chave_entry.get()
    url = "https://api.openai.com/v1/engines"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        messagebox.showinfo(title = 'Verificador de API', message='Chave API valida. Entrando na aplicação...')
        # print("Chave API válida!")
        janela_chave.destroy()
        return True
    else:
        messagebox.showwarning("Chave API", "Por favor, insira uma chave API válida.")
        return False

# Cria uma nova janela para solicitar a chave de API
janela_chave = tk.Tk()
janela_chave.title("Chave API")
janela_chave.geometry("300x100")

# Cria o campo de entrada para a chave de API
chave_label = tk.Label(janela_chave, text="Insira a chave de API:")
chave_label.pack()

chave_entry = tk.Entry(janela_chave, show='*')
chave_entry.pack()

# Cria o botão para confirmar a chave
confirmar_button = tk.Button(janela_chave, text="Confirmar", command=confirmar_chave)
confirmar_button.pack()

# Inicia o loop de eventos da janela de chave
janela_chave.mainloop()


# Configurar a API da OpenAI
# with open(r"env.json") as f:
#     env = json.load(f)

# api_key = env["api_key"]
os.environ["OPENAI_API_KEY"] = api_key

# Criar a janela principal
janela = tk.Tk()
janela.title("Chat com PDF")
janela.geometry("600x500")

# Função para exibir a pergunta e resposta na tela
def exibir_mensagem(mensagem):
    historico_text.config(state=tk.NORMAL)
    historico_text.insert(tk.END, mensagem + "\n")
    historico_text.see(tk.END)
    historico_text.config(state=tk.DISABLED)

# Função para processar a pergunta e obter a resposta
def processar_pergunta():
    pergunta = pergunta_entry.get()
    if pergunta:
        resposta = obter_resposta(pergunta)
        exibir_mensagem(f"Pergunta: {pergunta}")
        exibir_mensagem(f"Resposta: {resposta}")
        exibir_mensagem("-------------------------------------")
        pergunta_entry.delete(0, tk.END)

# Função para importar o arquivo PDF
def importar_pdf():
    
    global text_splitter
    global raw_text
    
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if caminho_arquivo:
        # Ler o conteúdo do PDF
        leitor_pdf = PdfReader(caminho_arquivo)
        raw_text = ""
        for i, pagina in enumerate(leitor_pdf.pages):
            texto = pagina.extract_text()
            if texto:
                raw_text += texto

        exibir_mensagem("Arquivo PDF importado com sucesso!")
        exibir_mensagem("-------------------------------------")
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function = len,
    )

# Função para obter a resposta usando o modelo ChatGPT
def obter_resposta(pergunta):

    chunks = text_splitter.split_text(raw_text)

    embeddings = OpenAIEmbeddings()

    docsearch = FAISS.from_texts(chunks, embeddings)

    chain = load_qa_chain(OpenAI(model_name="text-davinci-003"), chain_type="stuff")

    docs = docsearch.similarity_search(pergunta)
    answer = chain.run(input_documents=docs, question=pergunta)
    
    if answer != '':
        return answer
    else:
        answer = 'Não foi possivel encontrar a resposta para essa pergunta, reformule ou espere alguns instantes.'
        return answer

# Criar o campo de texto para exibir o histórico de perguntas e respostas
historico_text = tk.Text(janela, height=20, width=100)
historico_text.pack()
historico_text.config(state=tk.DISABLED)

# Criar o botão para importar o arquivo PDF
importar_button = tk.Button(janela, text="Importar PDF", command=importar_pdf)
importar_button.pack()

# Criar um rótulo para o prompt da pergunta
pergunta_label = tk.Label(janela, text="Digite sua pergunta:")
pergunta_label.pack()

# Criar o campo de entrada para a pergunta
pergunta_entry = tk.Entry(janela, width=80)
pergunta_entry.pack()

# Criar o botão para processar a pergunta
pergunta_button = tk.Button(janela, text="Enviar", command=processar_pergunta)
pergunta_button.pack()

# Iniciar o loop de eventos da janela
janela.mainloop()
