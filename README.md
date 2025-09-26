# Single File Simple Static Blog Generator

- Install UV https://docs.astral.sh/uv/getting-started/installation/ 
- Clone this repo (or simply copy `static.py`)


## Basic blog

```bash
mkdir myblog
echo "site_name = 'My Blog'" > myblog/config.toml
echo "# Hello World" > myblog/2025-01-31-hello-world.md
uv run static.py myblog public
```

## Custom template

```bash
mkdir myblog/templates
echo "<html> ... MY AWESOME JINJA for {{posts}} </html>" > myblog/templates/index.html
echo "<html> ... MY AWESOME JINJA for {{post}} </html>" > myblog/templates/post.html
uv run static.py myblog public
```

### template context

#### Global

```py
{"config": {"site_name": str}
```

#### index.html

A list of `Post` ordered by date desc

```py
{"posts": [{"title": str, "slug": str, "date": datetime, "text": str}]}
```

#### post.html

A single `Post`

```py
{"post": {"title": str, "slug": str, "date": datetime, "text": str}}
```




---

**Fork and customize**
