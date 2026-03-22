"""
Projeto: Análise de Comentários do YouTube com IA

Integrantes:
- Daniel Zou – RA: 10418211
- Danilo Ye – RA: 10417890
- Igor Shirata Duarte – RA: 10418106

Descrição:
Este script faz parte do pipeline do projeto, sendo responsável por uma etapa específica do processamento de dados.

Histórico:
- 20/03/2026 – Danilo – Criação do script
- 21/03/2026 – Daniel – Ajustes e melhorias
- 22/03/2026 – Igor – Revisão final
"""

# file: step_filter.py

import pandas as pd


def main():

    df = pd.read_csv("outputs/videos_clean.csv")

    df = df[df["duration_sec"] >= 60] 

    df = df.sort_values("viewCount", ascending=False)

    df_top50 = df.head(50)

    print(f"Base filtrada: {len(df)} linhas | Top50: {len(df_top50)}")

    df.to_csv("outputs/videos_filtered.csv", index=False, encoding="utf-8-sig")
    df_top50.to_csv("outputs/videos_top50.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()
