import os
import spacy
from pydub import AudioSegment
import speech_recognition as sr
import pandas as pd
from datetime import datetime

# Carrega o modelo de linguagem do spaCy
nlp = spacy.load("en_core_web_sm")

# Função para reconhecer o texto de um arquivo de áudio
def recognize_audio(file_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)
    with audio_file as source:
        audio_data = recognizer.record(source)
    try:
        # Reconhece o texto usando o Google Web Speech API
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "Inaudible"
    except sr.RequestError as e:
        text = f"API Error: {e}"
    return text

# Função para extrair metadados usando NLP
def extract_metadata_from_text(text):
    doc = nlp(text)
    
    market = None
    survey_date = None
    customer_name = None
    nps = None  # Adicionado para reconhecer NPS se disponível

    for ent in doc.ents:
        if ent.label_ == "GPE":  # GPE refere-se a Geopolitical Entity (como países, cidades)
            market = ent.text
        elif ent.label_ == "DATE":
            survey_date = ent.text
        elif ent.label_ == "PERSON":
            customer_name = ent.text
        elif ent.label_ == "CARDINAL":  # Supondo que NPS possa ser um número cardinal mencionado no áudio
            nps = ent.text

    # Tentativa de converter survey_date para um formato de data reconhecível
    try:
        survey_datetime = pd.to_datetime(survey_date)
        month = survey_datetime.strftime('%B')
        quarter = (survey_datetime.month - 1) // 3 + 1
    except:
        survey_datetime = None
        month = None
        quarter = None

    return market, survey_datetime, customer_name, month, quarter, nps

# Função para criar o dataset
def create_dataset_from_audio(folder_path):
    data = []

    for i, file_name in enumerate(os.listdir(folder_path)):
        if file_name.endswith(".mp3") or file_name.endswith(".wav"):
            file_path = os.path.join(folder_path, file_name)

            # Reconhece o áudio
            recognized_text = recognize_audio(file_path)

            # Extrai metadados do texto reconhecido
            market, survey_datetime, customer_name, month, quarter, nps = extract_metadata_from_text(recognized_text)

            # Se não puder extrair a data, tenta usar a data de modificação do arquivo
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
dataset.to_csv('dataset.csv', index=False)

# Exibe o dataset
print(dataset)
