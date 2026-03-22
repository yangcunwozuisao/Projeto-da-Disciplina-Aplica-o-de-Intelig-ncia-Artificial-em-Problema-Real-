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

# file: brand_entity_extract.py

import re
import pandas as pd
from pathlib import Path


def main():

    SRC = "outputs/dataset_nlp.csv"
    df = pd.read_csv(SRC)

    BRANDS = {
        "samsung": ["samsung", r"\bgalaxy\b", r"\ba\d{2}\b", r"\bs\d{2}\b", r"\bnote\b"],
        "apple": ["apple", r"\biphone\b", r"\bipad\b"],
        "xiaomi": ["xiaomi", r"\bmi\b", r"\bredmi\b", r"\bpoco\b"],
        "motorola": ["motorola", r"\bmoto\b", r"\bmotorola edge\b"],
        "infinix": ["infinix", r"\bnote 40\b", r"\binfinix note\b"],
        "huawei": ["huawei", r"\bmate\b", r"\bp(?:30|40|50|60)\b"],
        "oneplus": ["oneplus", r"\boneplus\b"],
        "oppo": ["oppo", r"\breno\b", r"\bfind\b"],
        "vivo": ["vivo", r"\bvivo v\d+\b"],
        "realme": ["realme", r"\brealme \w+\b"],
        "asus": ["asus", r"\brog\b", r"\bzenfone\b"],
        "google": ["google", r"\bpixel\b"],
        "tecno": ["tecno", r"\bphantom\b", r"\bspark\b"],
        "nothing": ["nothing", r"\bnothing phone\b"],
        "nubia": ["nubia", r"\bredmagic\b"],
        "sony": ["sony", r"\bxperia\b"],
        "nokia": ["nokia", r"\bnokia \w+\b"],
        "lenovo": ["lenovo"]
    }


    def detect_brand(text: str):

        if not isinstance(text, str):
            return None

        t = text.lower()

        for brand, pats in BRANDS.items():
            for p in pats:
                if re.search(p, t):
                    return brand

        return None


    MODEL_PAT = re.compile(
        r"\b(?:a|s)\d{2}\b|\b\d{1,2}\s?(?:pro|ultra|plus|max)\b|\bnote\s?\d{1,2}\b|\bpixel\s?\d{1,2}\b|\brog\b|\bredmagic\b",
        re.IGNORECASE,
    )


    def extract_model(text: str):

        if not isinstance(text, str):
            return None

        m = MODEL_PAT.search(text)

        return m.group(0) if m else None


    source_text = (
        df["title"].fillna("") + " " + df["text_short"].fillna("")
    ).astype(str)


    df["brand"] = source_text.apply(detect_brand)

    df["model_hint"] = source_text.apply(extract_model)


    df_out = df[[
        "videoId",
        "title",
        "channelTitle",
        "language",
        "viewCount",
        "brand",
        "model_hint",
        "keywords",
        "sent_label",
        "sent_value",
        "text_short"
    ]]


    df_out.to_csv(
        "outputs/dataset_brands.csv",
        index=False,
        encoding="utf-8-sig"
    )


    print(f" dataset_brands.csv salvo com {len(df_out)} linhas")


if __name__ == "__main__":
    main()
