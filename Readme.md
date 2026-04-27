# LangChain Demos

A collection of demonstrations and examples for working with LangChain, showcasing various language models, chat models, embeddings, and prompt engineering techniques.

## Description

This repository contains practical examples and demos for LangChain, a framework for developing applications powered by language models. It covers chat models (OpenAI, Hugging Face), embeddings (local and API-based), LLMs, and interactive prompt UIs built with Streamlit.

## Features

- **Chat Models**: Examples using OpenAI and Hugging Face models for conversational AI.
- **Embeddings**: Demonstrations of text embeddings for similarity search and document processing.
- **LLMs**: Basic LLM usage examples.
- **Prompt Engineering**: Interactive UI for research paper summarization with customizable styles and lengths.
- **Streamlit Integration**: Web-based interfaces for easy interaction with models.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SachidanandSharma2162/Langchain_2026.git
   cd Langchain_2026
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key_here
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
   ```

## Usage

### Running Individual Demos

- **Chat Models**: Run `python ChatModels/chatmodel_demo.py` for OpenAI examples, or `python ChatModels/huggingface_api_model.py` for Hugging Face API usage.
- **Embeddings**: Explore `EmbeddedModels/` for various embedding techniques, including document similarity projects.
- **LLMs**: Execute `python LLMs/llm_demo.py` for basic LLM interactions.
- **Prompt UI**: Launch the Streamlit app with `streamlit run Prompts/prompt_ui.py` for an interactive research paper summarizer.

### Project Structure

```
├── ChatModels/
│   ├── chatmodel_demo.py          # OpenAI ChatGPT examples
│   ├── huggingface_api_model.py   # Hugging Face API chat model
│   └── huggingface_local_model.py # Local Hugging Face model usage
├── EmbeddedModels/
│   ├── embedding_hf_local.py      # Local Hugging Face embeddings
│   ├── embedding_hf_localdoc.py   # Document embeddings with HF
│   ├── embedding_openai_document.py # OpenAI document embeddings
│   ├── embedding_openai_query.py  # OpenAI query embeddings
│   └── Embedding_Project_Document_Similarity/
│       └── project.py             # Document similarity project
├── LLMs/
│   └── llm_demo.py                # Basic LLM demonstrations
├── Prompts/
│   └── prompt_ui.py               # Streamlit UI for prompt engineering
├── requirements.txt               # Python dependencies
├── test.py                        # General test file
└── README.md                      # This file
```

## Requirements

- Python 3.8+
- API keys for OpenAI and Hugging Face (if using API-based models)
- Internet connection for API calls

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for improvements or additional examples.

## License

This project is open-source. Please check the license file for details.