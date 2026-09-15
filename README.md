# Multi-Agent AI Research System

An end-to-end research assistant built with LangChain, Groq, Tavily, and Streamlit. Enter a research topic and the system searches for relevant sources, reads a selected page, writes a structured report, and evaluates the result with a critic chain.

The project is designed as a small, understandable example of how multiple LLM-powered agents and deterministic processing steps can be composed into a research workflow.

## Features

- Web search through the Tavily Search API
- Search agent that identifies recent and relevant sources
- Reader agent that selects and extracts content from a source URL
- Writer chain that produces a structured research report
- Critic chain that scores the report and identifies strengths and gaps
- Streamlit interface with progress status, raw agent output, and Markdown download
- Terminal entry point for running the pipeline without the UI

## Architecture

```text
User topic
	|
	v
Search Agent -- Tavily web search --> source titles, URLs, and snippets
	|
	v
Reader Agent -- requests + extraction tools --> selected page content
	|
	v
Writer Chain -- Groq LLM --> structured Markdown report
	|
	v
Critic Chain -- Groq LLM --> score, strengths, and improvement areas
```

The Streamlit application stores each stage's output in session state so the intermediate search and reader responses can be inspected after a run.

## Technology

- **Python 3.11**
- **Streamlit** for the web interface
- **LangChain** and **LangChain Core** for agents, tools, prompts, and chains
- **Groq** through `langchain-groq` using the `openai/gpt-oss-20b` model
- **Tavily** for web search
- **Requests** for fetching pages
- **Trafilatura**, **Readability**, **BeautifulSoup**, and **lxml** for content extraction and cleanup
- **python-dotenv** for local environment configuration
- **Rich** for terminal output formatting

## Prerequisites

- Python 3.11 or compatible Python environment
- A [Tavily API key](https://tavily.com/)
- A [Groq API key](https://console.groq.com/)

## Installation

### Conda

```bash
conda create -n multi_agent_research_system python=3.11
conda activate multi_agent_research_system
pip install -r requirements.txt
```

### Python virtual environment

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
```

Keep `.env` out of version control. The application loads these values with `python-dotenv`; do not commit real keys to the repository.

## Usage

### Run the Streamlit application

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, enter a topic, and select **Run Research Pipeline**. The completed report can be downloaded as a Markdown file. The UI also exposes the raw search and scraped-reader output for inspection.

### Run from the terminal

```bash
python main.py
```

The terminal entry point currently runs the example topic defined in `main.py` and prints each stage's output. To research a different topic from the terminal, change the `topic` value in that file or call `run_research_pipeline()` from your own script.

## Project Structure

```text
.
├── app.py                    # Streamlit user interface and UI workflow
├── main.py                   # Terminal example entry point
├── requirements.txt          # Python dependencies
├── src/
│   ├── agents/
│   │   └── agents.py         # Search/reader agents and writer/critic chains
│   ├── pipeline/
│   │   └── pipline.py        # Four-stage research pipeline
│   └── tools/
│       └── tools.py          # Tavily search and web scraping tools
└── README.md
```

## Pipeline Details

1. **Search:** The search agent calls Tavily and returns up to five search results with titles, URLs, and snippets.
2. **Read:** The reader agent chooses a relevant URL and calls `scrape_url()`. The scraper tries Trafilatura first, then Readability/BeautifulSoup, and finally a full-page text fallback.
3. **Write:** The writer chain combines the search results and extracted page content into an introduction, at least three key findings, a conclusion, and a source list.
4. **Critique:** The critic chain reviews the generated report and returns a score, strengths, areas to improve, and a one-line verdict.

## Notes and Limitations

- Results depend on the availability and quality of Tavily search results and the selected source page.
- Some websites block automated requests or render content only with JavaScript, so scraping may fail or return incomplete text.
- Scraped content is capped at 5,000 characters before it is passed to the report workflow.
- The current terminal example uses a hard-coded topic; the Streamlit app is the interactive entry point.
- LLM output should be reviewed against the original sources before being used for high-stakes decisions.

## License

No license has been specified for this project yet. Add a license file before distributing it as an open-source package.