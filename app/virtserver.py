import subprocess
import json
import config
import yaml

class VirtServer(object):
    def __init__(self):
        self.t_url = config.TRAEFIK_URL
        self.v_cli = config.VIRTSERVER_CLI
        self.user = config.VIRTSERVER_USER
        self.password = config.VIRTSERVER_PASSWORD
        self.servers = config.VIRTSERVERS

    def get_virtservices(self, cli, virtserver):
        l = subprocess.check_output(cli, shell=True, universal_newlines=True)
        virts_list = l.split('\n')
        virts_list = list(filter(None, virts_list))
        for i in virts_list:
            ls = []
            v = i.split('|')
            ls.append(v[2].strip())
            ls.append(v[3].strip())
            ls.append(v[4].strip())
            ls.append(virtserver)
            if v[5].strip() == 'true':
                self.virts.append(ls)

    def parse_virtservices(self):
        self.virts = []
        for virtserver in self.servers:
            virtserver_cli = '{} -ls -s {}:9090 -u {} -pw {} | tail -n+4 | head -n-1'.format(
                self.v_cli,
                virtserver,
                self.user,
                self.password
            )
            self.get_virtservices(virtserver_cli, virtserver)
        return self.virts

    def generate_dynamic_config(self):
        d_conf = {
            'http': {
                'routers': {},
                'services': {}
            }
        }
        virts = self.parse_virtservices()
        for virt in virts:
            rule = 'Host(`{}`) && PathPrefix(`{}`)'.format(
                self.t_url,
                virt[1]
            )
            router = {'rule' : rule, 'service' : virt[0]}
            url = 'http://{}:{}'.format(virt[3], virt[2])
            service = {'loadBalancer': {'servers': [{'url': url }]}}
            d_conf['http']['routers'][virt[0]] = router
            d_conf['http']['services'][virt[0]] = service
        return d_conf

def generate_json():
    v = VirtServer()
    conf = v.generate_dynamic_config()
    #with open('mock-service.json', 'w') as fp:
    #    json.dump(conf, fp)
    return json.dump(conf)

def generate_yaml():
    v = VirtServer()
    conf = v.generate_dynamic_config()
    with open('mock-service.yaml', 'w') as fp:
        yaml.dump(conf, fp)

if __name__ == '__main__':
    output = 'yaml'
    if output == 'json':
        generate_json()
    elif output == 'yaml':
        generate_yaml()
