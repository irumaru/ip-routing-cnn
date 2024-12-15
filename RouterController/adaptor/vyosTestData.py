c = """
interfaces {
    ethernet eth0 {
        address "192.168.10.11/24"
        hw-id "bc:24:11:36:9f:e6"
        offload {
            gro
            gso
            sg
            tso
        }
    }
    ethernet eth1 {
        address "192.168.9.1/24"
        address "192.168.11.1/24"
        hw-id "bc:24:11:fc:61:00"
    }
    ethernet eth2 {
        hw-id "bc:24:11:71:04:1e"
    }
    ethernet eth3 {
        hw-id "bc:24:11:de:09:54"
    }
    loopback lo {
    }
}
protocols {
    static {
        route 0.0.0.0/0 {
            next-hop 192.168.10.1 {
            }
        }
    }
}
service {
    ntp {
        allow-client {
            address "127.0.0.0/8"
            address "169.254.0.0/16"
            address "10.0.0.0/8"
            address "172.16.0.0/12"
            address "192.168.0.0/16"
            address "::1/128"
            address "fe80::/10"
            address "fc00::/7"
        }
        server time1.vyos.net {
        }
        server time2.vyos.net {
        }
        server time3.vyos.net {
        }
    }
    ssh {
        port "22"
    }
}
system {
    config-management {
        commit-revisions "100"
    }
    console {
        device ttyS0 {
            speed "115200"
        }
    }
    host-name "vyos"
    login {
        user vyos {
            authentication {
                encrypted-password "$6$rounds=656000$GILz3ALYpxjfAsz7$BSFWyJu1y80eNTIx/xEejuV5dnCvmGa.n8N2UdnCS5HivFg/yDA6OKSTYX7Zs9H9xqPe5z5LHGYRUAkJqQ4cw1"
                plaintext-password ""
            }
        }
    }
    syslog {
        global {
            facility all {
                level "info"
            }
            facility local7 {
                level "debug"
            }
        }
    }
}


// Warning: Do not remove the following line.
// vyos-config-version: "bgp@5:broadcast-relay@1:cluster@2:config-management@1:conntrack@5:conntrack-sync@2:container@2:dhcp-relay@2:dhcp-server@11:dhcpv6-server@6:dns-dynamic@4:dns-forwarding@4:firewall@17:flow-accounting@1:https@7:ids@1:interfaces@33:ipoe-server@4:ipsec@13:isis@3:l2tp@9:lldp@2:mdns@1:monitoring@1:nat@8:nat66@3:ntp@3:openconnect@3:openvpn@4:ospf@2:pim@1:policy@8:pppoe-server@11:pptp@5:qos@3:quagga@11:reverse-proxy@2:rip@1:rpki@2:salt@1:snmp@3:ssh@2:sstp@6:system@28:vrf@3:vrrp@4:vyos-accel-ppp@2:wanloadbalance@3:webproxy@2"
// Release version: 1.5-rolling-202412060007
"""

p = """protocols {
    static {
        route 0.0.0.0/0 {
            next-hop 192.168.11.1 {
            }
        }
    }
}"""

r = {
  # "dst": "gateway"
  "0.0.0.0/0": "192.168.10.1",
  "135.1.0.15/32": "192.168.10.2"
}
