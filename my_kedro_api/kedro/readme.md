
kedro app


[1-bootstrap](./docs/1-bootstrap.md)



# kedro concepts

https://docs.kedro.org/en/stable/get_started/kedro_concepts.html#



## data catalog

numerous data catalog class, which allows you to define how yo want your pipeline output to be saved
+ kedro_datasets.json.JSONDataset
+ kedro_datasets.pandas.CSVDataset
+ kedro_datasets.pandas.JSONDataset
+ kedro_datasets.pandas.ParquetDataset
  + what we used in app
+ kedro_datasets.pickle.PickleDataset
  + what we used in app

> can we define a custom dataset?
> + of course. use kedro.io > AbstractDataset to define flexible and powerful custom dataset

https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-2.0.0.post1/api/kedro_datasets.html#module-kedro_datasets


# API doc

[kedro.io](./docs/2-API-doc/kedro-io.md)