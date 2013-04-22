import collections
import datetime
import itertools
import os
import re
import shutil

import jinja2
import yaml

from docutils.core import publish_parts


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'output')
OUTPUT_STATIC_DIR = os.path.join(OUTPUT_DIR, 'static')
POSTS_DIR = os.path.join(PROJECT_DIR, 'posts')
TEMPLATES_DIR = os.path.join(PROJECT_DIR, 'templates')
JINJA = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
    bytecode_cache=jinja2.FileSystemBytecodeCache(),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)


def makedirs(filename):
    dirname = os.path.dirname(filename)
    try:
        os.makedirs(dirname)
    except os.error:
        pass


def write(filename, data):
    makedirs(filename)
    with open(filename, 'w') as f:
        f.write(data)
        f.flush()


def slugify(name):
    return re.sub(r'\W+', '-', name.lower())
JINJA.globals['slugify'] = slugify


def metadata_to_url(metadata):
    return '/blog/%s/%s/%s/%s/' % (
        str(metadata['date'].year).zfill(2),
        str(metadata['date'].month).zfill(2),
        str(metadata['date'].day).zfill(2),
        metadata['slug'],
    )
JINJA.globals['metadata_to_url'] = metadata_to_url


def split_post_metadata(data):
    line_count = 0
    metadata_lines = []
    rst_lines = []
    for line in data.splitlines():
        if line_count >= 2:
            rst_lines.append(line)
        else:
            metadata_lines.append(line)
        if line.startswith('---'):
            line_count += 1
    return '\n'.join(metadata_lines[1:-1]), '\n'.join(rst_lines)


def annotate_metadata(filename, metadata):
    slug = os.path.splitext(os.path.split(filename)[-1])[0][11:]
    metadata['slug'] = slug
    metadata['url'] = '/blog/%s/%s/%s/%s/' % (
        str(metadata['date'].year).zfill(2),
        str(metadata['date'].month).zfill(2),
        str(metadata['date'].day).zfill(2),
        slug,
    )


def parse_post(filename, data):
    raw_metadata, rst = split_post_metadata(data)
    metadata = yaml.load(raw_metadata)
    annotate_metadata(filename, metadata)
    rst_rendered = publish_parts(
        rst,
        writer_name='html',
        settings_overrides={'syntax_highlight': 'short'},
    )['html_body'].replace('<h1>', '<h4>').replace('</h1>', '</h4>')
    template = JINJA.get_template('item.html')
    rendered = template.render(metadata=metadata, rst_rendered=rst_rendered)
    return metadata, rendered


def posts():
    for filename in sorted(os.listdir(POSTS_DIR)):
        if not filename.endswith('.rst'):
            continue
        filename = os.path.join(POSTS_DIR, filename)
        with open(filename, 'r') as f:
            metadata, rendered = parse_post(filename, f.read().strip())
            yield metadata, rendered


def group_by_year(posts):
    key_func = lambda p: p['metadata']['date'].year
    grouped = []
    for year, group in itertools.groupby(posts, key_func):
        grouped.append((year, list(group)))
    return grouped


def main():
    everything = []
    categories = collections.defaultdict(lambda: [])

    redirect_template = JINJA.get_template('redirect.html')
    archive_template = JINJA.get_template('archive.html')
    post_template = JINJA.get_template('post.html')
    index_template = JINJA.get_template('index.html')
    atom_template = JINJA.get_template('atom.xml')

    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    makedirs(OUTPUT_DIR)
    shutil.copytree(STATIC_DIR, OUTPUT_STATIC_DIR)

    for metadata, rendered in posts():
        if not metadata.get('published', False):
            continue

        print 'Rendering %s' % (metadata['slug'],)
        everything.insert(0, {'metadata': metadata, 'rendered': rendered})

        category_list = metadata.get('categories', []) or []
        for category in category_list:
            category_slug = slugify(category)
            categories[category_slug].append({
                'metadata': metadata,
                'rendered': rendered,
                'category': category,
                'category_slug': category_slug,
            })

        rendered_post = post_template.render(post=rendered, metadata=metadata)
        post_filename = os.path.join(
            OUTPUT_DIR,
            metadata['url'].lstrip('/'),
            'index.html',
        )
        write(post_filename, rendered_post)

        rendered_redirect = redirect_template.render(url=metadata['url'])
        for alias in metadata.get('alias', []):
            alias = alias.lstrip('/')
            redirect_filename = os.path.join(OUTPUT_DIR, alias, 'index.html')
            write(redirect_filename, rendered_redirect)

    rendered_archive = archive_template.render(
        title='Blog Archive',
        posts=group_by_year(everything),
        archives=True,
    )
    archive_filename = os.path.join(OUTPUT_DIR, 'blog/archives/index.html')
    write(archive_filename, rendered_archive)

    rendered_index = index_template.render(posts=everything, home=True)
    write(os.path.join(OUTPUT_DIR, 'index.html'), rendered_index)

    rendered_atom = atom_template.render(
        posts=everything,
        now=datetime.datetime.utcnow(),
    )
    write(os.path.join(OUTPUT_DIR, 'atom.xml'), rendered_atom)

    for category_slug, category_posts in categories.iteritems():
        rendered_category = archive_template.render(
            title='Category: %s' % (category_posts[0]['category'],),
            posts=group_by_year(category_posts),
            archives=False,
        )
        category_filename = os.path.join(
            OUTPUT_DIR,
            'blog',
            'categories',
            category_slug,
            'index.html',
        )
        write(category_filename, rendered_category)

if __name__ == '__main__':
    main()
