from jinja2 import Template, Environment, FileSystemLoader, Markup
import json
import markdown
import os
import urllib
from urllib.parse import quote

WAY_TO_MD_ARTICLE = 'articles/{}'
WAY_TO_HTML_ARTICLE = 'site/{}.html'


def load_config(path_to_json):
    with open(path_to_json, 'r') as jsonfile:
        return json.load(jsonfile)


def markdown_filter(text):
    md = markdown.Markdown(extensions=['meta'])
    return Markup(md.convert(text))


def open_markdown_article_from_file(md_article):
    with open(WAY_TO_MD_ARTICLE.format(md_article['source'])) as article_file:
        article_file = article_file.read()
        return article_file


def get_html_article_path(md_article):
    return WAY_TO_HTML_ARTICLE.format(quote(os.path.splitext(md_article['source'])[0]))


def write_html_article_to_file(html_article_file, html_article_path):
    with open(html_article_path, 'w') as article_html:
        article_html.write(html_article_file)


def create_html_article_dirs_if_not_exist(html_article_path):
    if not os.path.exists(os.path.dirname(html_article_path)):
        os.makedirs(os.path.dirname(html_article_path))


def create_jinja_environment():
    env = Environment(loader=FileSystemLoader(
        '.'), trim_blocks=True, lstrip_blocks=True, autoescape=True)
    env.filters['markdown'] = markdown_filter
    return env


def render_article_page(html_article, title):
    rendered_article_page = article_template.render(
        title=title, content=html_article)
    return rendered_article_page


def get_config_with_html_articales(config):
    for md_article in config['articles']:
        html_article_path = get_html_article_path(md_article)

        create_html_article_dirs_if_not_exist(html_article_path)

        article = open_markdown_article_from_file(md_article)

        write_html_article_to_file(
            render_article_page(article, md_article['title']), html_article_path)

        md_article['source'] = html_article_path
    return config


def fill_content_main_page(article_dict):
    with open('index.html', 'w') as index:
        index.write(main_template.render(
            themes=article_dict['topics'], topics=article_dict['articles']))


if __name__ == '__main__':

    config = load_config('config.json')

    env = create_jinja_environment()
    article_template = env.get_template('/templates/article.html')
    main_template = env.get_template('/templates/template.html')

    fill_content_main_page(get_config_with_html_articales(config))
