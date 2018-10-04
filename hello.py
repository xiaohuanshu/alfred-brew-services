#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow3, ICON_WARNING

ICON_MAP = {
    "stopped": "red.png",
    "started": "green.png",
}


def get_services_data():
    import os
    lines = os.popen('/usr/local/bin/brew services list').read().split("\n")
    item_lines = lines[1:]
    services = []
    for l in item_lines:
        try:
            service_name = l.split()[0]
            service_status = l.split()[1]
            services.append(
                {'name': service_name, 'status': service_status, 'icon': ICON_MAP[service_status]})
        except:
            break
    return services


def key_for_filter(item):
    return item['name']


ACTION_DATA = [
    {"name": 'run', "info": "Run the service %s without starting at login",
        "icon": "icon.png"},
    {"name": 'start', "info": "Start the service %s immediately and register it to launch at login", "icon": "icon.png"},
    {"name": 'stop', "info": "Stop the service %s immediately and unregister it from launching at login", "icon": "icon.png"},
    {"name": 'restart', "info": "Stop and start the service %s immediately and register it to launch at login", "icon": "icon.png"},
]


def main(wf):
    query_string = wf.args[0] if len(wf.args) else None
    if " " in query_string:
        query, action_query = query_string.split(" ")
    else:
        query = query_string
        action_query = None
    log.info(query)
    log.info(action_query)
    services = wf.cached_data('services_data', get_services_data, max_age=5)
    items = wf.filter(query, services, key_for_filter)
    if not items:
        wf.add_item('No matches', icon=ICON_WARNING)
    if len(items) == 1 and query == items[0]['name']:
        actions = wf.filter(action_query, ACTION_DATA, key_for_filter)
        item = items[0]
        for action in actions:
            wf.add_item(title=item['name']+" "+action['name'],
                        subtitle=action['info'] % item['name'],
                        arg=action['name']+" "+item['name'],
                        autocomplete=item['name']+" "+action['name'],
                        valid=True,
                        icon=action['icon']
                        )
    else:
        for item in items:
            wf.add_item(title=item['name'],
                        subtitle=item['status'],
                        arg="run "+item['name'],
                        autocomplete=item['name'],
                        valid=True,
                        icon=item['icon']
                        )
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3(update_settings={
        'github_slug': 'xiaohuanshu/alfred-brew-services',
        'frequency': 7,
    })
    if wf.update_available:
        wf.start_update()
    log = wf.logger
    sys.exit(wf.run(main))
