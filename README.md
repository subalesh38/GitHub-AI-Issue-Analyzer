# GitHub AI Issue Analyzer

Hey there! 👋

So you know how managing GitHub issues can be a total pain? Especially when you've got hundreds of them piling up, half of them are duplicates, and you're just trying to figure out which ones are actually urgent? Yeah, we've all been there.

That's exactly why I built this tool. It uses AI to automatically analyze GitHub issues and tells you:
- What type of issue it is (bug, feature request, documentation, etc.)
- How important it is (low, medium, high priority)
- If you've seen this issue before (duplicate detection)

Think of it as your personal assistant that reads through all your GitHub issues and gives you the TL;DR version with smart insights.

**Bonus**: Every analysis is automatically saved to the `data` folder, so you can track your usage and review past results anytime!

## What Does It Actually Do?

When you point this tool at any GitHub repository, here's what happens:

1. **Grabs the issues** - It fetches up to 30 open issues from the repo
2. **Reads them** - The AI actually reads the titles and descriptions
3. **Classifies them** - Tells you if it's a bug, feature request, question, or documentation issue
4. **Prioritizes them** - Figures out which ones need your attention ASAP
5. **Finds duplicates** - Uses semantic similarity to catch duplicate issues (even if they're worded differently)

All of this happens in seconds, and you get back a nice JSON response with all the insights.

## Tech Stack (For the Curious)

- **FastAPI** - Because it's fast and makes building APIs actually enjoyable
- **Sentence Transformers** - For that sweet semantic similarity magic
- **BART Model** - Facebook's zero-shot classifier that doesn't need training data
- **Scikit-learn** - For the cosine similarity math stuff
- **Uvicorn** - The server that runs everything

Yeah, there's some heavy ML going on under the hood, but you don't need to worry about that. It just works.

## Quick Start

Want to try it out? Here's the fastest way:

```bash
# 1. Install the dependencies
pip install -r requirements.txt

# 2. Start the server
python -m uvicorn api.main:app --reload

# 3. Open your browser
http://127.0.0.1:8000/docs
```

That's it! Now you can test it out with any GitHub repo.

## Real World Example

Let's say you want to analyze issues from Microsoft's VS Code repository:

```
http://127.0.0.1:8000/analyze/microsoft/vscode
```

Wait a few seconds (the AI is doing its thing), and boom - you'll get back something like:

```json
{
  "total_issues": 18,
  "duplicates_found": 0,
  "issues": [
    {
      "title": "Editor crashes when opening large files",
      "classification": {
        "label": "bug",
        "confidence": 0.92
      },
      "priority": "high"
    }
  ]
}
```

Pretty neat, right?

## Automatic Logging

Every analysis you run is automatically saved! Check out your history:

```bash
# See your analysis history
http://127.0.0.1:8000/history

# Check total analyses run
http://127.0.0.1:8000/stats
```

**What gets logged:**
- Full analysis results in `data/logs/{owner}_{repo}_{timestamp}.json`
- Summary log in `data/analysis_summary.jsonl`
- Timestamps, issue counts, and duplicate counts

This is super useful for:
- Tracking which repos you analyze most
- Comparing results over time
- Reviewing past analyses without re-running them
- Building analytics dashboards later

## Why Would I Use This?

Good question! Here are some real scenarios:

- **You're a maintainer** drowning in issues and need to prioritize what to work on
- **You're triaging** and want to quickly categorize incoming issues
- **You're looking for duplicates** but don't want to manually read through 500 issues
- **You're curious** about what kinds of issues your repo gets most often
- **You want to automate** part of your issue management workflow

## Important Notes

- The tool fetches **30 issues at a time** (GitHub API default)
- It only looks at **open issues** (not closed ones)
- Pull requests are filtered out (GitHub counts PRs as issues, but we ignore them)
- First run might be slow because it downloads the ML models (they're cached after that)

## What's Next?

This is a solid starting point, but there's tons more you could do:
- Add GitHub authentication for higher rate limits
- Store results in a database
- Build a web UI for it
- Fine-tune the models on your specific repos
- Add more classification categories
- Implement issue assignment suggestions

Feel free to hack on it and make it your own!

## Need Help?

Check out the `HOW_TO_USE.md` file for a detailed step-by-step guide.

Got questions or found a bug? Well... you could create a GitHub issue about it. Meta, right? 😄

---

Built with ☕ and a lot of curiosity about what AI can actually do for developers.
