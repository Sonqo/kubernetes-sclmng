import time
from kubernetes import client, config


def fecth_cpu_usage(group, version, plural, label_selector):
    node_metrics = kube_api.list_cluster_custom_object(group, version, plural, label_selector=label_selector)
    acc = []
    for metric in node_metrics['items']:
        cpu_usage = metric['usage']['cpu']
        if cpu_usage[-1] == 'n':
            cpu_usage = int(cpu_usage.strip('n')) // 1000000
        elif cpu_usage[-1] == 'm':
            cpu_usage = int(cpu_usage.strip('m'))
        else:
            raise ValueError('Unhandled CPU metric.')
        cpu_percentage = int(cpu_usage) // (2 * 10)
        acc.append(cpu_percentage)
    return acc


def fetch_mongodb_resource(group, version, plural):
    return kube_api.list_cluster_custom_object(group, version, plural)['items'][0]


config.load_incluster_config()
kube_api = client.CustomObjectsApi()

while True:

    time.sleep(15)

    cpu_usage_list = fecth_cpu_usage('metrics.k8s.io', 'v1beta1', 'nodes', 'status=worker')
    mongo = fetch_mongodb_resource('mongodb.com', 'v1', 'mongodb')

    nodes_number = len(cpu_usage_list)
    print('Number of worker nodes identified:{}'.format(nodes_number))

    spec = mongo['spec']['mongodsPerShardCount'] * mongo['spec']['shardCount']
    status = mongo['status']['mongodsPerShardCount'] * mongo['status']['shardCount']

    min_mongods = 1
    max_mongods = nodes_number // 2
    curr_mongods = mongo['status']['mongodsPerShardCount']

    if spec == status: # stable state
        overworked_nodes = 0
        underworked_nodes = 0
        for metric in cpu_usage_list:
            if metric > 50:
                overworked_nodes += 1
            elif metric < 30:
                underworked_nodes += 1
        patch_body = None
        if overworked_nodes >= 2 and nodes_number > status:
            print('CHANGE NEEDED')
            if curr_mongods < max_mongods:
                patch_body = {
                    'spec': {
                        'mongodsPerShardCount' : curr_mongods + 1
                    }
                }
                print('INCREASED MONGODS')
            else:
                print('NO WORKER NODES AVAILABLE') 
        elif underworked_nodes == nodes_number and curr_mongods > min_mongods:
            patch_body = {
                'spec': {
                    'mongodsPerShardCount' : curr_mongods - 1
                }
            }
        else:
            print('OK')
        if patch_body:
            patch_resource = kube_api.patch_namespaced_custom_object(
                group='mongodb.com',
                version='v1',
                name='mongodb-sharded',
                namespace='mongodb-mvp',
                plural='mongodb',
                body=patch_body
            )
            print('Sleeping for 5 minutes')
            time.sleep(300)
