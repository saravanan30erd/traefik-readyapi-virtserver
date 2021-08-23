import subprocess
import json
import config

def get_virtservices(cli, virtserver):
    l = subprocess.check_output(cli, shell=True, universal_newlines=True)
    virts_list = l.split('\n')
    virts_list = list(filter(None, virts_list))
    virts = []
    for i in virts_list:
        ls = []
        v = i.split('|')
        ls.append(v[2].strip())
        ls.append(v[3].strip())
        ls.append(v[4].strip())
        ls.append(virtserver)
        if v[5].strip() == 'true':
            virts.append(ls)
    return virts

def parse_virtservices():
    all_virts = []
    for virtserver in config.VIRTSERVERS:
        virtserver_cli = '{} -ls -s {}:9090 -u {} -pw {} | tail -n+4 | head -n-1'.format(
            config.VIRTSERVER_CLI,
            virtserver,
            config.VIRTSERVER_USER,
            config.VIRTSERVER_PASSWORD
        )
        virts = get_virtservices(virtserver_cli, virtserver)
        all_virts.append(virts)
    return all_virts

def generate_dynamic_config():
    d_conf = {
        'http': {
            'routers': {},
            'services': {}
        }
    }
    virts = parse_virtservices()
    for virt in virts:
        rule = 'Host(`{}`) && PathPrefix(`{}`)'.format(
            config.TRAEFIK_URL,
            virt[1]
        )
        router = {'rule' : rule, 'service' : virt[0]}
        url = 'http://{}:{}'.format(virt[3], virt[2])
        service = {'loadBalancer': {'servers': [{'url': url }]}}
        d_conf['http']['routers'][virt[0]] = router
        d_conf['http']['services'][virt[0]] = service
    print(d_conf)