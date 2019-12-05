#!/usr/bin/env bash

admin_address=
private_subnet=172.31.2.0
prefix=24
tcp_port=60000
udp_port=60001

iptables -t mangle -A PREROUTING -s ${admin_address} -j ACCEPT
iptables -t mangle -A PREROUTING  -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -t mangle -A PREROUTING -d ${private_subnet}/${prefix} -p tcp -j TPROXY --on-port=${tcp_port} --on-ip=127.0.0.1
iptables -t mangle -A PREROUTING -d ${private_subnet}/${prefix} -p udp -j TPROXY --on-port=${udp_port} --on-ip=127.0.0.1