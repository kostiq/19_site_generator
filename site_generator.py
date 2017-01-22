from jinja2 import Template
import json


def load_config(path_to_json):
    with open(path_to_json, 'r') as jsonfile:
        return json.load(jsonfile)


def content_main_page(article_dict):
    html = open('template.html').read()
    template = Template(html)
    with open('index.html', 'w') as index:
        index.write(template.render(
            themes=article_dict['topics'], topics=article_dict['articles']))


if __name__ == '__main__':
#    for item in load_config('config.json'):
#        print (item)
    print (content_main_page(load_config('config.json')))
