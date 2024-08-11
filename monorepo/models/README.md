## Downloads

### Poetry

[Installation instructions](https://python-poetry.org/docs/#installing-with-the-official-installer)

To run this project, you need to install poetry. You can do this by running the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
# optionally add completions
poetry completions bash >> ~/.bash_completion
```

Then, you can install the project dependencies and create a virtual environment by running the following command:

```bash
poetry install
```

### Dataset

The dataset used in this project can be found [here](https://www.kaggle.com/datasets/agrigorev/clothing-dataset-full/data).

## Usage

### Running scripts

You need to activate the virtual environment created by poetry:

```bash
poetry shell
```

Then, you should be able to run scripts.
