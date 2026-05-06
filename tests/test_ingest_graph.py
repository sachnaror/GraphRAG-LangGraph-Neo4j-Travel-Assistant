from scripts.ingest_graph import load_graph_dataset, summarize_dataset


def test_graph_dataset_loads_and_validates():
    dataset = load_graph_dataset()
    summary = summarize_dataset(dataset)

    assert summary["airports"] >= 1
    assert summary["routes"] >= 1
    assert summary["flights"] >= 1
    assert summary["users"] >= 1
