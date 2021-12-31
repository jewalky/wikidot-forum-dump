import logger
import sys
import config
import json
import logging
import codecs
import re
import helpers
import os
from bs4 import BeautifulSoup
import threading
import time


logging.info('Initializing...')


wikidot_site = config.wikidot_wiki


if __name__ != '__main__':
    print('Wrong execution')
    sys.exit(1)


def check_cached_json(location, function):
    if os.path.exists(location):
        logging.info('Cached: %s' % location)
        with codecs.open(location, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        logging.info('Processing: %s' % location)
        j = function()
        with codecs.open(location, 'w', encoding='utf-8') as f:
            json.dump(j, f)
        return j


def parse_posts_from(soup, node):
    # node = post-container
    post = node.find(class_='post', recursive=False)
    replies = node.find_all(class_='post-container', recursive=False)

    avatar = post.select('.head .info img')[0]

    post_title = post.select('.head .title')[0].text.strip()
    post_user_avatar = avatar['src']
    post_user_name = avatar['alt']
    try:
        post_user_id = int(re.match(r'.*u=(\d+)\)', avatar['style'])[1])
    except:
        post_user_id = -1
    post_user = {'avatar': post_user_avatar, 'name': post_user_name, 'id': post_user_id}
    post_date = int([x[5:] for x in post.select('.head .odate')[0]['class'] if x[0:5] == 'time_'][0])

    post_content = post.select('.content')[0].decode_contents().strip()

    post_replies = []
    if replies is not None:
        for sub_node in replies:
            try:
                cls = sub_node['class']
            except:
                cls = None
            if cls != ['post-container']:
                continue
            post_replies.append(parse_posts_from(soup, sub_node))

    post = {'user': post_user, 'date': post_date, 'title': post_title, 'replies': post_replies, 'content': post_content}
    return post


def get_thread_page(thread: int, page: int, wikidot_site: str):
    data = {'t': thread, 'moduleName': 'forum/ForumViewThreadPostsModule', 'pageNo': page}
    return helpers.fetch(data, wikidot_site)


def get_forum_thread(id, add_attrs = {}):
    # #thread-container-posts > .post-container and recurse
    haystack = helpers.fetch({'t': id, 'moduleName': 'forum/ForumViewThreadModule'}, wikidot_site)
    soup = BeautifulSoup(haystack, 'html.parser')
    title_raw = soup.find(class_='description-block').find_all('a')[-1]
    description_raw = soup.find(class_='description-block')
    statistics = description_raw.find(class_='statistics')

    try:
        avatar = statistics.select('.avatarhover img')[0]
    except:
        avatar = None

    if avatar is not None:
        thread_user_avatar = avatar['src']
        thread_user_name = avatar['alt']
        try:
            thread_user_id = int(re.match(r'.*u=(\d+)\)', avatar['style'])[1])
        except:
            thread_user_id = -1
        thread_user = {'avatar': thread_user_avatar, 'name': thread_user_name, 'id': thread_user_id}
    else:
        thread_user = None

    thread_date = int([x[5:] for x in statistics.select('.odate')[0]['class'] if x[0:5] == 'time_'][0])

    thread_description = ''
    for node in description_raw:
        try:
            if node['class'] == ['statistics'] or node['class'] == ['head']:
                continue
        except:
            pass
        thread_description += node.decode_contents() if hasattr(node, 'decode_contents') else str(node)

    thread_description = thread_description.strip()
    thread_base_page_id = None
    if title_raw is not None and title_raw['href'][0:6] != '/feed/':
        thread_base_page_id = title_raw['href'][1:]
    bc_raw = soup.find(class_='forum-breadcrumbs')
    bc_links = bc_raw.find_all('a')
    # <a href="/forum/c-171669/obsuzdenie-otdelnyh-stranic">
    thread_category = int(bc_links[1]['href'].split('/')[2].split('-')[1])
    thread_breadcrumbs = [x.strip() for x in bc_raw.text.split('»')]

    # handle pages
    max_pages = 1
    try:
        max_pages = int(re.match(r'page (\d+) of (\d+)', soup.select('.pager .pager-no')[0].text.strip())[2])
    except:
        pass

    thread_posts = []

    for page in range(max_pages):
        haystack = get_thread_page(thread=id, page=page+1, wikidot_site=wikidot_site)
        soup = BeautifulSoup(haystack, 'html.parser')

        logging.info('Thread: %d, Page: %d', id, page+1)

        for sub_node in soup:
            try:
                cls = sub_node['class']
            except:
                cls = None
            if cls != ['post-container']:
                continue
            thread_posts.append(parse_posts_from(soup, sub_node))

    thread = {'posts': thread_posts,
              'breadcrumbs': thread_breadcrumbs,
              'category': thread_category,
              'base_page_id': thread_base_page_id,
              'description': thread_description,
              'user': thread_user,
              'date': thread_date}

    for k in add_attrs:
        thread[k] = add_attrs[k]

    return thread


def get_forum_categories():
    haystack = helpers.fetch({'hidden': 'true', 'moduleName': 'forum/ForumStartModule'}, wikidot_site)
    soup = BeautifulSoup(haystack, 'html.parser')

    forum_groups = []

    groups = soup.find_all(class_='forum-group')
    for group in groups:
        group_title = group.find(class_='title').text.strip()
        group_description = group.find(class_='description').text.strip()
        group_categories = []
        categories = group.select('table tr')[1:]
        for category in categories:
            title_base = category.find(class_='title').find('a')
            category_description = category.find(class_='description').text.strip()
            category_title = title_base.text.strip()
            # /forum/c-186234/struktura-filiala
            category_id = int(title_base['href'].split('/')[2].split('-')[1])
            group_categories.append({'title': category_title, 'description': category_description, 'id': category_id})
        forum_groups.append({'title': group_title, 'description': group_description, 'categories': group_categories})

    return forum_groups


def get_forum_category(id):
    haystack = helpers.fetch({'c': id, 'p': 1, 'moduleName': 'forum/ForumViewCategoryModule'}, wikidot_site)
    soup = BeautifulSoup(haystack, 'html.parser')
    # handle pages
    max_pages = 1
    try:
        max_pages = int(re.match(r'page (\d+) of (\d+)', soup.select('.pager .pager-no')[0].text.strip())[2])
    except:
        pass

    category_threads = []

    pages_all = list(range(max_pages))
    threads_all = []
    lock = threading.RLock()

    def page_processor():
        nonlocal category_threads
        nonlocal pages_all
        while True:
            lock.acquire()
            if pages_all:
                page = pages_all[0]
                pages_all = pages_all[1:]
            else:
                page = None
            lock.release()
            if page is None:
                break

            haystack = helpers.fetch({'c': id, 'p': page + 1, 'moduleName': 'forum/ForumViewCategoryModule'}, wikidot_site)
            soup = BeautifulSoup(haystack, 'html.parser')
            logging.info('Category: %d, Page: %d', id, page + 1)

            ct = []

            threads_on_page = soup.select('table tr .title a')
            for thread_on_page in threads_on_page:
                # /forum/t-14009954/a-knopka-nabludatelej-v-opciah-cto-delaet
                thread_id = int(thread_on_page['href'].split('/')[2].split('-')[1])
                ct.append(thread_id)

            lock.acquire()
            category_threads += ct
            lock.release()

    for i in range(config.threads):
        t = threading.Thread(target=page_processor)
        t.daemon = True
        t.start()
        threads_all.append(t)

    while True:
        any_alive = bool([x for x in threads_all if x.is_alive()])
        if not any_alive:
            break
        time.sleep(1)

    return category_threads


if not os.path.exists('./dump/categories'):
    os.makedirs('./dump/categories')
if not os.path.exists('./dump/threads'):
    os.makedirs('./dump/threads')

categories = check_cached_json('./dump/categories.json', get_forum_categories)

total_threads = 0
all_thread_list = []

for group in categories:
    for category in group['categories']:
        category['threads'] = check_cached_json('./dump/categories/%d.json' % category['id'], lambda: get_forum_category(category['id']))
        all_thread_list += [{'category_id': category['id'], 'thread_id': x} for x in category['threads']]
        total_threads += len(category['threads'])

parsed_threads = 0
thread_lock = threading.RLock()


def thread_processor():
    global parsed_threads
    global all_thread_list

    while True:
        thread_lock.acquire()
        if all_thread_list:
            task = all_thread_list[0]
            all_thread_list = all_thread_list[1:]
        else:
            task = None
        thread_lock.release()
        if task is None:
            break # all done
        check_cached_json('./dump/threads/%d.json' % task['thread_id'], lambda: get_forum_thread(task['thread_id'], {'category': task['category_id']}))
        thread_lock.acquire()
        parsed_threads += 1
        logging.info('Threads: %d / %d', parsed_threads, total_threads)
        thread_lock.release()


processing_threads = []
for i in range(config.threads):
    t = threading.Thread(target=thread_processor)
    t.daemon = True
    t.start()
    processing_threads.append(t)


# make sure we can still exit with ctrl+c. all threads are daemon (will force-close)
while True:
    any_alive = bool([x for x in processing_threads if x.is_alive()])
    if not any_alive:
        break
    time.sleep(1)

logging.info('Complete.')
