import time, subprocess
from kubernetes import client, config, utils

config.load_incluster_config()
    
api_metrics = client.CustomObjectsApi()
api_stateful = client.AppsV1Api(client.ApiClient())

while True:
    time.sleep(15)
    k8s_nodes = api_metrics.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
    replicas = api_stateful.read_namespaced_stateful_set_status('mongodb-rs', 'app').status.replicas
    for stats in k8s_nodes['items']:
        if stats['metadata']['name'] != 'cluster80':
            cpu_usage = stats['usage']['cpu']
            if cpu_usage[-1] == 'n':
                cpu_usage = int(cpu_usage.strip('n')) // 1000000
            elif cpu_usage[-1] == 'm':
                cpu_usage = int(cpu_usage.strip('m'))
            else:
                raise ValueError('Unhandled CPU metric.')
            cpu_percentage = int(cpu_usage) // (2 * 10)
            print(stats['metadata']['name'], cpu_percentage)
            print(int(replicas))
            # res = subprocess.run('kubectl apply -f mongo-replica_v2.yaml', shell=True, executable='/bin/bash')
            # print(res, type(res))
