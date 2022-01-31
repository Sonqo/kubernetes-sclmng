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
    # print('Number of nodes:{}'.format(nodes_number))

    spec = mongo['spec']['mongodsPerShardCount'] * mongo['spec']['shardCount']
    status = mongo['status']['mongodsPerShardCount'] * mongo['status']['shardCount']
    # print('Spec:{} | Status:{}'.format(spec, status))

    curr_shards = mongo['status']['shardCount']
    curr_mongods = mongo['status']['mongodsPerShardCount']

    max_shards = nodes_number // 3
    max_mongods = nodes_number // max_shards

    alternator = 0 # 0 for mongods | 1 for shards
    if spec == status: # stable state
        overworked_nodes = 0
        for metric in cpu_usage_list:
            if metric > 40:
                overworked_nodes += 1
        if overworked_nodes == status and nodes_number > status:
            print('CHANGE NEEDED')
            if alternator == 0 and max_mongods > curr_mongods:
                alternator = 1
                patch_body = {
                    'spec': {
                        'mongodsPerShardCount' : curr_mongods + 1
                    }
                }
                print('INCREASED MONGODS')
            elif alternator == 1 and max_shards > curr_shards:
                alternator = 0
                patch_body = {
                    'spec': {
                        'shardCount' : curr_shards + 1
                    }
                }
                print('INCREASED SHARDS')
            else:
                print('NO WORKER NODES AVAILABLE')
            patch_resource = kube_api.patch_namespaced_custom_object(
                group='mongodb.com',
                version='v1',
                name='mongodb-sharded',
                namespace='mongodb-poc',
                plural='mongodb',
                body=patch_body
            )
        else:
            print('OK')
