# Traefik HTTP provider for ReadyAPI VirtServer

## Problem statement

  [ReadyAPI Virtualization](https://support.smartbear.com/readyapi/docs/virtualization/intro/about.html) is used for creating API Mock services.
  It have server side component called [VirtServer](https://support.smartbear.com/virtserver/docs/intro.html) which is used to deploy and run API Mock services.

  In VirtServer, every Mock service runs with own port. If we have 100 API microservices then we may need to create 100 Mock services and all these 100 mock services runs on own TCP port (3000, 3001,..3100).

  Example, If we have 100 Mock services and 3 VirtServers, assume every VirtServer running 35 Mock services.

  Without Traefik,
  ```
    http://virt-server1:3001/api/mock1
    http://virt-server2:3002/api/mock2
    ......
    http://virt-server3:3100/api/mock100
  ```

Its very difficult to maintain many Mock services across many VirtServers. If we want to utilize a mock service mock1 in our frontend applications then we need to check all the VirtServers to find where the mock1 mock service running and its port number.

Also If we want to use a load balancer in front of these 3 VirtServer nodes, then we need to update the load balancer configuration file manually whenever new mock service is deployed in any VirtServers and its tedious process.

## Solution

To manage this scenario effectively, I am going to use [Traefik](https://traefik.io/) and its [Dynamic Configuration](https://doc.traefik.io/traefik/providers/overview/) feature using [HTTP provider](https://doc.traefik.io/traefik/providers/http/).

What sets Traefik apart, besides its many features, is that it automatically discovers the right configuration for your services. You can provide the dynamic configuration via an HTTP(S) endpoint.

![Traffic Flow](traefik-virtserver.png)


I have created [this](https://github.com/saravanan30erd/traefik-readyapi-virtserver) HTTP provider to automatically generate the dynamic configuration for Traefik. We don't need to update the Traefik configuration each time the new mock service is deployed into VirtServers, this provider will detect newly deployed mock service configurations(Name, Path and Port number) and then generate the dynamic configuration for Traefik.

## Prerequisite

* [Traefik Installation](https://doc.traefik.io/traefik/getting-started/install-traefik/)
* [ReadyAPI VirtServer CLI Installation](https://support.smartbear.com/virtserver/docs/user-tasks/cli.html)
* Python3

## Configuration

Configure the traefik configuration file to use Dynamic Configuration from HTTP provider,

```
providers:
  http:
    endpoint:
      - "http://127.0.0.1:3000/api/config?output=json"
```

Install the dependency packages,

```
pip3 install -r requirements.txt
```

Configure the configuration file app/config.py,

```
Provide the list of VirtServer IPs in the cluster,

VIRTSERVERS = [
    '10.0.0.1',
    '10.0.0.2',
    '10.0.0.3'
]
```
```
Provide the correct VirtServer CLI Path,

VIRTSERVER_CLI = '/usr/local/bin/virtserver-cli.sh'
```
```
Provide the FQDN,

TRAEFIK_URL = 'mock.example.com'
```
```
Set VirtServer access credentials via Environment Variables,

export USER=test
export PASSWORD=test
```

Run the HTTP provider,

```
python3 app/main.py
```

## Conclusion

Without Traefik,

```
http://virt-server1:3001/api/mock1  http://virt-server2:3003/api/mock3  http://virt-server3:3005/api/mock5
http://virt-server1:3002/api/mock2  http://virt-server2:3004/api/mock4  http://virt-server3:3006/api/mock6
......
http://virt-server1:3098/api/mock98  http://virt-server2:3099/api/mock99  http://virt-server3:3100/api/mock100

```

With Traefik and HTTP Provider(Dynamic Configuration),

```
http://mock.example.com/api/mock1  http://mock.example.com/api/mock3  http://mock.example.com/api/mock5
http://mock.example.com/api/mock2  http://mock.example.com/api/mock4  http://mock.example.com/api/mock6
......
http://mock.example.com/api/mock98  http://mock.example.com/api/mock99  http://mock.example.com/api/mock100
```
