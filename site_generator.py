from jinja2 import Template, Environment, FileSystemLoader, Markup
import json
import markdown
import os


def load_config(path_to_json):
    with open(path_to_json, 'r') as jsonfile:
        return json.load(jsonfile)


def convert_markdown_to_html(article):
    return markdown.markdown(article, output_format='html5')


def markdown_filter(text):
    md = markdown.Markdown(extensions=['meta'])
    return Markup(md.convert(text))


def open_markdown_article_from_file(md_article):
    with open('articles/{0}'.format(md_article['source'])) as article_file:
        article_file = article_file.read()
        return article_file


def get_html_article_path(md_article):
    return 'site/{0}.html'.format(os.path.splitext(md_article['source'])[0])


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


def prepare_files(config):
    for md_article in config['articles']:
        html_article_path = get_html_article_path(md_article)

        create_html_article_dirs_if_not_exist(html_article_path)

        html_article = convert_markdown_to_html(
            open_markdown_article_from_file(md_article))

        write_html_article_to_file(
            render_article_page(html_article, md_article['title']), html_article_path)

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

    fill_content_main_page(prepare_files(config))
