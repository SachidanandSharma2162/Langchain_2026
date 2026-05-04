from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

text_splitter=SemanticChunker(
    HuggingFaceEmbeddings(),
    breakpoint_threshold_amount=1,
    breakpoint_threshold_type='standard_deviation'
)
text="""
Cricket is a popular sport played between two teams of eleven players each, known for its rich history and global appeal. 

It originated in England and has since become especially popular in countries like India, Australia, and England. 

The game is played on a large field with a rectangular pitch at the center, where one team bats to score runs while the other team bowls and fields to restrict scoring and dismiss players. 

Matches can vary in length, from quick Twenty20 games to traditional Test matches that last up to five days. 

Cricket requires a combination of skill, strategy, teamwork, and patience, making it both exciting to watch and challenging to play."""

res=text_splitter.split_text(text)

print(res)