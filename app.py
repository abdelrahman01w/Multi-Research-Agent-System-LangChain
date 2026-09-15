import streamlit as st
import time
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Pipeline",
    page_icon="🗞️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS — warm editorial / print theme ──────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;0,800;1,500&family=Source+Serif+4:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Serif 4', serif;
    color: #2b2620;
}

.stApp {
    background: #f7f2e9;
    background-image:
        repeating-linear-gradient(0deg, rgba(43,38,32,0.015) 0px, rgba(43,38,32,0.015) 1px, transparent 1px, transparent 3px);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem 4rem; max-width: 1180px; }

/* ── Masthead ── */
.masthead {
    border-top: 4px solid #2b2620;
    border-bottom: 1px solid #2b2620;
    padding: 1.4rem 0 1.1rem;
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
}
.masthead-title {
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    font-size: clamp(2.2rem, 4.5vw, 3.4rem);
    letter-spacing: -0.01em;
    color: #1a1712;
}
.masthead-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #a3341f;
    text-align: right;
}
.masthead-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7a7263;
    padding: 0.6rem 0 1.6rem;
    border-bottom: 1px dashed #c9bfa8;
    margin-bottom: 1.8rem;
}

/* ── Section labels ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #a3341f;
    margin: 2rem 0 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #c9bfa8;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: #fffdf8 !important;
    border: 1.5px solid #2b2620 !important;
    border-radius: 2px !important;
    color: #1a1712 !important;
    font-family: 'Source Serif 4', serif !important;
    font-size: 1.15rem !important;
    padding: 0.9rem 1.1rem !important;
    box-shadow: 3px 3px 0 #c9bfa8 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #a3341f !important;
    box-shadow: 3px 3px 0 #a3341f !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #7a7263 !important;
}

/* ── Button ── */
.stButton > button {
    background: #1a1712 !important;
    color: #f7f2e9 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: 1.5px solid #1a1712 !important;
    border-radius: 2px !important;
    padding: 0.95rem 1.5rem !important;
    width: 100%;
    box-shadow: 3px 3px 0 #a3341f !important;
    transition: all 0.12s ease !important;
}
.stButton > button:hover {
    transform: translate(-2px, -2px) !important;
    box-shadow: 5px 5px 0 #a3341f !important;
}
.stButton > button:active {
    transform: translate(1px, 1px) !important;
    box-shadow: 1px 1px 0 #a3341f !important;
}

/* ── Example chips ── */
.chip {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #4a453b;
    background: #efe7d6;
    border: 1px solid #c9bfa8;
    border-radius: 2px;
    padding: 0.35rem 0.7rem;
    margin: 0.2rem 0.35rem 0.2rem 0;
}

/* ── Pipeline status rows ── */
.ledger-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.85rem 0;
    border-bottom: 1px dashed #c9bfa8;
}
.ledger-row:last-child { border-bottom: none; }
.ledger-num {
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    font-size: 1.5rem;
    color: #c9bfa8;
    width: 2.2rem;
    flex-shrink: 0;
}
.ledger-row.running .ledger-num { color: #a3341f; }
.ledger-row.done .ledger-num { color: #3f6b3f; }
.ledger-body { flex: 1; }
.ledger-title {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #1a1712;
}
.ledger-desc {
    font-family: 'Source Serif 4', serif;
    font-style: italic;
    font-size: 0.85rem;
    color: #7a7263;
}
.ledger-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    flex-shrink: 0;
    padding: 0.25rem 0.6rem;
    border-radius: 2px;
    border: 1px solid transparent;
}
.status-waiting { color: #a39d8e; background: #efe7d6; }
.status-running { color: #a3341f; background: #f3e0da; border-color: #a3341f; }
.status-done    { color: #3f6b3f; background: #e2ebe0; border-color: #3f6b3f; }

/* ── Article panels (native bordered containers via st.container key) ── */
.article-kicker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #a3341f !important;
    margin-bottom: 0.6rem;
}

.st-key-report_panel > div,
.st-key-critic_panel > div,
.st-key-raw_search_panel > div,
.st-key-raw_reader_panel > div,
.st-key-empty_panel > div {
    border-radius: 2px !important;
}

.st-key-report_panel {
    background: #fffdf8;
    border: 1.5px solid #2b2620 !important;
    box-shadow: 6px 6px 0 #e3d9c2;
    padding: 0.4rem 0.4rem 1rem;
    margin-top: 0.5rem;
}
.st-key-critic_panel {
    background: #f3efe3;
    border: 1.5px dashed #3f6b3f !important;
    padding: 0.4rem 0.4rem 1rem;
    margin-top: 0.5rem;
}
.st-key-raw_search_panel, .st-key-raw_reader_panel {
    background: #efe7d6;
    border: 1px solid #c9bfa8 !important;
    padding: 0.2rem 0.4rem;
}
.st-key-empty_panel {
    background: #fffdf8;
    border: 1.5px solid #2b2620 !important;
    box-shadow: 6px 6px 0 #e3d9c2;
    padding: 2rem;
    text-align: center;
}

/* ── Force readable text inside every panel, regardless of Streamlit theme ── */
.st-key-report_panel *, .st-key-critic_panel *,
.st-key-raw_search_panel *, .st-key-raw_reader_panel *,
.st-key-empty_panel * {
    color: #2b2620 !important;
}
.st-key-report_panel h1, .st-key-report_panel h2, .st-key-report_panel h3,
.st-key-critic_panel h1, .st-key-critic_panel h2, .st-key-critic_panel h3 {
    color: #1a1712 !important;
    font-family: 'Playfair Display', serif !important;
}
.st-key-report_panel p, .st-key-report_panel li, .st-key-report_panel strong,
.st-key-critic_panel p, .st-key-critic_panel li, .st-key-critic_panel strong {
    font-family: 'Source Serif 4', serif !important;
    line-height: 1.75;
}
.st-key-report_panel a, .st-key-critic_panel a {
    color: #a3341f !important;
}
.st-key-raw_search_panel p, .st-key-raw_reader_panel p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    line-height: 1.65 !important;
    white-space: pre-wrap !important;
}

details {
    background: transparent;
    border: none;
}
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    color: #7a7263 !important;
    cursor: pointer;
}

.stSpinner > div { color: #a3341f !important; }

.footer-note {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a39d8e;
    text-align: center;
    margin-top: 3.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #c9bfa8;
}

@media (max-width: 768px) {
    .block-container { padding: 1rem 1.2rem 3rem; }
    .masthead { flex-direction: column; gap: 0.3rem; }
    .masthead-tag { text-align: left; }
    .article-panel { padding: 1.5rem 1.6rem; }
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a pipeline status row ───────────────────────────────────────
def ledger_row(num, title, desc, state):
    status_map = {
        "waiting": ("NOT STARTED", "status-waiting"),
        "running": ("RUNNING",     "status-running"),
        "done":    ("COMPLETE",    "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    row_cls = state if state in ("running", "done") else ""

    st.markdown(f"""
    <div class="ledger-row {row_cls}">
        <div class="ledger-num">{num}</div>
        <div class="ledger-body">
            <div class="ledger-title">{title}</div>
            <div class="ledger-desc">{desc}</div>
        </div>
        <div class="ledger-status {cls}">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ──────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Masthead ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-title">Research Pipeline</div>
    <div class="masthead-tag">Multi-Agent System &nbsp;·&nbsp; LangChain + Groq</div>
</div>
<div class="masthead-sub">Search agent → Reader agent → Writer chain → Critic chain</div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline status right ──────────────────────────────────
col_input, col_gap, col_ledger = st.columns([5, 0.4, 4])

with col_input:
    st.markdown('<div class="section-label">Research Topic</div>', unsafe_allow_html=True)

    topic = st.text_input(
        "What topic should the agents research?",
        placeholder="e.g. the impact of AI on the job market in 2024",
        key="topic_input",
    )

    run_btn = st.button("Run Research Pipeline →", use_container_width=True)

    st.markdown("""
    <div style="margin-top:1.1rem;">
        <span class="chip">Future of LLMs in the enterprise</span>
        <span class="chip">AI regulation in the EU, 2026</span>
        <span class="chip">Robotics adoption in manufacturing</span>
    </div>
    """, unsafe_allow_html=True)

with col_ledger:
    st.markdown('<div class="section-label">Pipeline Status</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    ledger_row("01", "Search Agent", "Searches the web for relevant sources", s("search"))
    ledger_row("02", "Reader Agent", "Scrapes the most relevant page for full content", s("reader"))
    ledger_row("03", "Writer Chain", "Drafts a structured report from the research", s("writer"))
    ledger_row("04", "Critic Chain", "Scores the report and lists strengths/gaps", s("critic"))


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


if st.session_state.running and not st.session_state.done:

    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search Agent ──
    with st.spinner("Search agent is finding sources…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [
                ("user", f"Find recent, reliable and detailed information about: {topic_val}")
            ]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader Agent ──
    with st.spinner("Reader agent is scraping the top source…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [(
                "user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer Chain ──
    with st.spinner("Writer chain is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic Chain ──
    with st.spinner("Critic chain is scoring the report…"):
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ─────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    if "writer" in r:
        st.markdown('<div class="section-label">Research Report</div>', unsafe_allow_html=True)
        with st.container(border=True, key="report_panel"):
            st.markdown('<div class="article-kicker">Writer Chain Output</div>', unsafe_allow_html=True)
            st.markdown(r["writer"])

        st.download_button(
            label="Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown('<div class="section-label">Critic Feedback</div>', unsafe_allow_html=True)
        with st.container(border=True, key="critic_panel"):
            st.markdown(r["critic"])

    if "search" in r or "reader" in r:
        st.markdown('<div class="section-label">Raw Agent Output</div>', unsafe_allow_html=True)

        if "search" in r:
            with st.expander("Search Agent — raw results"):
                with st.container(border=True, key="raw_search_panel"):
                    st.markdown(r["search"])

        if "reader" in r:
            with st.expander("Reader Agent — raw scraped content"):
                with st.container(border=True, key="raw_reader_panel"):
                    st.markdown(r["reader"])

else:
    with st.container(border=True, key="empty_panel"):
        st.markdown('<div class="article-kicker">Ready</div>', unsafe_allow_html=True)
        st.markdown("Enter a topic above and run the pipeline to see the report here.")


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
    Research Pipeline · Search → Read → Write → Critique · LangChain + Streamlit
</div>
""", unsafe_allow_html=True)