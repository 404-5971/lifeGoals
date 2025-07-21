# LifeGoals

## Running the Project with uv

This project uses [uv](https://github.com/astral-sh/uv) for dependency management and running the app.

1. **Install uv** (if you don't have it):
   ```bash
   pip install uv
   ```
2. **Install dependencies:**
   ```bash
   uv sync  # or use pyproject.toml if specified
   ```
3. **Run the app:**
   ```bash
   uv run src/main.py
   ```
4. **Open the app in your browser:**
   ```bash
   open http://localhost:5000
   ```

---

## How to Write Your Goals

To add your goals, edit the `lifeGoals.txt` file in the following format:

- Group your goals by category. Each category starts with its name in square brackets, e.g. `[Personal]`, `[Career]`, `[Health]`, etc.
- List each goal on a new line under its category.
- Leave a blank line between categories for readability (optional but recommended).

### Example

```
[Personal]
Travel to a new country
Learn a new language
Read 12 books in a year

[Career]
Get a promotion
Start a side business
Complete a professional certification

[Health]
Run a marathon
Eat vegetables daily
Exercise three times a week

[Finance]
Save $5,000
Create a monthly budget
Invest in stocks
```

- You can add as many categories and goals as you like.
- Make sure each category is unique and clearly labeled.
