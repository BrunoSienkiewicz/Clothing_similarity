from datasets import load_dataset


def load_query(query_path: str):
    with open(query_path, 'r') as f:
        return f.read()

class SQLDataset:
    def __init__(self, 
                 db_uri: str,
                 query_path: str, 
                 labels: list, 
                 **kwargs
        ):
        self.db_uri = db_uri
        self.query = load_query(query_path)
        self.labels = labels

        return load_dataset('sql', data_files=self.db_uri, query=self.query, **kwargs)

