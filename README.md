# STK Manufacturing Challenge - My Solution

Hi! This is my submission for the Circonomit challenge. I approached the STK Produktion challenge as an opportunity to apply my expertise and tackle the tasks as presented.

## What I Actually Built vs. Designed

I decided to focus most of my time on getting Task 1 really solid since it felt like the foundation everything else would build on. Here's the honest breakdown:

**✅ Fully Implemented (Task 1):**
- Working simulation engine using LangGraph
- Handles STK's business model with realistic interdependencies  
- Cycle detection that actually deals with business feedback loops (like pricing→demand→volume→costs→pricing)
- Demo with energy price scenarios that STK would actually face

**📋 Designed but not coded (Tasks 3-4):**
- Natural language processing approach using specialized AI tools
- Business user interface design 
- Detailed my thinking process but didn't have time to implement

## My Technical Decisions

**Why LangGraph over simpler approaches?**
When I saw the requirement to "handle dependencies between attributes" and "pay attention to feedback loops," I realized this wasn't just about running calculations in order. STK's business model has natural cycles - energy prices affect production costs, which affect selling prices, which affect demand, which affects production volume, which affects unit costs. 

I needed something that could orchestrate: dependency resolution → cycle detection → iterative resolution → calculation → validation. LangGraph's StateGraph made this workflow natural to implement, and the built-in MemorySaver solved the "manage where overrides are stored" requirement without me having to build a storage system.

**The cycle resolution challenge:**
This was the most interesting technical problem. Most dependency systems just detect cycles and fail. But STK's business has legitimate feedback loops that need to converge on realistic values. I implemented iterative resolution using business logic - for example, if there's a pricing feedback loop, use seed values and iterate until the system stabilizes at market equilibrium.

**What I learned about industrial modeling:**
Working through STK's scenarios made me realize how much domain knowledge goes into these systems. Energy cost isn't just price × volume - there are efficiency factors, overhead allocations, capacity constraints. The technical challenge isn't just graph algorithms; it's encoding real business logic correctly.

## Quick Start

```bash
# Run the main demo
python task1_solution/run_task1_demo.py

# See detailed scenarios
python task1_solution/stk_demo.py
```

## The STK Business Model I Implemented

I modeled three interconnected business domains:

**Supply Chain:** Energy pricing (€0.15/kWh baseline), material costs (€25K), labor (€15K), CO₂ tariffs
**Production:** Volume optimization, energy consumption per unit (2.5 kWh), overhead factors (15%)  
**Market:** Cost-plus pricing (20% margin), demand elasticity, profit margin analysis

The interesting part is how they interact - energy price increases don't just add to costs linearly. They trigger pricing adjustments that affect demand, which changes production volume, which changes unit economics.

## What Works (and what doesn't)

**Works well:**
- Simulates realistic STK scenarios correctly
- Detects and resolves the pricing feedback loops I modeled
- Energy price volatility analysis shows expected business impact
- LangGraph workflow handles the complexity cleanly

**Known limitations:**
- Only tested with relatively simple cycles (complex multi-loop scenarios might not converge)
- Business logic is based on my assumptions about manufacturing economics, not validated data
- No real persistence beyond demo scenarios
- Dependency resolution is deterministic (real business has uncertainty)

**If I had more time:** I'd focus on the natural language processing piece (Task 3). I think that's where the real business value would be - letting STK stakeholders describe their business logic in natural language and automatically mapping it to the simulation model.

## My Approach to Tasks 3 & 4

Since I couldn't implement everything, I focused on documenting my thinking:

**Task 3 (Natural Language to Model):** I designed an approach using AI tools with domain expertise to extract business relationships from conversations and map them to STK's Block/Attribute structure. The key insight was handling ambiguity resolution - when someone says "energy affects costs," what exactly does that mean quantitatively?

**Task 4 (User Experience):** I designed a "business questions first" interface that hides the technical complexity. Instead of asking users to create Blocks and Attributes, start with "What business decision are you trying to make?" and guide them through model building conversationally.

## File Organization

```
task1_solution/     # The actual working implementation
├── stk_simulation.py     # Core engine with LangGraph workflow
├── stk_demo.py          # Realistic STK scenarios  
├── run_task1_demo.py    # Quick demo runner
└── [tests and docs]

task3_solution/     # My approach to natural language processing
task4_solution/     # My UX design thinking  
documentation/      # How all the tasks connect together
```

## What This Shows About My Thinking

I tend to focus on getting the core problem really solid rather than building many half-working pieces. The cycle resolution algorithm took me the most time because I wanted to understand how real business feedback loops behave, not just implement textbook graph algorithms.

I'm genuinely curious about industrial decision-making systems - the technical challenges are interesting, but what makes them hard is encoding real business logic correctly. STK's energy cost modeling taught me a lot about how manufacturing economics actually work.

If you want to see my detailed technical documentation, it's in `task1_solution/TASK1_SOLUTION.md`. For my thinking on the other tasks, check `task3_solution/` and `task4_solution/`.

## Next Steps I'd Take

1. **Validate the business model** - Test with real manufacturing data to see if my assumptions about cost structures and market dynamics are realistic
2. **Implement the NLP pipeline** - The AI-based approach I designed would let business users contribute domain knowledge in natural language
3. **Add uncertainty modeling** - Real business planning deals with ranges and probabilities, not point estimates
4. **Build the conversational interface** - Make it actually usable for non-technical stakeholders

Thanks for the interesting challenge! The STK scenario felt like a realistic industrial problem rather than a toy example. 