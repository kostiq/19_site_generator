from jinja2 import Template, Environment, FileSystemLoader, Markup
import json
import markdown
import os
import urllib
from urllib.parse import quote


def load_config(path_to_json):
    with open(path_to_json, 'r') as jsonfile:
        return json.load(jsonfile)


def markdown_filter(text):
    md = markdown.Markdown(extensions=['meta'])
    return Markup(md.convert(text))


def get_md_article(path_to_file):
    with open('articles/{}'.format(path_to_file)) as article_file:
        return article_file.read()


def get_html_article_path(path_to_article):
    return '{}.html'.format(path_to_article)


def write_html_article(html_article_file, html_article_path):
    with open(html_article_path, 'w') as article_html:
        article_html.write(html_article_file)


def create_html_article_dirs_if_not_exist(html_article_path):
    if not os.path.exists(html_article_path):
        os.makedirs(html_article_path)


def create_jinja_environment():
    env = Environment(
        loader=FileSystemLoader('.'),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True)
    env.filters['markdown'] = markdown_filter
    return env


def render_article_page(html_article, title):
    rendered_article_page = article_template.render(
        title=title, content=html_article)
    return rendered_article_page


def create_html_articles(config):
    for md_article in config['articles']:
        html_article_path = 'site/{}'.format(
            get_html_article_path(os.path.splitext(md_article['source'])[0]))

        create_html_article_dirs_if_not_exist(html_article_path)

        source_article = get_md_article(md_article['source'])

        write_html_article(
            html_article_file=render_article_page(
                source_article, md_article['title']),
            html_article_path=html_article_path)
    return 0


def get_config_with_html_articles(config):
    for md_article in config['articles']:
        html_article_path = get_html_article_path(
            os.path.splitext(md_article['source'])[0])
        md_article['source'] = html_article_path
    return config


def fill_main_page(article_dict):
    with open('site/index.html', 'w') as index:
        index.write(main_template.render(
            themes=article_dict['topics'], topics=article_dict['articles']))


if __name__ == '__main__':

    config = load_config('config.json')

    env = create_jinja_environment()
    article_template = env.get_template('/templates/article.html')
    main_template = env.get_template('/templates/main_page.html')

    create_html_articles(config)
    fill_main_page(get_config_with_html_articles(config))
