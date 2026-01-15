# How to Use the GitHub AI Issue Analyzer

Alright, let's get you up and running! Don't worry if you're not super technical - I'll walk you through everything step by step.

## Step 1: Make Sure Python is Installed

First things first, you need Python on your computer. Open your terminal (PowerShell on Windows) and type:

```bash
python --version
```

If you see something like `Python 3.10.x` or higher, you're good! If not, go download Python from [python.org](https://www.python.org/downloads/) and install it.

## Step 2: Get the Code

If you don't have the project yet, download it or clone it:

```bash
git clone <your-repo-url>
cd github-ai-issue-analyzer
```

Or just download the ZIP file and unzip it somewhere.

## Step 3: Install the Required Packages

This is where we install all the dependencies. Don't panic when you see a ton of stuff downloading - that's normal!

```bash
pip install -r requirements.txt
```

Grab a coffee ☕ - this might take a few minutes because it's downloading some pretty big AI models (like 500MB+). It's a one-time thing though!

**Note:** First person to run this: Yeah, it downloads a lot. The sentence transformer model and BART model are chunky. But once they're cached, you're golden.

## Step 4: Start the Server

Now let's fire up the server:

```bash
python -m uvicorn api.main:app --reload
```

You should see something like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

That means it's working! Leave this terminal window open - that's your server running.

## Step 5: Check If It's Working

Open your web browser and go to:

```
http://127.0.0.1:8000/
```

You should see a simple JSON message:

```json
{
  "message": "GitHub AI Issue Analyzer is running"
}
```

Cool! It's alive! 🎉

## Step 6: See the Interactive Docs

This is the fun part. Go to:

```
http://127.0.0.1:8000/docs
```

You'll see a fancy interactive API documentation page (Swagger UI). This is where you can test everything without writing any code.

## Step 7: Try Analyzing a Repository

Let's test it with a real GitHub repo. You have two ways to do this:

### Option A: Using Your Browser (Easy Way)

Just type this in your browser's address bar:

```
http://127.0.0.1:8000/analyze/facebook/react
```

Replace `facebook/react` with any GitHub owner/repo combination. For example:
- `microsoft/vscode`
- `nodejs/node`
- `tensorflow/tensorflow`

Wait a few seconds (the first request is slower because models are loading), and you'll get back a bunch of JSON with all the analyzed issues.

### Option B: Using the Swagger UI (Also Easy)

1. Go to `http://127.0.0.1:8000/docs`
2. Click on the `GET /analyze/{owner}/{repo}` endpoint
3. Click "Try it out"
4. Fill in the owner (like `facebook`) and repo (like `react`)
5. Click "Execute"
6. Scroll down to see the response

### Option C: Using curl (Command Line)

If you're comfortable with the command line:

```bash
curl http://127.0.0.1:8000/analyze/facebook/react
```

## Understanding the Response

Here's what you get back:

```json
{
  "total_issues": 18,
  "duplicates_found": 2,
  "issues": [
    {
      "id": 12345,
      "title": "App crashes on startup",
      "body": "When I open the app...",
      "url": "https://github.com/...",
      "classification": {
        "label": "bug",
        "confidence": 0.87
      },
      "priority": "high"
    }
  ],
  "duplicates": [
    {
      "issue_1": "App crashes on startup",
      "issue_2": "Application won't start",
      "similarity": 0.82
    }
  ]
}
```

Breaking it down:
- **total_issues**: How many issues it analyzed
- **duplicates_found**: How many potential duplicates it found
- **issues**: Array of all the issues with their AI analysis
  - **classification**: What type of issue (bug, feature, etc.) and how confident it is
  - **priority**: low, medium, or high
- **duplicates**: Pairs of issues that look similar

## Step 8: View Your Analysis History

Good news - every analysis is automatically saved! Let's check it out.

### Check Your Stats

See how many analyses you've run:

```
http://127.0.0.1:8000/stats
```

You'll get:
```json
{
  "total_analyses": 5,
  "message": "Analysis logging is active"
}
```

### View Recent History

See your last 10 analyses:

```
http://127.0.0.1:8000/history
```

Or see more:
```
http://127.0.0.1:8000/history?limit=20
```

You'll get:
```json
{
  "history": [
    {
      "timestamp": "2026-01-16T04:15:51.980180",
      "repository": "fastapi/fastapi",
      "total_issues": 1,
      "duplicates_found": 0
    },
    {
      "timestamp": "2026-01-16T03:50:22.123456",
      "repository": "microsoft/vscode",
      "total_issues": 18,
      "duplicates_found": 2
    }
  ],
  "total_analyses": 2
}
```

### Where Are the Files?

All your analysis logs are saved in the `data` folder:

```
data/
├── analysis_summary.jsonl          # Quick summary (one line per analysis)
└── logs/
    ├── fastapi_fastapi_20260116_041551.json     # Full results
    └── microsoft_vscode_20260116_035022.json    # Full results
```

**Why is this useful?**
- Review past analyses without re-running them
- Track which repos you analyze most
- Compare issue counts over time
- Build analytics dashboards later
- Keep an audit trail of your work

## Tips and Tricks

### The First Request is Slow
The very first time you analyze issues, it takes longer because:
1. It's downloading ML models from HuggingFace
2. Loading them into memory

After that, it's much faster!

### How Many Issues Does It Analyze?
It grabs the 30 most recent **open** issues from the repo. That's GitHub's default limit. If you want more, you'll need to modify the code.

### What About Rate Limits?
GitHub's API allows 60 requests per hour without authentication. If you hit that limit, you'll need to add a GitHub token (but that's a whole other story).

### Stop the Server
When you're done, go back to the terminal where the server is running and press `Ctrl+C`. That'll shut it down gracefully.

### Restart the Server
If you made changes to the code:
```bash
# Just run it again - the --reload flag makes it auto-reload anyway!
python -m uvicorn api.main:app --reload
```

## Common Issues

**"ModuleNotFoundError"**
- You probably forgot to install the requirements. Run `pip install -r requirements.txt`

**"Address already in use"**
- The server is already running somewhere. Either close it or use a different port:
  ```bash
  python -m uvicorn api.main:app --reload --port 8001
  ```

**"Failed to fetch issues"**
- The GitHub repo doesn't exist or you hit the rate limit. Try a different repo or wait an hour.

**Takes forever to respond**
- First request? Normal - models are loading. If it's still slow after that, your computer might be struggling with the ML models. They're pretty heavy!

## What's Next?

Once you've got the hang of it:
1. Try different repositories and see how it classifies issues
2. Check out the code in `api/main.py` to see how it works
3. Modify the priority rules in `models/priority_predictor.py`
4. Add your own classification categories
5. Build a simple frontend to make it prettier

## Still Stuck?

If something's not working:
1. Make sure Python 3.10+ is installed
2. Check that all dependencies installed successfully
3. Look at the terminal where the server is running - any error messages there?
4. Try restarting the server
5. When in doubt, Google the error message (we've all been there)

Happy analyzing! 🚀

---

P.S. - If you're getting good results and find this useful, feel free to share it with your team or adapt it for your own projects. That's what code is for!
