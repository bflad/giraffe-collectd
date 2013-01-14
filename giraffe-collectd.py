#!/usr/bin/env python

import pprint
import re
import shutil
import os
import yaml


with open('giraffe-collectd.yaml') as configuration_file:
    configuration = yaml.safe_load(configuration_file)
configuration_file.closed

giraffe_dashboard_file = os.path.join(configuration['giraffe']['dashboard'], 'dashboards.js')
graphite_collectd_dir = os.path.join(configuration['graphite']['storage'], configuration['graphite']['prefix'])

def metric_server_target(metric_path):
    return metric_target(os.path.dirname(metric_path))

def metric_target(metric_path):
    return metric_path.replace(configuration['graphite']['storage'] + '/', '').replace('/', '.').replace('.wsp', '')

def metric_type(metric_filename):
    return re.sub('^.*(-|_)', '', metric_filename).replace('.wsp', '')

def cpu(metric_dir):
    c = os.path.basename(metric_dir)
    #server_target = metric_server_target(metric_dir)
    print '\tFound collectd cpu plugin for: ' + c
    #for submetric in os.listdir(metric_dir):
    #    submetric_type = metric_type(submetric)
    #    print ' - Found ' + plugin + ' metric type: ' + submetric_type
    #    metrics.append({'alias': metric + ' ' + submetric_type, 'target': metric_target(os.path.join(metric_dir, submetric))})
    return []

def df(metric_dir):
    d = os.path.basename(metric_dir)
    print '\tFound collectd df plugin for: ' + d
    if metric == 'df-boot':
        return []
    server_target = metric_server_target(metric_dir)
    return [
        {
            'alias': d,
            'targets': [
                '.'.join([server_target, d, 'df_complex-used']),
                '.'.join([server_target, d, 'df_complex-free'])
            ],
            'scheme': [
                '#ff0000',
                '#00ff00'
            ]
        }
    ]

def disk(metric_dir):
    d = os.path.basename(metric_dir)
    server_target = metric_server_target(metric_dir)
    print '\tFound collectd disk plugin for: ' + d
    return [
        {
            'alias': d + ' octets',
            'targets': [
                '.'.join([server_target, d, 'disk_octets.read']),
                '.'.join([server_target, d, 'disk_octets.write'])
            ],
            'renderer': 'line',
            'scheme': [
                '#00ff00',
                '#ff0000'
            ]
        },
        {
            'alias': d + ' ops',
            'targets': [
                '.'.join([server_target, d, 'disk_ops.read']),
                '.'.join([server_target, d, 'disk_ops.write'])
            ],
            'renderer': 'line',
            'scheme': [
                '#00ff00',
                '#ff0000'
            ]
        },
        {
            'alias': d + ' time',
            'targets': [
                '.'.join([server_target, d, 'disk_time.read']),
                '.'.join([server_target, d, 'disk_time.write'])
            ],
            'renderer': 'line',
            'scheme': [
                '#00ff00',
                '#ff0000'
            ]
        }
    ]

def interface(metric_dir):
    iface = os.path.basename(metric_dir)
    print '\tFound collectd interface plugin for: ' + iface
    server_target = metric_server_target(metric_dir)
    return [
        {
            'alias': iface + ' errors',
            'targets': [
                '.'.join([server_target, iface, 'if_errors.rx']),
                '.'.join([server_target, iface, 'if_errors.tx'])
            ],
            'renderer': 'line',
            'scheme': [
                '#00ff00',
                '#ff0000'
            ]
        },
        {
            'alias': iface + ' octets',
            'targets': [
                '.'.join([server_target, iface, 'if_octets.rx']),
                '.'.join([server_target, iface, 'if_octets.tx'])
            ],
            'renderer': 'line',
            'scheme': [
                '#00ff00',
                '#ff0000'
            ]
        },
        {
            'alias': iface + ' packets',
            'targets': [
                '.'.join([server_target, iface, 'if_packets.rx']),
                '.'.join([server_target, iface, 'if_packets.tx'])
            ],
            'renderer': 'line',
            'scheme': [
                '#00ff00',
                '#ff0000'
            ]
        }
    ]

def memory(metric_dir):
    server_target = metric_server_target(metric_dir)
    print '\tFound collectd memory plugin'
    return [
        {
            'alias': 'Memory Usage',
            'targets': [
                '.'.join([server_target, 'memory', 'memory-used']),
                '.'.join([server_target, 'memory', 'memory-buffered']),
                '.'.join([server_target, 'memory', 'memory-cached']),
                '.'.join([server_target, 'memory', 'memory-free'])
            ],
            'scheme': [
                '#ff0000',
                '#ff00ff',
                '#00ffff',
                '#00ff00'
            ]
        }
    ]

def swap(metric_dir):
    print '\tFound collectd swap plugin'
    server_target = metric_server_target(metric_dir)
    return [
        {
            'alias': 'Swap Usage',
            'targets': [
                '.'.join([server_target, 'swap', 'swap-used']),
                '.'.join([server_target, 'swap', 'swap-free'])
            ],
            'scheme': [
                '#ff0000',
                '#00ff00'
            ]
        },
        {
            'alias': 'Swap IO',
            'targets': [
                '.'.join([server_target, 'swap', 'swap_io-in']),
                '.'.join([server_target, 'swap', 'swap_io-out'])
            ],
            'renderer': 'line',
            'scheme': [
                '#00ff00',
                '#ff0000'
            ]
        }
    ]

dashboards = []
for server in sorted(os.listdir(graphite_collectd_dir)):
    print server
    server_metrics = [
        {
            'alias': 'CPU Usage',
            'targets': [
                'sum(' + configuration['graphite']['prefix'] + '.' + server + '.cpu-*.cpu-user)',
                'sum(' + configuration['graphite']['prefix'] + '.' + server + '.cpu-*.cpu-system)',
                'sum(' + configuration['graphite']['prefix'] + '.' + server + '.cpu-*.cpu-wait)',
                'sum(' + configuration['graphite']['prefix'] + '.' + server + '.cpu-*.cpu-nice)'
            ],
            'scheme': [
                '#00ff00',
                '#ff00ff',
                '#ff0000',
                '#00ffff'
            ]
        }
    ]
    server_dir = os.path.join(graphite_collectd_dir, server)
    for metric in sorted(os.listdir(server_dir)):
        #print metric
        metric_dir = os.path.join(server_dir, metric)
        if metric.startswith('cpu-'):
            server_metrics = server_metrics + cpu(metric_dir)
        elif metric.startswith('df-'):
            server_metrics = server_metrics + df(metric_dir)
        elif metric.startswith('disk-'):
            server_metrics = server_metrics + disk(metric_dir)
        elif metric.startswith('interface-'):
            server_metrics = server_metrics + interface(metric_dir)
        elif metric == 'memory':
            server_metrics = server_metrics + memory(metric_dir)
        elif metric == 'swap':
            server_metrics = server_metrics + swap(metric_dir)
    dashboards.append({
        "name": server,
        "refresh": configuration['giraffe']['refresh'],
        "metrics": server_metrics
    })

with open(giraffe_dashboard_file + '.tmp', 'w') as f:
    f.write('var graphite_url = ' + configuration['graphite']['url'] + ';\n')
    f.write('var dashboards = \n')
    pp = pprint.PrettyPrinter(indent=2, stream=f)
    pp.pprint(dashboards)
    f.write(';\n')
f.closed
shutil.move(giraffe_dashboard_file + '.tmp', giraffe_dashboard_file)
