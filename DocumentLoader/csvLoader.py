from langchain_community.document_loaders import CSVLoader

loader=CSVLoader(file_path='spam.csv')

data=loader.load()

print(data[0])