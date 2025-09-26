Basic

```bash
mkdir blog
echo "site_name = 'My Blog'" > blog/config.toml
echo "# Hello World" > blog/2025-01-31-hello-world.md
uv run static.py blog public
```

Custom template

```bash
mkdir blog/templates
echo "<html> ... MY AWESOME JINJA for {{posts}} </html>" > blog/templates/index.html
echo "<html> ... MY AWESOME JINJA for {{post}} </html>" > blog/templates/post.html
uv run static.py blog public
```
