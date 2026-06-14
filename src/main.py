from src.ingestion.celebrity_ingestor import ingest_celebrity


def main():
    celebrity = "Shah Rukh Khan"
    documents = ingest_celebrity(celebrity)

    print(
        f"Ingested {len(documents)} documents "
        f"for {celebrity}"
    )


if __name__ == "__main__":
    main()