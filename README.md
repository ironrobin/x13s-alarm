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

if it still says "unknown trust" even after you lsign it, try this and then resign:
```bash
sudo rm -rf /etc/pacman.d/gnupg
sudo pacman-key --init
sudo pacman-key --populate archlinux
sudo pacman-key --populate archlinuxarm
```

## Note on `linux-x13s`
For now, you will need `efi=noruntime clk_ignore_unused pd_ignore_unused iommu.passthrough=0 iommu.strict=0 arm64.nopauth` as kernel parameters to boot into the kernel.

In order to get the battery working, install `pd-mapper` `qmic` `qrtr` `rmtfs` and enable `pd-mapper.service`.
