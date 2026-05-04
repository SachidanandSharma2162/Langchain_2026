from langchain_text_splitters import CharacterTextSplitter
from langchain_classic.document_loaders import WebBaseLoader,PyPDFLoader
url='https://en.wikipedia.org/wiki/Cricket'
# loader=WebBaseLoader(url)
loader=PyPDFLoader('../DocumentLoader/docs.pdf')
text=loader.load()
final_text=text[0].page_content

splitter=CharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    separator=''
)

res=splitter.split_text(final_text)

# print(res)
print(len(res))