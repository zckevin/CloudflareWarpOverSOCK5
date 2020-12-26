## Cloudflare Warp setup
https://github.com/ViRb3/wgcf

generate wg conf for wg-quick

```
[Interface]
PrivateKey = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Address = 172.16.0.2/32
Address = fd01:5ca1:ab1e:8109:323e:6bd1:ea68:b6b4/128
MTU = 1280

[Peer]
PublicKey = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# add ipv4 ranges for local socks5 proxy's remote server
AllowedIPs = 5.7.9.0/24
AllowedIPs = ::/0
Endpoint = 162.159.192.1:2408
```

## boringtun install
https://github.com/cloudflare/boringtun

> cargo install boringtun
installed to ~/.cargo/bin

## boringtun usage
> WG_QUICK_USERSPACE_IMPLEMENTATION=boringtun wg-quick up ./wg0.conf

wg-quick is a bash script wrapper for manipulating/sends `wg` commands to kernel or userspace WireGuard.

Fix wg-quick for running as root user, is case of wg/wg-quick hangs
https://github.com/cloudflare/boringtun/issues/90#issuecomment-508327254

```
add_if() {
        cmd "${WG_QUICK_USERSPACE_IMPLEMENTATION:-wireguard-go}" --disable-drop-privileges true "$INTERFACE"
}
```

## run as non-root user / privileges dropping
> useradd -M -s /bin/false dummy_user

Create a dummy user without home dir & login shell

> sudo -u dummy_user whoami --version

Run all following programs with `sudo -u dummy_user` prefix

## local socks5 proxy with UDP forwarding enabled
https://github.com/shadowsocks/shadowsocks-libev

Cross compile for ARM64

## tun2socks
https://github.com/eycorsican/go-tun2socks

```
# For non-root user run without root permissions
ip tuntap add dev tun0 mode tun user dummy_user
ip link set tun0 up
ip addr add 241.0.0.1 dev tun0

# For CloudFlare warp/warp+ gateway
ip route add 162.159.192.0/24 dev tun0

# localhost:8080 is local socks5 proxy address
tun2socks-linux-arm64 -loglevel debug -proxyType socks -proxyServer localhost:8080 -tunName tun0 -tunAddr  241.0.0.2 -tunGw 241.0.0.1 -loglevel debug
```

## network redirection

