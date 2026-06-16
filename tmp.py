from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Flowable

# ── Colour palette ──────────────────────────────────────────────────────────
BRAND     = colors.HexColor("#1A1A2E")   # dark navy
ACCENT    = colors.HexColor("#E94560")   # vivid red
ACCENT2   = colors.HexColor("#0F3460")   # mid blue
LIGHT_BG  = colors.HexColor("#F0F4FF")   # pale lavender
CODE_BG   = colors.HexColor("#1E1E2E")   # dark code bg
CODE_FG   = colors.HexColor("#CDD6F4")   # light text for code
MUTED     = colors.HexColor("#6B7280")   # grey for meta
GREEN     = colors.HexColor("#10B981")
YELLOW    = colors.HexColor("#F59E0B")
PURPLE    = colors.HexColor("#8B5CF6")


class ColorBar(Flowable):
    """A coloured horizontal bar used as section divider."""
    def __init__(self, width, height=4, color=ACCENT):
        super().__init__()
        self.bar_width  = width
        self.bar_height = height
        self.bar_color  = color
        self.width  = width
        self.height = height

    def draw(self):
        self.canv.setFillColor(self.bar_color)
        self.canv.rect(0, 0, self.bar_width, self.bar_height, fill=1, stroke=0)


def build_styles():
    base = getSampleStyleSheet()

    custom = {
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Title"],
            fontSize=32, textColor=colors.white,
            fontName="Helvetica-Bold", spaceAfter=8, alignment=TA_CENTER
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", parent=base["Normal"],
            fontSize=13, textColor=colors.HexColor("#CBD5E1"),
            fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4
        ),
        "toc_title": ParagraphStyle(
            "toc_title", parent=base["Heading1"],
            fontSize=20, textColor=BRAND, fontName="Helvetica-Bold",
            spaceAfter=12, spaceBefore=12
        ),
        "toc_item": ParagraphStyle(
            "toc_item", parent=base["Normal"],
            fontSize=11, textColor=ACCENT2, fontName="Helvetica",
            leftIndent=10, spaceAfter=4
        ),
        "section_title": ParagraphStyle(
            "section_title", parent=base["Heading1"],
            fontSize=18, textColor=colors.white, fontName="Helvetica-Bold",
            spaceBefore=0, spaceAfter=0, alignment=TA_LEFT,
            backColor=BRAND, borderPadding=(8, 10, 8, 10)
        ),
        "subsection": ParagraphStyle(
            "subsection", parent=base["Heading2"],
            fontSize=13, textColor=ACCENT2, fontName="Helvetica-Bold",
            spaceBefore=14, spaceAfter=5, borderPadding=(4, 0, 4, 0)
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"],
            fontSize=10.5, textColor=colors.HexColor("#1F2937"),
            fontName="Helvetica", spaceAfter=6, leading=15, alignment=TA_JUSTIFY
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["Normal"],
            fontSize=10.5, textColor=colors.HexColor("#1F2937"),
            fontName="Helvetica", spaceAfter=4, leading=14,
            leftIndent=16, firstLineIndent=-10,
        ),
        "code": ParagraphStyle(
            "code", parent=base["Normal"],
            fontSize=8.5, textColor=CODE_FG, fontName="Courier",
            backColor=CODE_BG, spaceAfter=0, spaceBefore=0,
            leftIndent=8, rightIndent=8, leading=13,
            borderPadding=(6, 6, 6, 6)
        ),
        "code_label": ParagraphStyle(
            "code_label", parent=base["Normal"],
            fontSize=8, textColor=ACCENT, fontName="Courier-Bold",
            backColor=colors.HexColor("#12122A"),
            leftIndent=8, spaceAfter=0, spaceBefore=8, leading=12,
            borderPadding=(4, 6, 2, 6)
        ),
        "tip": ParagraphStyle(
            "tip", parent=base["Normal"],
            fontSize=10, textColor=colors.HexColor("#065F46"),
            fontName="Helvetica-Oblique", backColor=colors.HexColor("#D1FAE5"),
            spaceAfter=8, spaceBefore=4, leading=14,
            borderPadding=(6, 8, 6, 8), borderColor=GREEN, borderWidth=1
        ),
        "warn": ParagraphStyle(
            "warn", parent=base["Normal"],
            fontSize=10, textColor=colors.HexColor("#78350F"),
            fontName="Helvetica-Oblique", backColor=colors.HexColor("#FEF3C7"),
            spaceAfter=8, spaceBefore=4, leading=14,
            borderPadding=(6, 8, 6, 8)
        ),
        "qa_q": ParagraphStyle(
            "qa_q", parent=base["Normal"],
            fontSize=11, textColor=BRAND, fontName="Helvetica-Bold",
            spaceAfter=3, spaceBefore=10, leftIndent=14
        ),
        "qa_a": ParagraphStyle(
            "qa_a", parent=base["Normal"],
            fontSize=10.5, textColor=colors.HexColor("#374151"),
            fontName="Helvetica", spaceAfter=6, leading=14,
            leftIndent=14, alignment=TA_JUSTIFY
        ),
        "tag": ParagraphStyle(
            "tag", parent=base["Normal"],
            fontSize=9, textColor=colors.white, fontName="Helvetica-Bold",
            backColor=ACCENT, leftIndent=0, spaceAfter=2, leading=12,
            borderPadding=(2, 6, 2, 6)
        ),
    }
    return custom


def cover_page(story, styles, W):
    # dark background band
    story.append(Spacer(1, 1.5*cm))
    # gradient-like banner using a table
    banner_data = [[Paragraph(
        '<font color="white"><b>CampusX · MCP Trilogy · Comprehensive Notes</b></font>',
        styles["cover_sub"]
    )]]
    banner = Table(banner_data, colWidths=[W])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), ACCENT),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(banner)
    story.append(Spacer(1, 0.5*cm))

    title_data = [[Paragraph(
        '<font color="white"><b>Model Context Protocol</b></font><br/>'
        '<font color="#E94560" size="20">Interview-Ready Revision Sheet</font>',
        styles["cover_title"]
    )]]
    title_box = Table(title_data, colWidths=[W])
    title_box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BRAND),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 28),
        ("BOTTOMPADDING", (0,0), (-1,-1), 28),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(title_box)
    story.append(Spacer(1, 0.6*cm))

    meta_rows = [
        ["Source", "CampusX YouTube — MCP Trilogy Playlist"],
        ["Topics", "Why MCP · Architecture · Lifecycle · Local Server · Remote Server · MCP Client"],
        ["Coverage", "Definitions · Architecture · Code Examples · Interview Q&A"],
        ["Format", "Interview-Ready Revision PDF"],
    ]
    meta = Table(meta_rows, colWidths=[3.5*cm, W-3.5*cm])
    meta.setStyle(TableStyle([
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("BACKGROUND", (0,0), (0,-1), LIGHT_BG),
        ("TEXTCOLOR", (0,0), (0,-1), ACCENT2),
        ("TEXTCOLOR", (1,0), (1,-1), BRAND),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.white, LIGHT_BG]),
        ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(meta)
    story.append(PageBreak())


def section_header(story, styles, title, W, color=BRAND):
    story.append(Spacer(1, 0.3*cm))
    data = [[Paragraph(title, styles["section_title"])]]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [5]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.25*cm))


def sub(story, styles, text):
    story.append(Paragraph(text, styles["subsection"]))


def body(story, styles, text):
    story.append(Paragraph(text, styles["body"]))


def bullets(story, styles, items):
    for item in items:
        story.append(Paragraph(f"• {item}", styles["bullet"]))


def code_block(story, styles, label, code_lines):
    story.append(Paragraph(f"# {label}", styles["code_label"]))
    for line in code_lines:
        story.append(Paragraph(line.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;"), styles["code"]))
    story.append(Spacer(1, 0.2*cm))


def tip(story, styles, text):
    story.append(Paragraph(f"💡 {text}", styles["tip"]))


def warn(story, styles, text):
    story.append(Paragraph(f"⚠️ {text}", styles["warn"]))


def qa(story, styles, question, answer):
    story.append(Paragraph(f"Q: {question}", styles["qa_q"]))
    story.append(Paragraph(f"A: {answer}", styles["qa_a"]))


def comparison_table(story, headers, rows, W, col_ratios=None):
    if col_ratios is None:
        col_ratios = [1/len(headers)] * len(headers)
    col_widths = [W * r for r in col_ratios]
    data = [headers] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0,0), (-1,0), ACCENT2),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9.5),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D1D5DB")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("WORDWRAP", (0,0), (-1,-1), True),
    ]
    t.setStyle(TableStyle(style))
    story.append(t)
    story.append(Spacer(1, 0.25*cm))


# ── Build story ─────────────────────────────────────────────────────────────
def build():
    path = "MCP_Revision_Sheet_CampusX.pdf"
    doc  = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.8*cm,  bottomMargin=2*cm,
        title="MCP Interview Revision Sheet – CampusX",
        author="Claude"
    )
    W = A4[0] - 3.6*cm
    styles = build_styles()
    story  = []

    # ── COVER ────────────────────────────────────────────────────────────────
    cover_page(story, styles, W)

    # ── TABLE OF CONTENTS ────────────────────────────────────────────────────
    story.append(Paragraph("Table of Contents", styles["toc_title"]))
    toc = [
        "1.  What is MCP? — Definition & Origin",
        "2.  Why MCP? — The Problem of Fragmentation",
        "3.  MCP vs Function Calling vs REST API",
        "4.  MCP Architecture — Hosts, Clients, Servers",
        "5.  MCP Primitives — Tools, Resources, Prompts",
        "6.  MCP Lifecycle — Connection to Termination",
        "7.  Transport Layer — STDIO vs Streamable HTTP (SSE)",
        "8.  Building Local MCP Servers (FastMCP)",
        "9.  Building Remote MCP Servers",
        "10. Building MCP Clients",
        "11. MCP Inspector — Debugging Tool",
        "12. MCP Ecosystem & Real-world Use Cases",
        "13. Interview Q&A — 30 Questions",
        "14. Quick-Reference Cheat Sheet",
    ]
    for item in toc:
        story.append(Paragraph(item, styles["toc_item"]))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 1 — WHAT IS MCP
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "1.  What is MCP? — Definition & Origin", W)

    body(story, styles,
        "<b>Model Context Protocol (MCP)</b> is an <b>open, standardised protocol</b> "
        "introduced by Anthropic (November 2024) that defines a universal, "
        "vendor-neutral way for AI applications to connect to external tools, data "
        "sources and services. It is now hosted by the <b>Linux Foundation</b> and "
        "open to community contributions."
    )
    body(story, styles,
        'Often called the <b>"USB-C for AI"</b> — just as USB-C standardised how '
        "devices connect to peripherals, MCP standardises how LLMs connect to the "
        "world outside their weights."
    )

    sub(story, styles, "Key Properties")
    bullets(story, styles, [
        "Language & vendor agnostic — works with any LLM (Claude, GPT, Gemini, …).",
        "Client-Server architecture built on <b>JSON-RPC 2.0</b>.",
        "Three primitives: <b>Tools</b> (actions), <b>Resources</b> (data), <b>Prompts</b> (templates).",
        "Two transports: <b>STDIO</b> (local) and <b>Streamable HTTP / SSE</b> (remote).",
        "Enables full agentic workflows: reason → retrieve → act → iterate.",
    ])
    tip(story, styles, "MCP is NOT a replacement for the LLM itself; it extends what the LLM can DO and SEE.")
    story.append(Spacer(1, 0.2*cm))

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 2 — WHY MCP
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "2.  Why MCP? — The Problem of Fragmentation", W, ACCENT2)

    sub(story, styles, "The Evolution Story (CampusX — 'The Why')")
    bullets(story, styles, [
        "<b>Wave 1 — Standalone LLMs:</b> Chat UIs, summarisation. LLMs are isolated; no tool access.",
        "<b>Wave 2 — Function Calling:</b> LLMs can invoke pre-defined functions. Works but requires custom glue code per integration.",
        "<b>Wave 3 — Tool Proliferation:</b> Many tools, but each LLM-app pair needs its own M×N adapter layer.",
        "<b>Wave 4 — MCP:</b> A single, standardised protocol. Any client talks to any server. M+N instead of M×N.",
    ])

    sub(story, styles, "The Copy-Paste Hell Problem")
    body(story, styles,
        "Before MCP, a developer using AI in their workflow had to manually copy context "
        "(code, documents, database records) into the chat window. This is error-prone, "
        "breaks continuity, and does not scale to autonomous agents. MCP solves this by "
        "making the AI <i>pull</i> the right context itself from authoritative servers."
    )

    sub(story, styles, "Problem with Naked Tool Calling (Pre-MCP)")
    bullets(story, styles, [
        "Every AI application had to implement its own tool-calling schema.",
        "Tools were tightly coupled to one specific LLM or framework.",
        "No discovery mechanism — the app had to hard-code every tool.",
        "Security & auth were ad-hoc and inconsistent.",
        "Sharing tools across teams / products was nearly impossible.",
    ])
    warn(story, styles, "Without MCP, adding a new data source (e.g., Notion) to 5 different AI apps means writing 5 separate integrations. With MCP, you write ONE MCP server and all 5 apps connect automatically.")
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 3 — MCP vs FUNCTION CALLING vs API
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "3.  MCP vs Function Calling vs REST API", W)

    comparison_table(story,
        ["Dimension", "Function Calling", "REST API", "MCP"],
        [
            ["Standardisation",  "LLM-specific schema",        "HTTP standard", "Open, vendor-neutral protocol"],
            ["Discovery",        "Hard-coded in prompt",        "Manual / OpenAPI", "Dynamic via tools/list endpoint"],
            ["Who controls call","Model (decides when)",        "Developer (explicit call)", "Model (tools) or App (resources)"],
            ["Transport",        "Embedded in LLM API",         "HTTP/S",        "STDIO or Streamable HTTP"],
            ["Context sharing",  "Manual",                      "Manual",        "Resources & Prompts built-in"],
            ["Reusability",      "Low — per-app logic",         "Medium",        "High — any MCP client can use"],
            ["Auth",             "Ad-hoc",                      "OAuth / API key", "Server-side, standardised"],
            ["Statefulness",     "Stateless per call",          "Stateless",     "Stateful session lifecycle"],
        ],
        W, [0.18, 0.24, 0.24, 0.34]
    )
    tip(story, styles, "Interview angle: MCP does NOT replace function calling — it STANDARDISES and EXTENDS it into a full protocol with lifecycle, auth, and discovery.")

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 4 — ARCHITECTURE
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "4.  MCP Architecture — Hosts, Clients, Servers", W, ACCENT2)

    sub(story, styles, "Core Components")
    comparison_table(story,
        ["Component", "Definition", "Examples"],
        [
            ["MCP Host",
             "The AI application that wants to use external tools/data via MCP. Embeds an MCP Client.",
             "Claude Desktop, Cursor IDE, VS Code Copilot, custom AI agent"],
            ["MCP Client",
             "Protocol client inside the Host. Maintains a 1:1 stateful session with one MCP Server.",
             "Built into Claude Desktop; or created manually with mcp Python SDK"],
            ["MCP Server",
             "Lightweight process that exposes capabilities (tools, resources, prompts) over MCP. Can be local or remote.",
             "expense-tracker-server, GitHub MCP, Filesystem MCP"],
            ["Local Data Sources",
             "Files, databases, services on the user's machine that the MCP Server can access.",
             "SQLite DB, local files, Docker containers"],
            ["Remote Services",
             "Cloud APIs and external platforms the MCP Server can call on behalf of the LLM.",
             "GitHub API, Slack API, Google Drive"],
        ],
        W, [0.18, 0.42, 0.40]
    )

    sub(story, styles, "Data Flow Diagram (Text)")
    body(story, styles,
        "<b>User → Host (AI App) → MCP Client → MCP Server → Data Source / API</b><br/>"
        "The Host does NOT talk to data sources directly. It talks to the MCP Client, "
        "which forwards requests to the appropriate MCP Server, which then accesses the "
        "underlying data."
    )

    sub(story, styles, "Two Protocol Layers")
    bullets(story, styles, [
        "<b>Data Layer:</b> Defines the JSON-RPC 2.0 message format, lifecycle management, and the three primitives (tools, resources, prompts).",
        "<b>Transport Layer:</b> Defines the physical channel — STDIO for local, Streamable HTTP for remote. Described in Section 7.",
    ])
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 5 — PRIMITIVES
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "5.  MCP Primitives — Tools, Resources, Prompts", W)

    sub(story, styles, "Overview Table")
    comparison_table(story,
        ["Primitive", "Definition", "Who Controls", "Read/Write", "Endpoint"],
        [
            ["Tools",
             "Executable functions the LLM can invoke to perform actions — API calls, DB writes, computations.",
             "Model-controlled (LLM decides when to call)",
             "Read + Write",
             "tools/list\ntools/call"],
            ["Resources",
             "Read-only data sources that provide context — files, DB records, schemas, configs.",
             "Application-controlled (Host decides when to surface)",
             "Read-only",
             "resources/list\nresources/read"],
            ["Prompts",
             "Reusable, pre-crafted instruction templates that guide how the LLM uses tools/resources.",
             "User-controlled (user selects from menu)",
             "Template",
             "prompts/list\nprompts/get"],
        ],
        W, [0.12, 0.35, 0.25, 0.14, 0.14]
    )

    sub(story, styles, "Tools — Deep Dive")
    body(story, styles,
        "Tools are the <b>action verbs</b> of MCP. The LLM autonomously decides when to "
        "call a tool based on the conversation. Each tool is defined with a name, "
        "description, and a <b>JSON Schema</b> for its inputs."
    )
    code_block(story, styles, "FastMCP — Defining a Tool (Python)", [
        "from fastmcp import FastMCP",
        "import sqlite3",
        "",
        "mcp = FastMCP('expense-tracker')",
        "",
        "@mcp.tool()",
        "def add_expense(amount: float, category: str, description: str) -> str:",
        '    """Add a new expense entry to the database."""',
        "    conn = sqlite3.connect('expenses.db')",
        "    conn.execute(",
        "        'INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)',",
        "        (amount, category, description)",
        "    )",
        "    conn.commit()",
        "    conn.close()",
        "    return f'Expense of {amount} added under {category}.'",
    ])

    sub(story, styles, "Resources — Deep Dive")
    body(story, styles,
        "Resources expose <b>read-only context</b>. The Host application makes them "
        "available; the LLM can reference them but cannot modify them through the resource "
        "interface. Think of them as a librarian handing over reference books."
    )
    code_block(story, styles, "FastMCP — Defining a Resource", [
        "@mcp.resource('config://categories')",
        "def get_categories() -> str:",
        '    """Return allowed expense categories as JSON."""',
        "    import json",
        "    categories = ['Food', 'Travel', 'Utilities', 'Entertainment', 'Health']",
        "    return json.dumps(categories)",
    ])

    sub(story, styles, "Prompts — Deep Dive")
    body(story, styles,
        "Prompts are <b>server-defined instruction templates</b>. A user picks a prompt "
        "from the Host UI (like a slash-command) and the server fills in the template "
        "with the right instructions and context for the LLM."
    )
    code_block(story, styles, "FastMCP — Defining a Prompt", [
        "from mcp.types import PromptMessage, TextContent",
        "",
        "@mcp.prompt()",
        "def monthly_summary_prompt(month: str) -> list[PromptMessage]:",
        '    """Generate a monthly expense analysis prompt."""',
        "    return [",
        "        PromptMessage(",
        "            role='user',",
        "            content=TextContent(",
        "                type='text',",
        "                text=f'Analyse all expenses for {month}. '",
        "                     f'Group by category, show totals, and flag anomalies.'",
        "            )",
        "        )",
        "    ]",
    ])
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 6 — LIFECYCLE
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "6.  MCP Lifecycle — Connection to Termination", W, ACCENT2)

    body(story, styles,
        "Every MCP session follows a <b>five-phase lifecycle</b>. Understanding this is "
        "critical for debugging and interviews."
    )

    phases = [
        ["Phase", "Name", "What Happens"],
        ["1", "Discovery",
         "Host finds available MCP servers (config file, registry, env vars). "
         "For local: path to executable. For remote: URL endpoint."],
        ["2", "Initialisation",
         "Client sends initialize request with its protocol version and capabilities. "
         "Server responds with its version and capabilities. Handshake is complete."],
        ["3", "Capability Exchange",
         "Client calls tools/list, resources/list, prompts/list to discover what the server offers. "
         "Both sides now know each other's full feature set."],
        ["4", "Active Session",
         "Normal operation — LLM makes tool calls, reads resources, selects prompts. "
         "Server sends notifications (progress, log events) without being asked."],
        ["5", "Termination",
         "Client sends shutdown signal. Server cleans up (closes DB connections, etc.). "
         "Process exits. For STDIO: parent process kills child. For HTTP: session ID invalidated."],
    ]
    t = Table(phases, colWidths=[1.0*cm, 3.5*cm, W-4.5*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BRAND),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9.5),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D1D5DB")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,0), (0,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*cm))
    tip(story, styles, "The initialize handshake uses protocol versioning — if client and server versions are incompatible, the session is rejected before any data flows.")

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 7 — TRANSPORT
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "7.  Transport Layer — STDIO vs Streamable HTTP (SSE)", W)

    sub(story, styles, "Transport Overview")
    comparison_table(story,
        ["Aspect", "STDIO (Standard I/O)", "Streamable HTTP / SSE"],
        [
            ["Use case",        "Local server, same machine",    "Remote server, multi-client, cloud"],
            ["How it works",    "Client spawns server as child process; JSON-RPC over stdin/stdout", "Client connects via HTTP; server streams responses via SSE; client POSTs requests"],
            ["Latency",         "Extremely low (in-process)",    "Network latency"],
            ["Multi-client",    "No — 1:1 relationship",         "Yes — multiple clients per server instance"],
            ["Auth",            "OS-level process isolation",    "OAuth 2.0 / Bearer tokens / API keys"],
            ["Deployment",      "Desktop apps (Claude Desktop)", "Cloud, Docker, SaaS platforms"],
            ["Logging",         "Must use stderr (stdout = protocol stream)", "Can use any logging framework"],
            ["Example clients", "Claude Desktop, local agents",  "Claude.ai, Cursor remote, web agents"],
        ],
        W, [0.17, 0.415, 0.415]
    )

    sub(story, styles, "One-Sentence Decision Rule")
    body(story, styles,
        "<i>\"If the user of the AI client also controls the machine the server runs on → "
        "use STDIO. If they don't → use Streamable HTTP.\"</i>"
    )
    warn(story, styles, "SSE (Server-Sent Events) was MCP's original remote transport (spec 2024-11-05) requiring two endpoints. It was replaced by Streamable HTTP in spec 2025-03-26. Many tutorials still show SSE — know both for interviews.")

    code_block(story, styles, "Running a FastMCP server in STDIO mode (default)", [
        "# server.py",
        "from fastmcp import FastMCP",
        "mcp = FastMCP('my-server')",
        "",
        "@mcp.tool()",
        "def add(a: int, b: int) -> int:",
        '    """Add two numbers."""',
        "    return a + b",
        "",
        "if __name__ == '__main__':",
        "    mcp.run()   # defaults to STDIO",
    ])

    code_block(story, styles, "Running a FastMCP server in Streamable HTTP mode (remote)", [
        "if __name__ == '__main__':",
        "    mcp.run(transport='streamable-http', host='0.0.0.0', port=8000)",
        "    # Clients connect to http://your-host:8000/mcp",
    ])
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 8 — LOCAL SERVER
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "8.  Building Local MCP Servers (FastMCP)", W, ACCENT2)

    sub(story, styles, "FastMCP vs Official MCP SDK")
    comparison_table(story,
        ["", "Official MCP SDK (mcp)", "FastMCP"],
        [
            ["Abstraction", "Low-level, verbose boilerplate", "High-level decorators, minimal code"],
            ["Learning curve", "Steep", "Gentle — Pythonic"],
            ["Production", "Full control", "Built on top of official SDK"],
            ["FastAPI compat", "No built-in", "Can convert FastAPI routes to MCP tools"],
            ["Install", "pip install mcp", "pip install fastmcp"],
        ],
        W, [0.22, 0.39, 0.39]
    )
    tip(story, styles, "FastMCP IS the official high-level SDK now maintained by Anthropic. It is NOT a third-party wrapper.")

    sub(story, styles, "Full Local Server Example — Expense Tracker (CampusX Project)")
    code_block(story, styles, "expense_tracker_server.py", [
        "from fastmcp import FastMCP",
        "import sqlite3, json",
        "from datetime import date",
        "",
        "mcp = FastMCP('expense-tracker')",
        "DB  = 'expenses.db'",
        "",
        "def init_db():",
        "    conn = sqlite3.connect(DB)",
        "    conn.execute('''CREATE TABLE IF NOT EXISTS expenses",
        "                    (id INTEGER PRIMARY KEY AUTOINCREMENT,",
        "                     amount REAL, category TEXT,",
        "                     description TEXT, date TEXT)''')",
        "    conn.commit(); conn.close()",
        "",
        "@mcp.tool()",
        "def add_expense(amount: float, category: str,",
        "                description: str, expense_date: str = '') -> str:",
        '    """Add a new expense. date format: YYYY-MM-DD"""',
        "    if not expense_date:",
        "        expense_date = str(date.today())",
        "    conn = sqlite3.connect(DB)",
        "    conn.execute('INSERT INTO expenses VALUES (NULL,?,?,?,?)',",
        "                 (amount, category, description, expense_date))",
        "    conn.commit(); conn.close()",
        "    return f'Added: {category} — {amount} on {expense_date}'",
        "",
        "@mcp.tool()",
        "def list_expenses(start_date: str = '', end_date: str = '') -> str:",
        '    """List expenses, optionally filtered by date range."""',
        "    conn = sqlite3.connect(DB)",
        "    if start_date and end_date:",
        "        rows = conn.execute(",
        "            'SELECT * FROM expenses WHERE date BETWEEN ? AND ?',",
        "            (start_date, end_date)).fetchall()",
        "    else:",
        "        rows = conn.execute('SELECT * FROM expenses').fetchall()",
        "    conn.close()",
        "    return json.dumps([{'id':r[0],'amount':r[1],'category':r[2],",
        "                        'desc':r[3],'date':r[4]} for r in rows])",
        "",
        "@mcp.tool()",
        "def summarise_expenses() -> str:",
        '    """Return total spend per category."""',
        "    conn = sqlite3.connect(DB)",
        "    rows = conn.execute(",
        "        'SELECT category, SUM(amount) FROM expenses GROUP BY category'",
        "    ).fetchall()",
        "    conn.close()",
        "    return json.dumps({r[0]: r[1] for r in rows})",
        "",
        "@mcp.resource('config://categories')",
        "def categories() -> str:",
        '    """Allowed expense categories."""',
        "    return json.dumps(['Food','Travel','Utilities','Health','Entertainment'])",
        "",
        "if __name__ == '__main__':",
        "    init_db()",
        "    mcp.run()   # STDIO — for Claude Desktop",
    ])

    sub(story, styles, "Connecting to Claude Desktop (claude_desktop_config.json)")
    code_block(story, styles, "~/.config/Claude/claude_desktop_config.json", [
        '{',
        '  "mcpServers": {',
        '    "expense-tracker": {',
        '      "command": "python",',
        '      "args": ["/absolute/path/to/expense_tracker_server.py"],',
        '      "env": {}',
        '    }',
        '  }',
        '}',
    ])
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 9 — REMOTE SERVER
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "9.  Building Remote MCP Servers", W)

    body(story, styles,
        "A <b>remote MCP server</b> runs on a separate machine (cloud VM, container, "
        "serverless function) and is accessible over the network via Streamable HTTP. "
        "Multiple MCP clients can connect to a single remote server simultaneously."
    )

    sub(story, styles, "Converting the Local Server to Remote")
    code_block(story, styles, "remote_expense_server.py (only change from local)", [
        "if __name__ == '__main__':",
        "    init_db()",
        "    mcp.run(",
        "        transport='streamable-http',",
        "        host='0.0.0.0',",
        "        port=8000",
        "    )",
        "    # Endpoint: http://<your-ip>:8000/mcp",
    ])

    sub(story, styles, "Connecting Claude Desktop to a Remote Server")
    code_block(story, styles, "claude_desktop_config.json — remote", [
        '{',
        '  "mcpServers": {',
        '    "remote-expense-tracker": {',
        '      "command": "npx",',
        '      "args": ["-y", "mcp-remote", "http://your-server-ip:8000/mcp"]',
        '    }',
        '  }',
        '}',
        '// mcp-remote is a bridge that wraps HTTP servers for STDIO-only clients',
    ])

    sub(story, styles, "FastAPI → MCP Conversion")
    body(story, styles,
        "FastMCP supports converting an existing <b>FastAPI</b> application into an MCP "
        "server. This lets businesses expose their existing REST API to AI clients without "
        "rewriting logic:"
    )
    code_block(story, styles, "fastapi_to_mcp.py", [
        "from fastapi import FastAPI",
        "from fastmcp import FastMCP",
        "",
        "app = FastAPI()",
        "",
        "@app.get('/expenses')",
        "def get_expenses(): ...",
        "",
        "@app.post('/expenses')",
        "def create_expense(amount: float, category: str): ...",
        "",
        "# Convert FastAPI app to MCP server",
        "mcp = FastMCP.from_fastapi(app, name='expense-api-mcp')",
        "",
        "if __name__ == '__main__':",
        "    mcp.run(transport='streamable-http', port=9000)",
    ])
    tip(story, styles, "FastAPI→MCP conversion is a huge business advantage: existing REST backends instantly become MCP-compatible without code duplication.")
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 10 — MCP CLIENT
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "10.  Building MCP Clients", W, ACCENT2)

    body(story, styles,
        "While Claude Desktop is a pre-built MCP client, you can build your own custom "
        "MCP client — for example, a Python agent that programmatically talks to multiple "
        "MCP servers. This is covered in the CampusX 'How to Build MCP Clients' video."
    )

    code_block(story, styles, "Custom MCP Client — Connecting to Multiple Servers", [
        "import asyncio",
        "from mcp import ClientSession, StdioServerParameters",
        "from mcp.client.stdio import stdio_client",
        "",
        "async def main():",
        "    # Connect to local Math MCP server",
        "    math_params = StdioServerParameters(",
        "        command='python', args=['math_server.py']",
        "    )",
        "    async with stdio_client(math_params) as (read, write):",
        "        async with ClientSession(read, write) as session:",
        "            await session.initialize()",
        "",
        "            # Discover available tools",
        "            tools = await session.list_tools()",
        "            print('Tools:', [t.name for t in tools.tools])",
        "",
        "            # Call a tool",
        "            result = await session.call_tool('add', {'a': 5, 'b': 3})",
        "            print('5 + 3 =', result.content[0].text)",
        "",
        "asyncio.run(main())",
    ])

    code_block(story, styles, "Connecting to a Remote MCP Server (HTTP)", [
        "from mcp.client.streamable_http import streamablehttp_client",
        "",
        "async def connect_remote():",
        "    async with streamablehttp_client('http://myserver:8000/mcp') as (r, w, _):",
        "        async with ClientSession(r, w) as session:",
        "            await session.initialize()",
        "            tools = await session.list_tools()",
        "            # ... use tools",
    ])

    tip(story, styles, "A single MCP client can maintain sessions with MULTIPLE MCP servers simultaneously. The LLM picks which server's tools to call based on context.")

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 11 — MCP INSPECTOR
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "11.  MCP Inspector — Debugging Tool", W)

    sub(story, styles, "What is MCP Inspector?")
    body(story, styles,
        "MCP Inspector is the <b>official browser-based debugging tool</b> for MCP servers. "
        "It lets you connect to any MCP server, list its tools/resources/prompts, and "
        "invoke them manually — without needing Claude Desktop."
    )

    sub(story, styles, "Running MCP Inspector")
    code_block(story, styles, "Terminal — launch inspector", [
        "# Start your server first",
        "python expense_tracker_server.py",
        "",
        "# In another terminal, launch inspector",
        "npx @modelcontextprotocol/inspector",
        "",
        "# Open browser at http://localhost:5173",
        "# Connect to: http://localhost:8000/mcp  (or stdio transport)",
    ])

    sub(story, styles, "Inspector Capabilities")
    bullets(story, styles, [
        "List all tools, resources, and prompts exposed by the server.",
        "Call any tool with custom JSON input and see the response.",
        "Read any resource and view its content.",
        "View protocol-level JSON-RPC messages in real time.",
        "Test error handling and edge cases before connecting to a real LLM.",
    ])
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 12 — ECOSYSTEM
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "12.  MCP Ecosystem & Real-World Use Cases", W, ACCENT2)

    sub(story, styles, "Official MCP Servers (maintained by Anthropic & community)")
    bullets(story, styles, [
        "<b>Filesystem</b> — read/write local files with permission controls.",
        "<b>GitHub</b> — manage repos, PRs, issues, and code via natural language.",
        "<b>Slack</b> — send messages, read channels, search workspace.",
        "<b>Google Drive</b> — search and read documents, spreadsheets.",
        "<b>PostgreSQL / SQLite</b> — natural language to SQL query execution.",
        "<b>Sentry</b> — fetch error reports and stack traces into LLM context.",
        "<b>Puppeteer</b> — browser automation via LLM instructions.",
        "<b>Memory</b> — persistent knowledge graph the LLM updates over time.",
    ])

    sub(story, styles, "CampusX Real-World Demo — AI Newsletter Generator")
    body(story, styles,
        "In the Trilogy intro video, CampusX demonstrated an end-to-end MCP workflow: "
        "the AI was given a topic and, using MCP, it autonomously — (1) <b>researched</b> "
        "the topic via web-search tools, (2) <b>drafted</b> the newsletter copy, and "
        "(3) <b>designed</b> the layout — all without manual copy-pasting. Each phase used "
        "a different MCP server."
    )

    sub(story, styles, "Benefits Summary")
    comparison_table(story,
        ["Benefit", "Explanation"],
        [
            ["Interoperability", "Any MCP-compatible host works with any MCP server. Write once, use everywhere."],
            ["Reduced Integration Cost", "M+N integrations instead of M×N. Huge savings at scale."],
            ["Security", "Servers handle auth; LLM never sees raw credentials."],
            ["Discoverability", "LLM can discover tools at runtime — no hard-coded prompts."],
            ["Agentic Power", "LLM can chain multiple tool calls across servers to complete complex tasks."],
            ["Observability", "Centralised server-side logging, monitoring, and rate limiting."],
        ],
        W, [0.25, 0.75]
    )
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 13 — Q&A
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "13.  Interview Q&A — 30 Questions", W)

    qas = [
        ("What is the Model Context Protocol?",
         "MCP is an open, vendor-neutral protocol by Anthropic (2024) that standardises how AI applications connect to external tools, data sources, and services using a client-server architecture over JSON-RPC 2.0."),
        ("Why was MCP created?",
         "To solve the M×N integration problem — without MCP, each AI app needed custom code to talk to each data source. MCP reduces this to M+N by providing a universal interface layer."),
        ("What analogy is used to explain MCP?",
         "'USB-C for AI' — just as USB-C standardised peripheral connections for devices, MCP standardises how LLMs connect to external systems."),
        ("What are the three roles in MCP architecture?",
         "MCP Host (the AI application), MCP Client (protocol client inside the host, 1:1 with server), and MCP Server (exposes tools/resources/prompts)."),
        ("What are the three MCP primitives?",
         "Tools (executable functions, model-controlled), Resources (read-only data, application-controlled), and Prompts (reusable templates, user-controlled)."),
        ("What is the difference between Tools and Resources?",
         "Tools are action-oriented and can read AND write data; the LLM decides when to call them. Resources are strictly read-only context; the application decides when to surface them."),
        ("What is the MCP lifecycle?",
         "Five phases: (1) Discovery, (2) Initialisation (version handshake), (3) Capability Exchange (list tools/resources/prompts), (4) Active Session, (5) Termination."),
        ("What are the two MCP transports and when do you use each?",
         "STDIO for local servers on the same machine (Claude Desktop use case). Streamable HTTP for remote/cloud servers accessed by multiple clients."),
        ("What is FastMCP?",
         "FastMCP is the official high-level Python SDK for building MCP servers. It provides Pythonic decorators (@mcp.tool, @mcp.resource, @mcp.prompt) built on top of the low-level MCP SDK."),
        ("How do you define a tool in FastMCP?",
         "Using the @mcp.tool() decorator on a Python function with a docstring (description) and typed parameters (JSON schema generated automatically)."),
        ("What is MCP Inspector and why is it useful?",
         "MCP Inspector is a browser-based debugging tool (npx @modelcontextprotocol/inspector) that lets developers connect to any MCP server, discover capabilities, and manually invoke tools without needing Claude Desktop."),
        ("How does MCP differ from traditional function calling?",
         "Function calling is LLM-specific and requires hard-coded schemas. MCP is vendor-neutral, has a standardised lifecycle, built-in discovery (tools/list), stateful sessions, and covers both action (tools) and context (resources) primitives."),
        ("What protocol underlies MCP message exchange?",
         "JSON-RPC 2.0 — a lightweight remote procedure call protocol using JSON for message encoding."),
        ("What is the copy-paste hell problem MCP solves?",
         "Before MCP, developers had to manually copy context (code, documents, records) into AI chat windows. MCP lets the AI autonomously pull the right context from authoritative servers, eliminating manual copy-pasting."),
        ("Can one MCP client talk to multiple servers?",
         "Yes. A single MCP host can maintain MCP client sessions with multiple servers simultaneously. The LLM selects the appropriate server's tools based on the task."),
        ("What happens during Capability Exchange?",
         "The client calls tools/list, resources/list, and prompts/list to dynamically discover everything the server exposes. This allows the LLM to know what actions are available at runtime."),
        ("How is auth handled in remote MCP servers?",
         "Auth is server-side. Remote servers use OAuth 2.0, Bearer tokens, or API keys. The LLM never sees raw credentials — the server handles all auth logic."),
        ("What is the difference between SSE and Streamable HTTP in MCP?",
         "SSE (deprecated, spec 2024-11-05) needed two endpoints — a GET for the event stream and a POST for client messages. Streamable HTTP (spec 2025-03-26) unified this into a single /mcp endpoint."),
        ("Why must STDIO servers log to stderr, not stdout?",
         "MCP uses stdout for JSON-RPC messages. Any output to stdout (like print statements) corrupts the protocol stream and causes the client to disconnect."),
        ("How do you connect Claude Desktop to a local MCP server?",
         "Add an entry in claude_desktop_config.json under 'mcpServers' with the command and args pointing to your server script. Claude Desktop spawns it as a child process on startup."),
        ("How do you connect Claude Desktop to a remote MCP server?",
         "Use mcp-remote as a bridge: set command to 'npx', args to ['-y', 'mcp-remote', 'http://server-url/mcp'] in claude_desktop_config.json."),
        ("What is FastAPI→MCP conversion and why is it useful?",
         "FastMCP.from_fastapi(app) converts an existing FastAPI application into an MCP server. This allows businesses to expose existing REST APIs to AI clients without rewriting any business logic."),
        ("What is the MCP ecosystem?",
         "A growing collection of official and community MCP servers (GitHub, Slack, Filesystem, PostgreSQL, Google Drive, etc.) and clients (Claude Desktop, Cursor, VS Code). Open-sourced under Linux Foundation."),
        ("What does 'model-controlled' mean for Tools?",
         "The LLM autonomously decides WHEN to call a tool based on the conversation. The developer does not need to explicitly trigger it — the model infers the right tool from context."),
        ("What does 'application-controlled' mean for Resources?",
         "The host application decides which resources to surface to the LLM, not the LLM itself. Resources are injected into context by the application layer."),
        ("What endpoint does a client use to invoke a tool?",
         "tools/call — with the tool name and input parameters as JSON. The server returns the result which the LLM reads and incorporates into its response."),
        ("How does MCP enable agentic AI?",
         "MCP gives AI models a standardised way to discover actions (tools), access context (resources), and follow workflows (prompts). This enables autonomous, multi-step agentic loops: reason → retrieve → act → iterate."),
        ("What is the MCP Server Inspector and what's its npm command?",
         "The official browser UI for testing MCP servers: npx @modelcontextprotocol/inspector. It connects to your server and lets you call tools, read resources, and view raw protocol messages."),
        ("How are resources different from direct database queries?",
         "Resources are abstracted, read-only data access with defined URIs (e.g., 'config://categories'). The LLM accesses data through a safe, server-controlled interface rather than executing raw SQL."),
        ("What is the significance of MCP being under the Linux Foundation?",
         "It guarantees long-term vendor neutrality, open governance, and community ownership. No single company (including Anthropic) can unilaterally change the protocol, making it safe for enterprise adoption."),
    ]

    for i, (q, a) in enumerate(qas, 1):
        qa(story, styles, f"[Q{i}] {q}", a)
        if i % 10 == 0 and i < len(qas):
            story.append(PageBreak())

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 14 — CHEAT SHEET
    # ═══════════════════════════════════════════════════════════════════════
    section_header(story, styles, "14.  Quick-Reference Cheat Sheet", W, ACCENT2)

    sub(story, styles, "Key Terms at a Glance")
    terms = [
        ["Term", "One-Line Definition"],
        ["MCP", "Open protocol for connecting AI apps to external tools & data (USB-C for AI)"],
        ["MCP Host", "The AI application (e.g., Claude Desktop) that embeds an MCP Client"],
        ["MCP Client", "Protocol client inside a Host; maintains 1:1 session with a Server"],
        ["MCP Server", "Lightweight process exposing tools/resources/prompts over MCP"],
        ["Tool", "Executable function the LLM calls to take action (model-controlled)"],
        ["Resource", "Read-only data the app surfaces to the LLM (application-controlled)"],
        ["Prompt", "Reusable instruction template the user selects (user-controlled)"],
        ["STDIO", "Local transport — client spawns server as child process"],
        ["Streamable HTTP", "Remote transport — HTTP + SSE for multi-client server access"],
        ["FastMCP", "Official high-level Python SDK with @mcp.tool / @mcp.resource decorators"],
        ["JSON-RPC 2.0", "The underlying wire protocol for all MCP messages"],
        ["MCP Inspector", "Browser-based debug tool: npx @modelcontextprotocol/inspector"],
        ["Capability Exchange", "Client lists tools/resources/prompts from server at session start"],
        ["mcp-remote", "npm bridge that lets STDIO-only clients connect to remote HTTP servers"],
    ]
    t = Table(terms, colWidths=[3.8*cm, W-3.8*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), ACCENT2),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (0,-1), "Courier-Bold"),
        ("FONTNAME", (1,1), (1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("TEXTCOLOR", (0,1), (0,-1), ACCENT),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D1D5DB")),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.4*cm))

    sub(story, styles, "Must-Know Commands")
    code_block(story, styles, "Install FastMCP", [
        "pip install fastmcp",
        "pip install mcp          # low-level SDK",
    ])
    code_block(story, styles, "Run MCP Inspector", [
        "npx @modelcontextprotocol/inspector",
    ])
    code_block(story, styles, "FastMCP minimal server (3 lines)", [
        "from fastmcp import FastMCP",
        "mcp = FastMCP('demo')",
        "@mcp.tool()",
        "def hello(name: str) -> str: return f'Hello {name}'",
        "mcp.run()",
    ])
    code_block(story, styles, "FastMCP run modes", [
        "mcp.run()                                        # STDIO (local)",
        "mcp.run(transport='streamable-http', port=8000)  # Remote HTTP",
    ])

    # ── Footer ───────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width=W, thickness=1, color=ACCENT))
    story.append(Spacer(1, 0.15*cm))
    footer_data = [[
        Paragraph('<font color="#6B7280" size="8">Based on CampusX YouTube — MCP Trilogy Playlist | '
                  'Prepared with Claude | For interview preparation only</font>',
                  ParagraphStyle("footer", fontSize=8, textColor=MUTED, alignment=TA_CENTER))
    ]]
    footer = Table(footer_data, colWidths=[W])
    footer.setStyle(TableStyle([("ALIGN", (0,0), (-1,-1), "CENTER")]))
    story.append(footer)

    doc.build(story)
    print(f"PDF saved to {path}")


build()