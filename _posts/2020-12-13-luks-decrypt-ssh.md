---
title: "LUKS decrypt over ssh"
---

If you're using LUKS encryption for your system drive, there's no way, by
default, to unlock a remote machine (you need a keyboard and monitor).

We can run a lightweight ssh server, `dropbear`, from the kernel, to allow
decryption (and therefore booting) over the network.

I did this on Ubuntu; there may be easier options for other systems ([this][1]
seems targeted to Fedora).

## Installation
```bash
sudo apt install dropbear busybox
```
Dropbear is the SSH server we run from busybox; however, it can also be used as
a regular user-space ssh server. It will generate its own keys, but I ignored
those. When installing, you might see something about dropbear not being able
to find an `authorized_keys` file. That's fine; we add it later.

## Setup

**Copy keys.** You could generate a separate keypair for logging into the
kernel, but I don't feel like it. Instead, I just copied my already-loaded SSH
keys over:
   
```bash
cp ~/.ssh/authorized_keys /etc/dropbear-initramfs/authorized_keys
```

Then, run `sudo update-initramfs -u` to load the changes. You shouldn't see the
error message about dropbear not finding a keyfile. You could also use the
standard `ssh-copy-id` command (from the device you want to use to unlock), and
then copy them from the local ssh directory to dropbear.

**Note:** you have to run `update-initramfs` any time you want to reload
changes.

## Unlocking

Might take a few seconds to get a network connection & launch dropbear after
boot. Then, `ssh root@machine-hostname-or-ip`. You should a busybox prompt. To
unlock,

```bash
echo -ne "PASSWORD" > /lib/cryptsetup/passfifo
```

You will be kicked out of your SSH session if that worked, and Ubuntu will boot!

To make things easier, I wrote a shell script on my other computer that asks for
your password, and unlocks:

```bash
#!/bin/zsh

echo -n "password? "
read PASSWD

ssh macmini-crypt "echo -ne \"$PASSWD\" > /lib/cryptsetup/passfifo"
```

## Unknowns

- **How to set hostname during boot?** Of course we want this to use a different
  hostname than the real system, since its host authorization keys are
  different. I tried setting `ip=...` in `/etc/initramfs/initramfs.conf`
  but it didn't work (this may be an issue with my router not wanting to swap
  hostnames for what it thinks is the same device, however). For now, I've just
  manually set an IP address for my computer via my router's DHCP server, and
  then, in my `.ssh/config` file, I've added a host by IP. To prevent any
  validation issues, I'm SSHing into the real machine by hostname.
 
- **Can we change the dropbear settings?** I think any options have to be
  specified in `/etc/dropbear-initramfs`, not `/etc/default/dropbear` or
  `/etc/dropbear`, as I initially tried, as these are the config files for the
  user-space copy of dropbear, were I to use that. Specifically, it'd be nice to
  be able to change the port. Then again, probably doesn't matter on local
  network.

*Update, July 2023*: after a power failure, I was unable to log in to dropbear, seeing scary messages about rejected keys. After plugging in a USB keyboard to decrypt, I found [this ServerFault post](https://serverfault.com/questions/1080816/how-do-i-get-logs-from-my-dropbear-initramfs-ssh-host), which details the same issue. [This linked blog post](https://dev.to/bowmanjd/upgrade-ssh-client-keys-and-remote-servers-after-fedora-33-s-new-crypto-policy-47ag) describing the fix: basically, we just needed to force-allow RSA. The best way to solve this would be to update keys to not use RSA, but I'm ok with this solution. The SSH config on my laptop now looks like:

```
# "normal" access
Host macmini
    Hostname macmini-ubuntu.local
    User eli
    LocalForward 3000 localhost:3000

# bootup LUKS/dropbear access
Host macmini-crypt
    Hostname 192.168.1.200
    User root
    # added this line to force RSA
    PubkeyAcceptedKeyTypes +ssh-rsa
```
  
## Helpful Links

[Unlocking a LUKS encrypted root partition remotely via SSH][2]

[How to install and configure Dropbear on Linux][3]

[1]: https://github.com/dracut-crypt-ssh/dracut-crypt-ssh

[2]: http://blog.neutrino.es/2011/unlocking-a-luks-encrypted-root-partition-remotely-via-ssh/

[3]: https://linuxconfig.org/how-to-install-and-configure-dropbear-on-linux
