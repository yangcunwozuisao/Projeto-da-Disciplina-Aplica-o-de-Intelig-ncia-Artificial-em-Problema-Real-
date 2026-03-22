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

from pathlib import Path
import pandas as pd

from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.cluster import KMeans


def main():

    SRC = "outputs/dataset_nlp.csv"
    df = pd.read_csv(SRC)

    texts = df["text_short"].fillna("").astype(str).tolist()

    if len(texts) == 0:
        raise SystemExit("Sem textos para tópicos.")

    embedder = SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    embeddings = embedder.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    N = len(texts)

    def bertopic_with_small_dataset(texts, embeddings):

        nn = max(2, min(10, N - 1)) if N > 2 else 2

        umap_model = UMAP(
            n_neighbors=nn,
            n_components=2,
            min_dist=0.0,
            metric="cosine",
            random_state=42,
            low_memory=True,
        )

        mcs = max(2, min(5, N))

        hdb = HDBSCAN(
            min_cluster_size=mcs,
            min_samples=1,
            metric="euclidean",
            cluster_selection_method="eom",
            prediction_data=True,
        )

        topic_model = BERTopic(
            language="multilingual",
            umap_model=umap_model,
            hdbscan_model=hdb,
            min_topic_size=mcs,
            nr_topics="auto",
            calculate_probabilities=False,
            verbose=False,
        )

        topics, probs = topic_model.fit_transform(texts, embeddings)

        return topic_model, topics, probs


    def kmeans_fallback(texts, embeddings, k=2):

        k = min(max(2, k), N)

        km = KMeans(
            n_clusters=k,
            n_init=10,
            random_state=42
        )

        labels = km.fit_predict(embeddings)

        reps = []

        for i in range(N):
            title = df.loc[i, "title"] if "title" in df.columns else ""
            reps.append(title.split()[:3])

        reps = [" ".join(r) if r else "Topic" for r in reps]

        return labels, reps


    try:

        topic_model, topics, probs = bertopic_with_small_dataset(
            texts,
            embeddings
        )

        topic_repr = []

        for t in topics:

            if t == -1:
                topic_repr.append("Other")

            else:
                rep = topic_model.get_topic(t)
                topic_repr.append(rep[0][0] if rep else "Topic")

    except Exception as e:

        print(
            "[warn] BERTopic falhou em N pequeno, aplicando KMeans fallback:",
            e
        )

        topics, topic_repr = kmeans_fallback(texts, embeddings, k=2)


    out = df.copy()

    out["topic_id"] = topics
    out["topic_repr"] = topic_repr

    out.to_csv(
        "outputs/dataset_topics.csv",
        index=False,
        encoding="utf-8-sig"
    )


    try:

        topics_info = topic_model.get_topic_info()

        topics_info.to_csv(
            "outputs/topics_overview.csv",
            index=False,
            encoding="utf-8-sig"
        )

        print(
            f" dataset_topics.csv ({len(out)}) e topics_overview.csv ({len(topics_info)}) salvos"
        )

    except:

        ov = (
            pd.DataFrame({
                "topic_id": topics,
                "topic_repr": topic_repr
            })
            .value_counts(["topic_id", "topic_repr"])
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
        )

        ov.to_csv(
            "outputs/topics_overview.csv",
            index=False,
            encoding="utf-8-sig"
        )

        print(
            f" dataset_topics.csv ({len(out)}) e topics_overview.csv (fallback) salvos"
        )


if __name__ == "__main__":
    main()
