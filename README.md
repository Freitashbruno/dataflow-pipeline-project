# Dataflow Pipeline Project

Este repositório contém um projeto de pipeline de dados utilizando Google Cloud Dataflow e Apache Beam.

## Estrutura do Projeto

- `main.py`: Script principal para execução do pipeline.
- `bqscriptv2.py`: Script para processamento de dados com Apache Beam e BigQuery.
- `requirements.txt`: Arquivo de dependências do Python.
- `input_data.txt`: Arquivo de entrada de dados para teste.
- `env/`: Ambiente virtual Python.
- Outros scripts relacionados ao pipeline de dados.

## Como Executar o Projeto

### Pré-requisitos

- Python 3.11
- Apache Beam
- Google Cloud SDK

### Passos para Execução

1. **Criar um Ambiente Virtual e Instalar Dependências**:
    ```sh
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

2. **Executar o Pipeline Localmente**:
    ```sh
    python bqscriptv2.py --input_file input_data.txt --output_path gs://seu_bucket/output --project seu_projeto --region sua_regiao --temp_location gs://seu_bucket/temp --runner DirectRunner
    ```

3. **Desplegar e Executar no Google Cloud Dataflow**:
    ```sh
    gcloud dataflow jobs run nome_do_job --gcs-location gs://seu_bucket/template --region sua_regiao
    ```

## Automatização com Cloud Functions e Cloud Scheduler

### Desplegar Cloud Function

```sh
gcloud functions deploy run_dataflow \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --source gs://seu_bucket/abds.zip \
  --project seu_projeto \
  --region sua_regiao
