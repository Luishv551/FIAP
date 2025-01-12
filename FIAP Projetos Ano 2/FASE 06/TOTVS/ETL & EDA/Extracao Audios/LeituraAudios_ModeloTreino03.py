import os
import speech_recognition as sr
from pydub import AudioSegment
import pandas as pd
from datetime import datetime
import re
from collections import Counter

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Audio inaudível"
    except sr.RequestError:
        return "Erro na API de reconhecimento de fala"

def extract_metadata_from_text(text):
    words = text.lower().split()
    word_freq = Counter(words)
    
    # Extração simples baseada em frequência de palavras e padrões
    market = next((word for word in words if word in ['market', 'country', 'region']), None)
    customer_name = next((word for word in words if word.istitle() and len(word) > 2), None)
    
    # Tenta encontrar NPS
    nps_match = re.search(r'\b(?:nps\s*(?:score|rating)?:?\s*)?(\d{1,2})(?:/10)?\b', text.lower())
    nps = int(nps_match.group(1)) if nps_match else None
    
    # Tenta extrair data
    date_pattern = r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{2,4}[-/]\d{1,2}[-/]\d{1,2})\b'
    date_match = re.search(date_pattern, text)
    if date_match:
        try:
            survey_datetime = pd.to_datetime(date_match.group(1), dayfirst=True)
            month = survey_datetime.strftime('%B')
            quarter = (survey_datetime.month - 1) // 3 + 1
        except:
            survey_datetime = None
            month = None
            quarter = None
    else:
        survey_datetime = None
        month = None
        quarter = None
    
    return market, survey_datetime, customer_name, month, quarter, nps

def create_dataset_from_audio(folder_path):
    data = []
    temp_wav_path = "temp.wav"

    for i, file_name in enumerate(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        
        if file_name.endswith('.mp3'):
            convert_mp3_to_wav(file_path, temp_wav_path)
            transcribed_text = transcribe_audio(temp_wav_path)
            os.remove(temp_wav_path)
        elif file_name.endswith('.wav'):
            transcribed_text = transcribe_audio(file_path)
        else:
            continue  # Ignora outros tipos de arquivo

        market, survey_datetime, customer_name, month, quarter, nps = extract_metadata_from_text(transcribed_text)

        if not survey_datetime:
            survey_datetime = datetime.fromtimestamp(os.path.getmtime(file_path))
            month = survey_datetime.strftime('%B')
            quarter = (survey_datetime.month - 1) // 3 + 1

        data.append([i + 1, market, survey_datetime, customer_name, month, quarter, nps])

    df = pd.DataFrame(data, columns=['ID', 'Market', 'Survey date', 'Customer Name', 'Month', 'Quarter', 'NPS'])
    return df

# Uso do script
folder_path = '/caminho/para/a/pasta/'
dataset = create_dataset_from_audio(folder_path)
dataset.to_csv('dataset_simples.csv', index=False)
print(dataset)