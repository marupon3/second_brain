---
crated: 2026-08-09
tags:
  - claude
  - obsidian
Source: https://x.com/0xkkai/status/2085838657068347401
---
# 要約

Claudeに知識を記憶させるためにObsidianを活用するGitHubリポジトリが急増していると指摘。
KarpathyのWikiパターン、Skills、MCPの3アーキテクチャを解説し、10個のリポジトリを評価。結局必要なのは、**「知識を構造化するコンパイラ系」 と 「実行時アクセス用ブリッジ系」** の2つだけだと主張し、ユーザー種別に応じた選び方を提案している。

# In the past four months, GitHub has quietly filled up with repositories that solve the same problem from different angles: how to make Claude actually remember what you know, using Obsidian as the storage layer.

Most of them are wrappers. Some of them are architectures. Two of them are worth building your workflow around today. This is the honest breakdown - what each one actually does, what it doesn't, and which one to install first depending on who you are.

Before the list, three architectures you need to understand. Otherwise every repo will look the same, and you'll waste a weekend installing four things that do the same thing.

## The Three Architectures Behind Every Repo On This List

### 1. The Karpathy LLM Wiki Pattern

In April 2026, Andrej Karpathy published an 800-word gist on GitHub called LLM-WIKI. It described a three-folder architecture: `raw/` for source documents, `wiki/` for compiled linked pages Claude actually reads from, and `instructions/` for the rules that keep the wiki from drifting into chaos.

The move that made it viral: Claude reads any given raw file once in its entire life, extracts what matters, writes it into the wiki, and never touches the raw file again.

**Why this matters:** Every subsequent query pulls from the compiled wiki, which cuts token spend 70-90% on repeat lookups and gives you a knowledge base that actually compounds instead of decays.

**Repos in this family:** #1, #4, #5, #10.

### 2. The Skills Architecture

Anthropic quietly shipped a folder system in July where Claude auto-loads specialized instructions based on what you ask. You drop a folder into your skills directory containing a `SKILL.md` that describes when to trigger and what to do. Claude reads only the description at startup - the full skill loads only when the trigger fires.

For an Obsidian vault, this means you can define workflows like "when I mention a paper, activate paper-reader skill" or "when I open the vault, load my note-organization convention" without polluting your main context window.

**Repos in this family:** #3, #9.

### 3. The MCP Bridge

Model Context Protocol is the standard Anthropic released for connecting Claude to external tools and data. An MCP server acts as a live bridge - Claude sends structured requests, the server queries your vault, returns results in real time.

MCP repos come in two flavors: read-only (safe, Claude can only pull data) and read-write (powerful, Claude can create/edit notes).

**Rule of thumb:** Read-only is what most researchers should start with. Read-write is what enables the "vault builds itself while you sleep" workflow.

**Repos in this family:** #2, #6, #7, #8.

---

## The 10 Repos, Ranked and Analyzed

### 1. AgriciDaniel/claude-obsidian

**Architecture:** Karpathy Wiki Pattern (purest implementation)

**What it does:** You drop any source document - pdf, markdown note, web clip, transcript - into a `raw/` folder. Claude reads it once, compiles it into 8-15 linked wiki pages, and files it into the graph. Next time you query, Claude speaks only from the wiki with sources already cited.

**Setup difficulty:** Medium. You install as a Claude Code plugin, point it at an empty vault, then start dropping files. Initial vault takes 20-30 minutes to configure the way you want. After that, ingest is a single command.

**Best for:** Anyone new to the Karpathy pattern who wants the cleanest reference implementation. This is the closest thing to a canonical setup and is what most creators building content around this pattern are running.

**Actual limitations:** Opinionated folder structure - if you already have a vault organized differently, migration is painful. No built-in semantic search - retrieval relies on Claude opening the wiki and following links. Not designed for team use.

**Verdict:** Start here if you're building your first knowledge vault. Skip if you already have 500+ notes in a different structure.

### 2. eugeniughelbur/obsidian-second-brain

**Architecture:** MCP (read-write) + Skills + custom commands

**What it does:** Provides persistent memory for Claude Code and six other CLI agents. Ships with 45 named commands including hybrid semantic search (BM25 + embeddings), self-rewriting notes that update themselves when you contradict them, key-less web research (uses public search), and scheduled agents that maintain the vault while you sleep.

**Setup difficulty:** High initially, low forever after. First-time setup requires installing local embedding models and configuring the scheduler. Once running, it's the most hands-off system on this list.

**Best for:** Power users with a vault of 1,000+ notes who want to stop babysitting it.

**The killer feature:** Scheduled agents. You can tell Claude to lint your wiki nightly, deduplicate similar notes weekly, or resurface stale content monthly, with no intervention.

**Actual limitations:** Complexity tax. Reading the docs takes 90 minutes. Local embeddings require ~4GB RAM. Some commands assume Claude Code specifically and won't work with Claude Desktop or the web app.

**Verdict:** The most powerful setup on this list. Reach for it once your vault has outgrown your ability to maintain it manually.

### 3. kepano/obsidian-skills

**Architecture:** Skills (Anthropic-native pattern)

**What it does:** Ships pre-built agent skills authored by Kepano (the creator of Obsidian). Works with Claude Code, Codex, and Open Code. Each skill is a folder with a `SKILL.md` describing when to trigger and what to do - no manual context management needed.

**Setup difficulty:** Low. Clone the repo into your Claude skills folder, done. Skills auto-register on next Claude startup.

**Best for:** Anyone who wants "official-ish" defaults. Because Kepano authored these, the conventions align with how Obsidian actually thinks about knowledge management - folders, tags, backlinks. If you're already fluent in the Obsidian ecosystem, this feels native.

**Actual limitations:** Skills-only, no MCP. You can't do live queries - Claude reads the vault through the file system, so real-time vault state changes require refreshes. Also: fewer skills shipped than the ecosystem clones like #9.

**Verdict:** The safest bet for anyone deep in the Obsidian mindset already. The trust factor here is high - you're running code from the person who built the thing.

### 4. qhuang20/obsidian-skills

**Architecture:** Skills + Karpathy Wiki Pattern

**What it does:** A Claude Code plugin that ships with a dedicated llm-wiki skill implementing the Karpathy pattern directly, plus several utility skills for note management. Trigger the wiki skill by mentioning a source; Claude does the ingest and linking silently.

**Setup difficulty:** Low-medium. Standard Claude Code plugin install. The wiki skill needs one initial config file describing your vault's naming conventions.

**Best for:** Users who want the Karpathy pattern without building it from scratch. Faster path to a working wiki than repo #1 if you're comfortable in Claude Code specifically.

**Actual limitations:** Less battle-tested than #1. The utility skills are convenient but overlap with #3 and #5, so you'll want to pick a lane.

**Verdict:** Solid if you already live in Claude Code. Consider #1 for a cleaner reference and #5 for a purer Karpathy focus.

### 5. ekadetov/llm-wiki

**Architecture:** Karpathy Wiki Pattern (pure play)

**What it does:** Nothing but the Karpathy pattern, implemented as a Claude Code plugin. No extra bells. Ingest, query, save, lint - the six commands from the original gist, tightened up.

**Setup difficulty:** Very low. Install, point at vault, run `/init`. Working ingest in under 5 minutes.

**Best for:** Purists. If you want the pattern implemented exactly as Karpathy described it and nothing else muddying the surface area, this is it.

**Actual limitations:** No semantic search, no scheduled agents, no MCP bridge. Deliberately minimal, which is either a feature or a dealbreaker depending on your appetite.

**Verdict:** Best minimum-viable Karpathy pattern implementation. Great starting point, may outgrow it.

### 6. iansinnott/obsidian-claude-code-mcp

**Architecture:** MCP (read-write via Obsidian plugin)

**What it does:** An Obsidian plugin that runs an MCP server inside your Obsidian instance. When Claude Code queries the server, it can read files, create new notes, modify existing ones, follow backlinks, and update the graph - all through Obsidian's own API, so nothing bypasses Obsidian's file safety.

**Setup difficulty:** Medium. Install as an Obsidian community plugin, enable the MCP server, add the endpoint to Claude Code config. Requires Obsidian to be running for the bridge to work.

**Best for:** Users who want Claude to interact with a live Obsidian instance - respecting plugins, templates, dataview queries, all of it.

**What makes this one different:** It's the only repo on this list that goes through Obsidian's API rather than the raw file system.

**Actual limitations:** Requires Obsidian to be open. Bridge latency is higher than file-system MCPs (~200ms per query vs. ~20ms). No support for mobile Obsidian.

**Verdict:** The right choice if your vault depends heavily on Obsidian plugins (Dataview, Templater, Excalidraw). Overkill for plain markdown vaults.

### 7. noesskeetit/second-brain-mcp

**Architecture:** MCP (read-only + semantic search)

**What it does:** Offline, plugin-free MCP server. Reads vault as plain files from disk, builds a local semantic index, and exposes semantic search rather than path-based file access. Works with Claude Code, Cursor, Zed, or any MCP-compliant client.

**Setup difficulty:** Low. One config command, one Claude config edit, done. Semantic index builds automatically on first run.

**Best for:** Multi-tool users. If you switch between Claude Code, Cursor, and Zed depending on task, this gives you a consistent semantic memory across all of them without duplicating setup.

**Actual limitations:** Read-only. Claude can query and retrieve but cannot write back - so this pairs well with a separate write-oriented tool like #4 or the Karpathy skills.

**Verdict:** Best MCP for semantic retrieval across multiple AI tools. Pair with a write-capable tool for the full workflow.

### 8. CoMfUcIoS/second-brain-mcp

**Architecture:** MCP (strictly read-only)

**What it does:** Intentionally read-only MCP server. Claude can query the vault every way - search, follow links, extract metadata - but it cannot write, delete, or modify anything. Ever.

**Setup difficulty:** Low. Same profile as #7.

**Best for:** Security-conscious users. If you have 5+ years of notes and the idea of Claude accidentally rewriting one gives you anxiety, this removes the risk entirely.

**Actual limitations:** Read-only means you lose the automation loop (Claude can't file new notes for you). Every "save this insight" moment requires you to manually copy from chat into Obsidian.

**Verdict:** The right choice for archivists. Wrong choice for automation workflows.

### 9. sunnyhasija/obsidian-plugin-skills

**Architecture:** Skills (Obsidian-specific expansions of #3)

**What it does:** Expands on Kepano's official skills with community-contributed additions - daily journal skill, meeting-notes skill, book-highlight extractor, spaced-review skill. All Obsidian-native, no MCP.

**Setup difficulty:** Low.

**Best for:** Users who liked #3 but wanted more variety out of the box.

**Actual limitations:** Community-maintained means quality varies skill by skill. Some are polished, some are drafts. Read each `SKILL.md` before enabling.

**Verdict:** Good complement to #3. Cherry-pick specific skills rather than enabling everything.

### 10. C-Bjorn/MegaMem

**Architecture:** MCP + Temporal Knowledge Graph (powered by Graphiti)

**What it does:** Syncs your Obsidian vault into a temporal knowledge graph and exposes it to Claude via MCP. Ships with 12 graph tools + 11 vault file tools. Unlike every other MCP on this list, MegaMem tracks when concepts changed - so Claude can answer "what did I believe about X in April vs. now" instead of just "what do I believe about X".

**Setup difficulty:** Medium-high. Requires a running graph store (Graphiti backend) plus the MCP config. First-time setup ~40 minutes.

**Best for:** Anyone whose thinking evolves over time - analysts, researchers, journal writers. If you regularly change your mind about topics you've already documented, this is the only repo that captures the drift.

**Actual limitations:** Heaviest infrastructure footprint on the list. Overkill if your vault is mostly evergreen references. Requires more memory than pure-file MCPs.

**Verdict:** The only repo here that treats your knowledge as changing over time. Reach for it when temporal reasoning matters.

---

## Which One to Install by User Type

- **If you're new to this and just want a working vault:** Install #1 AgriciDaniel/claude-obsidian. Follow the quickstart, ingest one file, watch the wiki appear. If you like it, you now have a working reference implementation.

- **If you already have 500+ notes and want automation:** Install #2 eugeniughelbur/obsidian-second-brain. Absorb the setup cost once, then never manually maintain your vault again.

- **If you use Claude Code as your daily driver:** Install #4 qhuang20/obsidian-skills. Skills-native, Claude Code-native, fastest time-to-working-state.

- **If you're a researcher who values retrieval over automation:** Install #7 noesskeetit/second-brain-mcp for read-only semantic search across your existing vault. Add write capability later with #4 if needed.

- **If your vault is precious and you don't want automated writes:** Install #8 CoMfUcIoS/second-brain-mcp. Strictly read-only. Nothing can be corrupted.

- **If your Obsidian setup lives on plugins (Dataview, Templater):** Install #6 iansinnott/obsidian-claude-code-mcp. It's the only one that goes through the Obsidian API and respects your plugin stack.

---

## 5-Minute Quickstart With Repo #1

Within a minute Claude reads the file, writes 8-15 linked wiki pages, and files them into your vault. Open Obsidian, switch to graph view, and you'll see the first nodes of what will become your second brain.

**The compounding moment:** Every subsequent ingest expands the graph without ever re-reading the original source. That's the entire point.

---

## What's Not On This List, and Why

- **Smart Connections / Copilot / QuickAdd plugins.** Solid Obsidian AI plugins, but they don't implement the wiki pattern or use MCP. They put AI features on top of your existing workflow rather than restructuring how the vault compiles knowledge. Different tool category.

- **Notion / Mem / Reflect.** Not Obsidian, not open source, not on plain markdown. If you care about owning your data as portable files, they're not options.

- **RAG-only wrappers.** Any repo that just wraps embeddings + retrieval without the wiki pattern is retrieving from your mess, not building order out of it.

That's the whole insight from Karpathy - raw is source code, wiki is compiled product. RAG without compilation is grep with vibes.

---

## The Honest Take

You need two of these, not ten.

Pick one from the Karpathy Wiki family (#1, #4, or #5) to be the compiler that turns raw sources into structured knowledge. Pick one from the MCP family (#2, #7, or #8) to give Claude runtime access to that knowledge across every AI tool you use.

That's it. Two repos, one compiler, one bridge. Everything else on this list is either a variation of the two or a specialty tool for a specific edge case.

The mistake most people make is installing five of these and losing weekends to config debt. Start with two. Build the vault. Add the third only when you feel the specific pain the third one solves.

---

## GitHub links

- https://github.com/AgriciDaniel/claude-obsidian
- https://github.com/eugeniughelbur/obsidian-second-brain
- https://github.com/kepano/obsidian-skills
- https://github.com/qhuang20/obsidian-skills
- https://github.com/ekadetov/llm-wiki
- https://github.com/iansinnott/obsidian-claude-code-mcp
- https://github.com/noesskeetit/second-brain-mcp
- https://github.com/CoMfUcIoS/second-brain-mcp
- https://github.com/sunnyhasija/obsidian-plugin-skills
- https://github.com/C-Bjorn/MegaMem

---


