# file: nlp_stage.py

import os
from pathlib import Path
import pandas as pd
from tqdm import tqdm


def main():

    # Carregar bases
    SRC_VIDEOS = "outputs/videos_clean_filtered.csv" if Path("outputs/videos_clean_filtered.csv").exists() else "outputs/videos.csv"
    SRC_TRANS  = "outputs/transcripts.csv"

    if not Path(SRC_TRANS).exists():
        raise FileNotFoundError("transcripts.csv não encontrado. Rode o ASR primeiro.")

    videos = pd.read_csv(SRC_VIDEOS)
    trans  = pd.read_csv(SRC_TRANS)

    # tipos e merge
    videos["viewCount"] = pd.to_numeric(videos.get("viewCount"), errors="coerce")
    trans["text"] = trans["text"].fillna("")
    df = videos.merge(trans[["videoId","language","text"]], on="videoId", how="inner")

    MAX_CHARS = 3000
    df["text_short"] = df["text"].astype(str).str.slice(0, MAX_CHARS)

    print(f"[info] linhas com transcrição: {len(df)} (de {len(videos)} videos)")
    print("[info] amostra de idiomas:", df["language"].value_counts().to_dict())

    # KeyBERT
    from keybert import KeyBERT
    from sentence_transformers import SentenceTransformer

    embedder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    kw_model = KeyBERT(model=embedder)

    def extract_keywords(txt: str, top_n=8):
        if not isinstance(txt, str) or not txt.strip():
            return ""
        try:
            kws = kw_model.extract_keywords(
                txt,
                keyphrase_ngram_range=(1,2),
                stop_words=None,
                use_maxsum=True,
                nr_candidates=24,
                top_n=top_n
            )
            return "; ".join([k for k, _ in kws])
        except Exception:
            return ""

    print("[info] extraindo keywords...")
    tqdm.pandas()
    df["keywords"] = df["text_short"].progress_apply(lambda s: extract_keywords(s, top_n=8))

    # Sentimento
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

    SENT_MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

    tokenizer = AutoTokenizer.from_pretrained(SENT_MODEL, use_fast=False)
    model     = AutoModelForSequenceClassification.from_pretrained(SENT_MODEL)

    clf = pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer,
        truncation=True,
        max_length=512,
        padding="max_length",
        device=-1
    )

    label_map = {
        "LABEL_0": "NEG", "LABEL_1": "NEU", "LABEL_2": "POS",
        "NEG": "NEG", "NEU": "NEU", "POS": "POS"
    }
    val_map = {"NEG": -1, "NEU": 0, "POS": 1}

    def sent_score(txt: str):
        if not isinstance(txt, str) or not txt.strip():
            return {"label":"NEU","score":0.0,"sent_value":0.0}
        out = clf(txt[:4000])[0]
        label = label_map.get(out["label"], "NEU")
        score = float(out["score"])
        return {"label": label, "score": score, "sent_value": val_map[label] * score}

    print("[info] calculando sentimento...")
    sents = df["text_short"].progress_apply(sent_score)
    df["sent_label"] = sents.apply(lambda d: d["label"])
    df["sent_conf"]  = sents.apply(lambda d: d["score"])
    df["sent_value"] = sents.apply(lambda d: d["sent_value"])

    cols_keep = [
        "videoId", "title", "channelTitle", "publishedAt", "duration",
        "viewCount", "commentCount",
        "language", "keywords", "sent_label", "sent_conf", "sent_value",
        "text_short"
    ]

    for c in cols_keep:
        if c not in df.columns:
            df[c] = None

    df_out = df[cols_keep].sort_values("viewCount", ascending=False)

    df_out.to_csv("outputs/dataset_nlp.csv", index=False, encoding="utf-8-sig")

    print(f" salvo dataset_nlp.csv com {len(df_out)} linhas")
    print("   colunas:", cols_keep)


if __name__ == "__main__":
    main()
