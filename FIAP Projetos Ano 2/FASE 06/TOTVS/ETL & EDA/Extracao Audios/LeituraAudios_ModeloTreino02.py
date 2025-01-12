import os
import whisper
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import pandas as pd
from datetime import datetime

# Baixar recursos necessários do NLTK
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Carregar o modelo Whisper
model = whisper.load_model("base")

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

def extract_metadata_from_text(text):
    chunks = ne_chunk(pos_tag(word_tokenize(text)))
    
    market = None
    survey_date = None
    customer_name = None
    nps = None

    for chunk in chunks:
        if isinstance(chunk, Tree):
            if chunk.label() == 'GPE':
                market = ' '.join([c[0] for c in chunk])
            elif chunk.label() == 'PERSON':
                customer_name = ' '.join([c[0] for c in chunk])
        elif chunk[1] == 'CD':  # CD tag for cardinal numbers
            if not nps:  # Assume o primeiro número como NPS
                nps = chunk[0]

    # Tentativa de extrair data do texto
    try:
        survey_datetime = pd.to_datetime(text, infer_datetime_format=True)
        month = survey_datetime.strftime('%B')
        quarter = (survey_datetime.month - 1) // 3 + 1
    except:
        survey_datetime = None
        month = None
        quarter = None

    return market, survey_datetime, customer_name, month, quarter, nps

def create_dataset_from_audio(folder_path):
    data = []

    for i, file_name in enumerate(os.listdir(folder_path)):
        if file_name.endswith(".mp3") or file_name.endswith(".wav"):
            file_path = os.path.join(folder_path, file_name)

            # Transcreve o áudio
            transcribed_text = transcribe_audio(file_path)

            # Extrai metadados do texto transcrito
            market, survey_datetime, customer_name, month, quarter, nps = extract_metadata_from_text(transcribed_text)

            # Se não puder extrair a data, usa a data de modificação do arquivo
            if not survey_datetime:
                survey_datetime = datetime.fromtimestamp(os.path.getmtime(file_path))
                month = survey_datetime.strftime('%B')
                quarter = (survey_datetime.month - 1) // 3 + 1

            # Adiciona ao dataset com um ID gerado automaticamente
            data.append([i + 1, market, survey_datetime, customer_name, month, quarter, nps])

    # Cria o DataFrame
    df = pd.DataFrame(data, columns=['ID', 'Market', 'Survey date', 'Customer Name', 'Month', 'Quarter', 'NPS'])
    
    return df

# Caminho da pasta com os arquivos de áudio
folder_path = '/caminho/para/a/pasta/'

# Cria o dataset
dataset = create_dataset_from_audio(folder_path)

# Salva o dataset em um arquivo CSV
dataset.to_csv('dataset_alternativo.csv', index=False)

# Exibe o dataset
print(dataset)