---
title: "why is ssh exposed on my router? (part 1)"
---

I recently ran an `nmap` scan on my router, a [TP-Link Archer AX50][1]. From the LAN port, nothing looked amiss, but scanning my *external* IP address gave some interesting results:

```
$ nmap -Pn X.X.X.X
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-05-21 18:46 EDT
Nmap scan report for X.X.X.X
Host is up (0.0099s latency).
Not shown: 952 filtered ports, 46 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
53/tcp open  domain

Nmap done: 1 IP address (1 host up) scanned in 2048.37 seconds
```

(ssh actually also showed up on the LAN IP but I didn't think much of it.)

At first I thought this was some computer on my local network, but no, I'm not forwarding port 22. It looks like the *router itself* does actually expose SSH to the internet... concerning. I tried a few usernames (`root`, `user`, `admin`, etc.) with my WiFi admin password without any luck.

## Looking through the firmware

Luckily, TP-link makes [the firmware][2] available for download! As of this writing, my router is running version 200708. My idea was to either figure out how to SSH into the router, or see if I could identify any vulnerabilities.

Inside the firmware zip is a binary (as well as the license document, which helpfully reminds the user that [GPL source is available...][3] I'll look into this later):

```bash
$ mv ax50v1_intel-up-ver1-0-9-P1\[20200708-rel55037\]_signed.bin firmware1.0.9.bin
$ ls
GPLeLicenseeTerms.pdf
How to upgrade TP-LINK Wireless AC Router(New VI).pdf
firmware1.0.9.bin
$ file firmware1.0.9.bin 
firmware1.0.9.bin: data
$ binwalk firmware1.0.9.bin 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
4519          0x11A7          uImage header, header size: 64 bytes, header CRC: 0xB7455DE6, created: 2020-07-08 07:18:29, image size: 29654552 bytes, Data Address: 0x0, Entry Point: 0x0, data CRC: 0x506ACDE2, OS: Linux, CPU: MIPS, image type: Multi-File Image, compression type: none, image name: "TP-Link Totalimage"
4591          0x11EF          uImage header, header size: 64 bytes, header CRC: 0xF85FFD41, created: 2020-07-08 07:18:28, image size: 150864 bytes, Data Address: 0x0, Entry Point: 0x0, data CRC: 0x888C4C94, OS: Linux, CPU: MIPS, compression type: lzma, image name: "U-Boot Img"
39107         0x98C3          CRC32 polynomial table, little endian
51855         0xCA8F          CRC32 polynomial table, little endian
55855         0xDA2F          uImage header, header size: 64 bytes, header CRC: 0x908FBBD4, created: 2020-07-08 05:01:29, image size: 99600 bytes, Data Address: 0xA0400000, Entry Point: 0xA0400000, data CRC: 0x38F8E3FA, OS: Linux, CPU: MIPS, image type: Firmware Image, compression type: lzma, image name: "u-boot image"
55919         0xDA6F          LZMA compressed data, properties: 0x5D, dictionary size: 8388608 bytes, uncompressed size: 343580 bytes
155519        0x25F7F         uImage header, header size: 64 bytes, header CRC: 0xCD4DD048, created: 2020-07-08 07:18:29, image size: 131072 bytes, Data Address: 0x0, Entry Point: 0x0, data CRC: 0x6C65B573, OS: Linux, CPU: MIPS, image type: Firmware Image, compression type: lzma, image name: "gphyfw"
155583        0x25FBF         uImage header, header size: 64 bytes, header CRC: 0xE76A1040, created: 2020-07-08 05:01:39, image size: 29176 bytes, Data Address: 0x0, Entry Point: 0x0, data CRC: 0x6D88B827, OS: Linux, CPU: MIPS, image type: Multi-File Image, compression type: lzma, image name: "GPHY Firmware"
155655        0x26007         LZMA compressed data, properties: 0x5D, dictionary size: 8388608 bytes, uncompressed size: 65664 bytes
286655        0x45FBF         uImage header, header size: 64 bytes, header CRC: 0x846655C1, created: 2020-07-08 07:17:38, image size: 26226688 bytes, Data Address: 0x0, Entry Point: 0x0, data CRC: 0x78134F7C, OS: Linux, CPU: MIPS, image type: Filesystem Image, compression type: lzma, image name: "LTQCPE RootFS"
286719        0x45FFF         Squashfs filesystem, little endian, version 4.0, compression:xz, size: 26223172 bytes, 5462 inodes, blocksize: 131072 bytes, created: 2020-07-08 07:17:37
26513407      0x1948FFF       uImage header, header size: 64 bytes, header CRC: 0xC71E56C7, created: 2020-07-08 05:17:29, image size: 3145664 bytes, Data Address: 0xA0020000, Entry Point: 0xA002DF00, data CRC: 0xD79B6C75, OS: Linux, CPU: MIPS, image type: OS Kernel Image, compression type: lzma, image name: "MIPS LTQCPE Linux-3.10.104"
26513471      0x194903F       LZMA compressed data, properties: 0x5D, dictionary size: 8388608 bytes, uncompressed size: 9232128 bytes
```

That's promising! Time to extract:

```bash
$ binwalk -e firmware1.0.9.bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
(same as above...)

WARNING: Extractor.execute failed to run external extractor 'unsquashfs -d 'squashfs-root' '%e'': [Errno 2] No such file or directory: 'unsquashfs', 'unsquashfs -d 'squashfs-root' '%e'' might not be installed correctly

WARNING: Extractor.execute failed to run external extractor 'sasquatch -p 1 -le -d 'squashfs-root' '%e'': [Errno 2] No such file or directory: 'sasquatch', 'sasquatch -p 1 -le -d 'squashfs-root' '%e'' might not be installed correctly

WARNING: Extractor.execute failed to run external extractor 'sasquatch -p 1 -be -d 'squashfs-root' '%e'': [Errno 2] No such file or directory: 'sasquatch', 'sasquatch -p 1 -be -d 'squashfs-root' '%e'' might not be installed correctly
286719        0x45FFF         Squashfs filesystem, little endian, version 4.0, compression:xz, size: 26223172 bytes, 5462 inodes, blocksize: 131072 bytes, created: 2020-07-08 07:17:37
26513407      0x1948FFF       uImage header, header size: 64 bytes, header CRC: 0xC71E56C7, created: 2020-07-08 05:17:29, image size: 3145664 bytes, Data Address: 0xA0020000, Entry Point: 0xA002DF00, data CRC: 0xD79B6C75, OS: Linux, CPU: MIPS, image type: OS Kernel Image, compression type: lzma, image name: "MIPS LTQCPE Linux-3.10.104"
26513471      0x194903F       LZMA compressed data, properties: 0x5D, dictionary size: 8388608 bytes, uncompressed size: 9232128 bytes
```

oops! macOS doesn't like it. Trying on linux.
```bash
$ ls
194903F  26007  45FFF.squashfs  DA6F  squashfs-root
$ file *
194903F:        data
26007:          u-boot legacy uImage, GRX500 V1.1 GPHY BE, Linux/MIPS, Firmware Image (Not compressed), 65536 bytes, Wed Jul  8 05:01:39 2020, Load Address: 0x00000000, Entry Point: 0x00000000, Header CRC: 0x3777347D, Data CRC: 0x8E18E096
45FFF.squashfs: Squashfs filesystem, little endian, version 1024.0, compressed, 4909644877756628992 bytes, 1444216832 inodes, blocksize: 512 bytes, created: Thu Apr 12 07:38:07 1979
DA6F:           data
squashfs-root:  directory
$ ls squashfs-root
bin  data  dev  etc  lib  mnt  opt  overlay  proc  rom  root  sbin  sys  tmp  usr  var  www
```

Exciting. Clearly the Linux image was inside the squashfs, and `26007` is just the bootloader. What's `194903F`?

```bash
$ binwalk -e 194903F 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
1040          0x410           device tree image (dtb)
7389484       0x70C12C        Linux kernel version 3.10.1
7464308       0x71E574        gzip compressed data, maximum compression, from Unix, last modified: 1970-01-01 00:00:00 (null date)
7804252       0x77155C        xz compressed data
7853860       0x77D724        Unix path: /lib/firmware/updates/3.10.104
7930028       0x7900AC        Unix path: /dev/switch_api/0
7935256       0x791518        Unix path: /dev/switch_api/1
7961493       0x797B95        eCos RTOS string reference: "ecostat"
7961522       0x797BB2        eCos RTOS string reference: "ecostat -c pic0=0,pic1=1:EXL,K,S,U,IE 1"
8030833       0x7A8A71        PARity archive data - file number 20548
8215729       0x7D5CB1        Copyright string: "Copyright (c) 2006-2007 BalaBit IT Ltd."
8238988       0x7DB78C        Neighborly text, "NeighborSolicitsp6InMsgs"
8239008       0x7DB7A0        Neighborly text, "NeighborAdvertisementsrs"
8242790       0x7DC666        Neighborly text, "neighbor %.2x%.2x.%pM lost rename link %s to %s"
8298302       0x7E9F3E        Unix path: /var/run/rpcbind.sock
8639872       0x83D580        CRC32 polynomial table, little endian
9220320       0x8CB0E0        ASCII cpio archive (SVR4 with no CRC), file name: "dev", file name length: "0x00000004", file size: "0x00000000"
9220436       0x8CB154        ASCII cpio archive (SVR4 with no CRC), file name: "dev/console", file name length: "0x0000000C", file size: "0x00000000"
9220560       0x8CB1D0        ASCII cpio archive (SVR4 with no CRC), file name: "root", file name length: "0x00000005", file size: "0x00000000"
9220676       0x8CB244        ASCII cpio archive (SVR4 with no CRC), file name: "TRAILER!!!", file name length: "0x0000000B", file size: "0x00000000"
```

Is this the Linux kernel, maybe? The extraction resulted in:

```bash
$ ls -R
.:
71E574  77155C.xz  8CB0E0.cpio  console  cpio-root  dev  root

./cpio-root:
dev  root

./cpio-root/dev:

./cpio-root/root:

./dev:

./root:
```

...but the `cpio` archive only contains empty files, and the `xz` archive is apparently corrupted. weird???

Going back up to the main level, there's not much else to see. `DA6F` is just a CRC polynomial table.

```bash
$ binwalk DA6F 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
211536        0x33A50         CRC32 polynomial table, little endian
213632        0x34280         CRC32 polynomial table, little endian
```

So that pretty much leaves me with the squashfs image. What can I find? `etc` is probably a good place to start, at least to find human-readable stuff.

```bash
$ ls etc/
avahi             dropbear               init.d            passwd             samba_performance_turning
banner            easy-rsa               inittab           powermanager.conf  sbin
certificate       filesystems            iproute2          ppa.conf           services
cloud_config.cfg  firewall.user          ltqpreinit        ppp                shadow
cloud_https.cfg   flag_2g                mcast.conf        pptpd.conf         shells
config            flag_5g                modules.d         preinit            ssl
config.sh         fstab                  mtab              preinit.d          sysctl.conf
conntrackd        functions.sh           netatalk          profile            sysupgrade.conf
crontabs          group                  nixio             proftpd            tsched.conf.d
device_table.txt  hosts                  openvpn           protocols          tsched.d
dhcp6cctlkey      hotplug                openwrt_release   rc.common          TZ
dhcp6s.conf       hotplug2-common.rules  openwrt_version   rc.d               uci-defaults
dhcp6sctlkey      hotplug2-init.rules    opkg.conf         rc.local           udev
diag.sh           hotplug2.rules         oui               resolv.conf        wave_components.ver
dnsmasq.conf      hotplug.d              partition_config  samba              webpage_time
```

welp, looks like TP-link is just running a repackaged version of OpenWRT. Guess I shouldn't be surprised. Oh, and dropbear - there's my ssh server!

```bash
$ cat openwrt_release 
DISTRIB_ID="OpenWrt"
DISTRIB_RELEASE="Attitude Adjustment"
DISTRIB_REVISION="unknown"
DISTRIB_CODENAME="attitude_adjustment"
DISTRIB_TARGET="model_intel_grx350/generic"
DISTRIB_DESCRIPTION="OpenWrt Attitude Adjustment 12.09-rc1"
```

I'm not super familiar with OpenWRT, but after a bit of digging, I realized that this version is from... 2013. That's insane! I'm not seeing that target platform on [OpenWRT's website][4], but I bet I can find it somewhere if I go down that route.

As for my original question,
```bash
$ cat shadow 
root:x:0:0:99999:7:::
daemon:*:0:0:99999:7:::
ftp:*:0:0:99999:7:::
network:*:0:0:99999:7:::
nobody:*:0:0:99999:7:::
admin:x:0:0:99999:7:::
guest::0:0:99999:7:::
$ cat passwd 
root:x:0:0:root:/root:/bin/ash
daemon:*:1:1:daemon:/var:/bin/false
ftp:*:55:55:ftp:/home/ftp:/bin/false
network:*:101:101:network:/var:/bin/false
nobody:*:65534:65534:nobody:/var:/bin/false
admin:x:1000:0:admin:/var:/bin/false
guest::2000:65534:guest:/var:/bin/false
```

Only `root` is given a shell, but no accounts have a valid password. So there will be no logging in directly to the router.

I dug around the file system for a while longer, and discovered:

- `opt/lantiq` seems to contain the original Intel firmware, including Intel's original web GUI
- dropbear actually appears to be disabled (in `/etc/dropbear/config`), and its host keys are empty.
- However, dropbear 2011.54-2 is installed. That's a *decade* old. There's no way it's survived that long and is still perfectly secure.

## Possible Vulnerabilities

I headed over to the CVE database to see if anything popped up for old versions of dropbear. Indeed, there are a few; notably:

- [CVE-2012-0920][5]: Use-after-free vulnerability in Dropbear SSH Server 0.52 through 2012.54, when command restriction and public key authentication are enabled, allows remote authenticated users to execute arbitrary code and bypass command restrictions via multiple crafted command requests, related to "channels concurrency."
    + Interesting, but not applicable to me - authenticated users only.
    + I went back through TP-Link's GPL-released source, and they actually have a patch for this CVE. (`Iplatform/packages/opensource/dropbear/patches`) Good on them!
- [CVE-2016-7406][6]: Format string vulnerability in Dropbear SSH before 2016.74 allows remote attackers to execute arbitrary code via format string specifiers in the (1) username or (2) host argument.
    + This looks interesting! I'm not seeing any mention of it in TP-Link's code.
    + A bit more info [here][7].

The link to the revision fixing 7406 above no longer works, but [this one works as of May 2021][8]. It looks like the issue (line diff 2.43) boils down to calling `printf` with a variable format string! The `svr_dropbear_exit` function takes a format string and variable arguments that it will append to its own log message; however, that log message also includes the (attacker supplied) username we're trying to authenticate. If the username is allowed to contain `%`, then we're vulnerable to all sorts of `printf` nastiness, such as parameter overflows and `%n` memory-writes.

Questions at this point, however:
- Is this code path reachable remotely?
- Is it reachable on the build used in my router?
    + In particular, no users have passwords, so this whole thing may be moot.
    + Also, if my router isn't logging dropbear messages, the format string may never actually be interpreted!
    + ...and if dropbear is disabled, it may keep the port open, but just immediately reject all attempts.
- Does my router even allow `%` in usernames?
- At least in the code snippet linked above, I think the only values a remote attacker controls are the number of failures, and the username.

## Other Ideas
- Run OpenWRT/dropbear in a VM and try to exercise CVE-2016-7406.
- Try to find OpenWRT 12.09 for this chipset, and compare the firmwares: find what TP-link added. I'm more likely to find something in outdated TP-link software than a heavily vetted 8-year-old version of OpenWRT.
    + There are a bunch of "patches" folders -- I'm wondering if that's TP-Link's doing, or OpenWRT.
- Look for possible web attacks from the TP-link GUI
- CVEs in other components (OpenWRT, TP-Link generally)

This was just an initial investigation, so I may return later and look into some of these questions more in depth.


[1]: https://www.tp-link.com/us/home-networking/wifi-router/archer-ax50/
[2]: https://www.tp-link.com/us/support/download/archer-ax50/#Firmware
[3]: https://www.tp-link.com/us/support/gpl-code/
[4]: https://archive.openwrt.org/attitude_adjustment/12.09/
[5]: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-0920
[6]: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-7406
[7]: https://seclists.org/oss-sec/2016/q3/504
[8]: https://hg.ucc.asn.au/dropbear/rev/b66a483f3dcb