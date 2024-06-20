# Coleta de emails e uso de LLM local Ollama.

![Badge](https://img.shields.io/badge/Status-_Desenvolvimento-yellow)
![Badge](https://img.shields.io/badge/Criado_em-_19/06/2024-gree)
![Badge](https://img.shields.io/badge/Lingugem_-Python-blue)

## Informaçãoes Gerais:
Estudo focado em executar localmente uma LLM para conseguir obter informações de arquivos de emails baixado em uma pasta local.

### Tecnologias utilizadas:
- LangChain

- Banco de dados utilizado: ChromaDB

- A LLM usada foi é Ollama com os modelos phi3 (3B), llama2 (7B) e llama3 (8B).
  - com o modelo phi3 os resultados obtidos foram bastantes insatisfatórios,
  - llama2 e llama3 tiver resultados melhores e semelhantes.

### Configuração da máquina utilizada
#### Máquina 1:
- Core i5 13400 
- Mémoria ram 32 GB DDR5
- RTX 4060 8GB
- M.2 de 1TB 4gen
- Sistema Windows 11
#### Máquina 2:
- Core i7 13700
- Mémoria ram 16 GB DDR5
- Intel Graphics (a llm não utiliza)
- M.2 de 256GB 4gen
- Sistema Linux Ubuntu 24.04

## Resultados obtidos
- Quando usado arquivos *.eml* sem processar os anexos e **poucos arquivos** o processamento é "rápido" e as respostas retornadas são mais precisas.
- Quando aumenta a quantidade de arquivos o processo é mais longo e as respostas começam a fazer confusão, que aumenta na medida que adiciona novos arquivos.
- Ao selecionar arquivos de anexos separados como *.pdf* a resposta é mais precisa, mas acontece o mesmo de fazer confusão quando se adiciona mais arquivos para processar.

## Limitações encontradas:
- Com o aumento da quantidade de arquivos, principlamente com anexos, aumenta bastante o tempo de processamento dos dados. Também foi observado que quanto maior os arquivos *.eml* e arquivos *.pdf* grandes, o processo se torna bastante prolongado com resultados confuso.
- Com determinado tipo de arquivos retornaram erros. Arquivos compactados, de imagens, alguns arquivos em pdf (onde o conteúdo é imagem) e outros formatos não suportados. Precisa fazer um tratamento para criar uma exclusão desses formatos e provalvemente criar função para lidar arquivos compactados para extrair os arquivos que possa interessar o usuário.
- Foi observado momentos de "alucinações" ou de "respostas misturadas" com o aumento de novos arquivos na base de dados ja existentes. Também foi observado quando analisado arquivos .eml com conteúdo bem parecidos.

## Trabalhos futuro:
- implementar uma versão utilizando o LlamaIndex com modelos llama3 ou outro com mais paramentos.
- Escolher de um outro banco de dados vetoriais.
- Escolher outra forma de baixar e organizar os arquivos do emails baixados.

## Execução do código:
### Primeiro Passo (instalar as libs)
Instale as libs necessárias para execução correta do código:
```
pip install -r requirements.txt
```

### Segundo Passo (baixar os emails)
Para baixar todos os emails de uma conta do Gmail deve utilizar o *email_gmail.py* (o acesso e processo é por meio do uso da *API do Gmail* e autenticação por *OAUTH 2.0*), mas antes disso deve-se criar, se já não estiver, uma pasta chamada credentials e nela colocar o arquivo de credenciais com o nome: 
```
credentials/.credentials.jon
```

Então, ao executar será soliciatado o ***nome de usuário*** da conta Gmail, onde irá pedir a autenticação e ao final será criada uma pasta chamada token, onde será guardado o arquivo token da conta de cada do usuário.

Logo em seguinda será baixado todo o conteúdo do conta (nesse código não há filtros para selecionar determinados tipo de emails por data, assunto, quantidade e etc) onde ser salvo na pasta ***downloaded_emails***. Os arquivos serão salvo em .eml na pasta ***downloaded_emails/nome_do_usuario/***.
Ao final do processo todos os arquivos estarão salvos.

### Terceiro Passo (processar o conteúdo dos emails)
No terminal execute o seguinte comando: 
```
streamlit run query.py
```
Estão irá abrir uma janela no navegador padrão onde o usuário poderá fazer as perguntas e obter as respostas. O arquivo *query.py* fará a chamada no *base_langchain.py* onde tem a logica do processo de tratar arquivos salvos em uma pasta.
Nessa etapa é um processo mais demorado a depender da configuração do computador.

![image](https://github.com/valderlan/sprint3/assets/71195621/33f26ee3-d44c-424a-909a-ae0112775e01)

![image](https://github.com/valderlan/sprint3/assets/71195621/c99d677d-2f27-461b-afa6-4175db9942d7)




