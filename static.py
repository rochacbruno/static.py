# /// script
# dependencies = ["jinja2", "mistune"]
# ///
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import mistune
import tomllib
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

TEMPLATES = {
    "index.html": '<h1>{{ config.site_name }}</h1><ul>{% for post in posts %}<li><a href="{{ post.slug }}.html">{{ post.title }}</a></li>{% endfor %}</ul>',
    "post.html": '<a href="./index.html">{{ config.site_name }}</a><article><p>{{ post.date.strftime("%Y-%m-%d") }}</p>{{ post.text|safe }}</article>',
}


@dataclass
class Config:
    site_name: str


@dataclass
class Post:
    title: str
    slug: str
    date: datetime
    text: str


def load_config(input_dir: Path) -> Config:
    try:
        with open(input_dir / "config.toml", "rb") as f:
            return Config(**tomllib.load(f))
    except FileNotFoundError:
        return Config(site_name="My Site")


def collect_posts(input_dir: Path) -> list[Post]:
    posts = []
    for file in input_dir.glob("*.md"):
        title, slug, date = parse_filename(file.name)
        with open(file, "r") as f:
            text = mistune.html(f.read())
        posts.append(Post(title=title, slug=slug, date=date, text=text))
    posts.sort(key=lambda post: post.date, reverse=True)
    return posts


def parse_filename(filename: str) -> tuple[str, str, datetime]:
    date_str, slug = filename[:10], filename[11:-3]
    date = datetime.strptime(date_str, "%Y-%M-%d")
    title = slug.replace("-", " ").title()
    return title, slug, date


def render_template(jinja_env: Environment, template: str, filename: Path, context: dict):
    try:
        jinja_template = jinja_env.get_template(template)
    except TemplateNotFound:
        jinja_template = Template(TEMPLATES[template])
    with open(filename, "w") as f:
        f.write(jinja_template.render(**context))


def generate_site(input_dir: Path, output_dir: Path, config: Config, posts: list[Post]):
    jinja_env = Environment(loader=FileSystemLoader(input_dir / "templates"))
    context = {"config": config}
    render_template(jinja_env, "index.html", output_dir / "index.html", {"posts": posts, **context})
    for post in posts:
        render_template(jinja_env, "post.html", output_dir / f"{post.slug}.html", {"post": post, **context})


if __name__ == "__main__":
    try:
        input_dir, output_dir = Path(sys.argv[1]), Path(sys.argv[2])
    except IndexError:
        print("Usage: uv run static.py <input_dir> <output_dir>")
        sys.exit(1)
    if not input_dir.exists():
        print(f"Input directory {input_dir} does not exist")
        sys.exit(1)
    output_dir.mkdir(parents=True, exist_ok=True)
    config = load_config(input_dir)
    posts = collect_posts(input_dir)
    generate_site(input_dir, output_dir, config, posts)
