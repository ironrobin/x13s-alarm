Packages for the ThinkPad X13s

## Binary repository
To use pre-built packages, add this section to the end of your `/etc/pacman.conf`:

```conf
[ironrobin-x13s]
Server = https://github.com/ironrobin/x13s-alarm/releases/download/packages
```

You'll need to trust the public key in order to verify package signature:

```bash
sudo pacman-key --recv-keys 6ED02751500A833A --keyserver pgp.mit.edu
sudo pacman-key --lsign-key 6ED02751500A833A
```

## Note on `linux-x13s`
For now, you will need `efi=noruntime` as a kernel parameter to boot into the kernel.

In order to get the battery working, install `pd-mapper` `qmic` `qrtr` `rmtfs` and enable `pd-mapper.service`.
