from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from typing import TypedDict,Annotated, Optional

class Review(TypedDict):
    summary: Annotated[str,"A consise summary of the review in one line."]
    sarcastic: Annotated[str,"Indicates if the review is sarcastic (yes/no)."]
    pros: Annotated[Optional[list[str]],"A list of the positive aspects, if any present in the review."]
    cons: Annotated[Optional[list[str]],"A list of the negative aspects, if any present in the review."]
    features: Annotated[list[str],"A list of the key features mentioned in the review."]

# Load API key
load_dotenv()

# Initialize model
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model = ChatHuggingFace(llm=llm)
structured_model=model.with_structured_output(Review)
review="""
After using the Samsung Galaxy S26 for some time, it feels like a polished flagship device. It focuses more on refinement, AI features, and performance rather than major design or hardware changes. It is reliable for daily use but not a big leap over previous models.

Key Features
Galaxy AI integration for smart assistance, automation, and editing
Powerful processor (Exynos/Snapdragon depending on region) for fast performance
6.3-inch Dynamic AMOLED display with smooth refresh rate
Triple camera setup (50MP main, ultra-wide, telephoto)
Night photography improvements with AI image processing
4300 mAh battery with fast charging
Premium build with Armor Aluminum and Gorilla Glass Victus 2
Water resistance and durable design
One UI software with long-term updates
Pros
Smooth and fast performance in daily use and gaming
Excellent display quality with bright and vibrant colors
Useful AI features that improve productivity and photos
Compact and premium design, easy to hold
Good low-light camera performance
Reliable for multitasking and heavy apps
Strong build quality and durability
Cons
Camera hardware is not a big upgrade compared to older models
Battery life can feel average with heavy usage
Expensive for the level of improvements
Heating or efficiency issues during intense gaming
Feels like an incremental upgrade rather than a major change
Some users report inconsistent camera results in certain conditions
"""
res=structured_model.invoke(review)
print(res)