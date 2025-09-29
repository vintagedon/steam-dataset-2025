# [Phase/Sprint Name]: [Achievement Summary]

> **Session Date:** YYYY-MM-DD  
> **Status:** Complete | In Progress | Blocked  
> **Scripts Produced:** X production scripts | X config files | X SQL schemas  
> **Key Innovation:** [One-line technical achievement]

---

## Problem Statement

[2-3 sentences: What business/technical problem needed solving and why it mattered]

---

## Solution Overview

[2-3 sentences: What was built and how it solves the problem. Focus on the practical outcome.]

---

## What Was Built

### Quick Reference

| Artifact | Purpose | Key Feature |
|----------|---------|-------------|
| `script-name.py` | [Brief purpose] | [Standout capability] |
| `config-file.yml` | [Brief purpose] | [Standout capability] |
| `schema.sql` | [Brief purpose] | [Standout capability] |

---

### Script 1: `script-name.py`

**Purpose:** [What this script accomplishes]

**Key Capabilities:**

- Feature/capability 1
- Feature/capability 2
- Feature/capability 3

**Usage:**

```bash
python script-name.py [args]
````

**Dependencies:** [Required packages if noteworthy]

**Performance Notes:** [Relevant metrics, timing, scale achieved]

<details>
<summary>Execution Output</summary>

```bash
[Terminal output from successful run - show the key parts that demonstrate success]
```

</details>

---

### Script 2: `another-script.py`

**Purpose:** [What this script accomplishes]

**Key Capabilities:**

- Feature/capability 1
- Feature/capability 2
- Feature/capability 3

**Usage:**

```bash
python another-script.py [args]
```

**Dependencies:** [Required packages if noteworthy]

**Performance Notes:** [Relevant metrics, timing, scale achieved]

<details>
<summary>Execution Output</summary>

```bash
[Terminal output from successful run]
```

</details>

---

### Configuration: `config-file.yml`

**Purpose:** [What this configuration controls]

**Key Settings:**

- Setting 1: [Purpose]
- Setting 2: [Purpose]

<details>
<summary>Configuration Details</summary>

```yaml
[Configuration file content]
```

</details>

---

### Schema: `schema.sql`

**Purpose:** [What this schema defines]

**Key Tables/Structures:**

- Table 1: [Purpose]
- Table 2: [Purpose]

<details>
<summary>Schema Definition</summary>

```sql
[SQL schema content]
```

</details>

---

## Technical Approach

### Architecture Decisions

**[Decision Name]:** [Why this approach was chosen, what alternatives were considered, what trade-offs were made]

**[Decision Name]:** [Why this approach was chosen, what alternatives were considered, what trade-offs were made]

**[Decision Name]:** [Why this approach was chosen, what alternatives were considered, what trade-offs were made]

### Key Implementation Patterns

1. **[Pattern Name]:** [How it was implemented and what value it provides]
2. **[Pattern Name]:** [How it was implemented and what value it provides]
3. **[Pattern Name]:** [How it was implemented and what value it provides]

### Technical Innovations

- [Novel approach or solution developed during this session]
- [Clever workaround or optimization discovered]
- [Reusable component or pattern created]

---

## Validation & Results

### Success Metrics

- ✅ **[Metric Name]:** [Result achieved]
- ✅ **[Metric Name]:** [Result achieved]
- ✅ **[Metric Name]:** [Result achieved]

### Performance Benchmarks

| Metric   | Target | Achieved | Notes     |
| -------- | ------ | -------- | --------- |
| [Metric] | [Goal] | [Result] | [Context] |
| [Metric] | [Goal] | [Result] | [Context] |

### Data Quality Checks

[If applicable - validation queries run, integrity checks performed, etc.]

---

## Integration Points

**Database:** [Connection requirements, credentials handling, which database/schema]

**File System:** [Data locations, input/output paths, file operations performed]

**External APIs:** [Any API integrations and their configuration]

**Other Scripts:** [Dependencies on other project scripts or components]

---

## Usage Guide

### Prerequisites

```bash
# Required packages
package-name>=version
another-package>=version

# Environment variables
VARIABLE_NAME=description
ANOTHER_VAR=description

# System requirements
[OS, hardware, database version, etc.]
```

### Running the Scripts

**Step 1: [First Operation]**

```bash
python script-1.py [args]
```

[Expected outcome or what this accomplishes]

**Step 2: [Second Operation]**

```bash
python script-2.py [args]
```

[Expected outcome or what this accomplishes]

**Step 3: [Third Operation]**

```bash
python script-3.py [args]
```

[Expected outcome or what this accomplishes]

### Verification

[How to confirm everything worked correctly]

```bash
# Verification command
command-to-check-results
```

[What successful output should look like]

---

## Lessons Learned

### Challenges Overcome

| Challenge             | Root Cause        | Solution            | Technical Approach |
| --------------------- | ----------------- | ------------------- | ------------------ |
| [Problem encountered] | [Why it happened] | [How it was solved] | [Method/tool used] |
| [Problem encountered] | [Why it happened] | [How it was solved] | [Method/tool used] |
| [Problem encountered] | [Why it happened] | [How it was solved] | [Method/tool used] |

### Technical Insights

- [Key technical learning or discovery from this session]
- [Important insight about tools, libraries, or approaches]
- [Performance characteristic or limitation discovered]

### Process Insights

- [What worked well in the development approach]
- [Collaboration pattern that proved efficient]
- [Time-saving technique or workflow improvement]

### Reusable Components

- **[Component Name]:** [What it does and where it can be reused]
- **[Component Name]:** [What it does and where it can be reused]

---

## Next Steps

### Immediate Actions

1. [Clear next step with specific outcome]
2. [Clear next step with specific outcome]
3. [Clear next step with specific outcome]

### Enhancement Opportunities

**Short-term:** [Improvements that could be made quickly]

**Medium-term:** [Larger enhancements requiring more effort]

**Long-term:** [Strategic improvements or major architectural changes]

---

## Session Metadata

**Development Environment:** [Python version, OS, key tools]
**Total Development Time:** ~X hours
**Session Type:** [Production Development | Rapid Prototyping | Debugging | Analysis]
**Code Version:** All scripts v1.X - production ready

---

**Related Worklogs:** [Links to previous or related sessions if applicable]

---

## Template Usage Notes

### When to Use Which Sections

**Always Include:**

- Problem Statement
- Solution Overview
- What Was Built (with at least Quick Reference table)
- Technical Approach
- Validation & Results
- Session Metadata

**Include When Relevant:**

- Integration Points (if scripts interact with external systems)
- Usage Guide (if scripts are meant to be run by others)
- Lessons Learned (always valuable but especially when challenges were overcome)
- Next Steps (if this is part of ongoing work)

### Adaptive Patterns

**For Single-Script Sessions:**

- Skip the Quick Reference table
- Go straight into the single script section
- Keep Technical Approach focused and concise

**For Multi-Script Sessions (4+ scripts):**

- Quick Reference table is essential for navigation
- Consider adding a brief "Script Interaction Flow" paragraph after the table explaining execution order
- Each script gets its own full section with collapsible output

**For Pure Analysis Sessions (No Scripts):**
Replace "What Was Built" with:

```markdown
## Analysis Conducted

### Research Questions
1. [Question being investigated]
2. [Question being investigated]

### Methodology
[Approach taken for the analysis]

### Key Findings
- **Finding 1:** [Details and implications]
- **Finding 2:** [Details and implications]

<details>
<summary>Complete Analysis Output</summary>

[Full report content, query results, or data analysis]
</details>
````

**For Schema/Configuration-Heavy Sessions:**

- Group all schemas together in one section
- Group all configs together in another section
- Show relationships between artifacts in Technical Approach

### Style Guidelines

**Terminal Outputs:**

- Show enough to prove success (key metrics, final summary)
- Trim repetitive middle sections but indicate with [...] or similar
- Always show any error handling or validation messages
- Keep outputs authentic - copy/paste actual terminal text

**Code Blocks:**

- Use syntax highlighting (python, bash, sql, yaml)
- Include comments in code snippets when helpful for understanding
- Show realistic examples, not placeholder values

**Tables:**

- Use for Quick Reference, metrics, comparisons, challenges
- Keep rows scannable - brevity is key
- Align information logically (inputs → outputs, problem → solution)

**Tone:**

- Professional but accessible
- Focus on what was accomplished, not the struggle
- Technical precision without jargon overload
- Practical emphasis on "how to use" rather than "how built"

### Collapsible Sections Best Practices

**Use `<details>` for:**

- Full terminal outputs
- Complete configuration files
- SQL schemas
- Long lists or data that adds depth but isn't essential for scanning

**Keep visible:**

- Key metrics and results
- Usage commands
- High-level architecture decisions
- Success indicators
