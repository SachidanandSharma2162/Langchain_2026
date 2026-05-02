from langchain_community.document_loaders import PyPDFLoader,PDFPlumberLoader,AmazonTextractPDFLoader,UnstructuredPDFLoader,PyMuPDFLoader

loader=PyPDFLoader("docs.pdf")

docs=loader.load()

print(docs)

print(len(docs))


# simple pdf: PyPDFLoader
# pdf with table: PDFPlumberLoader
# scanned pdf and image: PDFPlumberLoader, AmazonTextractPDFLoader
# want best structure extraction: PyMuPDFLoader