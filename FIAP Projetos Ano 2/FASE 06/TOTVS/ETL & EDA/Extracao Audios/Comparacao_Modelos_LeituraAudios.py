import os
import time
import importlib
import pandas as pd

# Caminho para os modelos
models_path = r"C:\Users\luish\OneDrive\Área de Trabalho\FIAP\FIAP Projetos Ano 2\FASE 06\TOTVS\ETL & EDA"

# Lista de nomes dos arquivos dos modelos
model_files = [
    "LeituraAudios_ModeloTreino01.py",
    "LeituraAudios_ModeloTreino02.py",
    "LeituraAudios_ModeloTreino03.py"
]

def load_model(file_name):
    """Carrega dinamicamente o módulo do modelo."""
    spec = importlib.util.spec_from_file_location("model", os.path.join(models_path, file_name))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def compare_models(audio_folder_path):
    """Compara a performance dos três modelos."""
    results = []

    for model_file in model_files:
        print(f"Executando modelo: {model_file}")
        model = load_model(model_file)
        
        start_time = time.time()
        try:
            dataset = model.create_dataset_from_audio(audio_folder_path)
            end_time = time.time()
            execution_time = end_time - start_time
            
            results.append({
                "Modelo": model_file,
                "Tempo de Execução (s)": execution_time,
                "Número de Linhas": len(dataset),
                "Colunas": ", ".join(dataset.columns)
            })
            
            # Salva o dataset gerado por cada modelo
            output_file = f"output_{model_file.replace('.py', '.csv')}"
            dataset.to_csv(output_file, index=False)
            print(f"Dataset salvo em: {output_file}")
            
        except Exception as e:
            print(f"Erro ao executar o modelo {model_file}: {str(e)}")
    
    return pd.DataFrame(results)

# Caminho para a pasta com os arquivos de áudio
audio_folder_path = r"C:\Users\luish\OneDrive\Área de Trabalho\FIAP\FIAP Projetos Ano 2\FASE 06\TOTVS\ETL & EDA\audios"

# Executa a comparação
comparison_results = compare_models(audio_folder_path)

# Exibe os resultados
print("\nResultados da Comparação:")
print(comparison_results)

# Salva os resultados em um arquivo CSV
comparison_results.to_csv("comparison_results.csv", index=False)
print("\nResultados da comparação salvos em 'comparison_results.csv'")