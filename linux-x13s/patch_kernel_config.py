#!/usr/bin/env python3

import sys

inputfile = sys.argv[1]
outputfile = sys.argv[2]

# uncomment for testing
# inputfile = "/home/alex/src/git/x13s-alarm/linux-x13s/config"
# outputfile = "config.out"

with open(inputfile, "r") as f:
    lines = f.readlines()

anomalies = {
    "CONFIG_CC_IMPLICIT_FALLTHROUGH": '"-Wimplicit-fallthrough=5"',
}

x13s_options = {
    # Add raw HID support so FIDO works in browsers
    "CONFIG_HIDRAW": "y",
    "CONFIG_USB_HIDDEV": "y",
    "CONFIG_HID_CP2112": "n",
    "CONFIG_HID_FT260": "n",
    # Turn on essential configuration options
    "CONFIG_BLOCK_LEGACY_AUTOLOAD": "y",
    "CONFIG_PHY_QCOM_APQ8064_SATA": "m",
    "CONFIG_PHY_QCOM_IPQ806X_SATA": "m",
    "CONFIG_PHY_QCOM_QMP": "y",
    "CONFIG_PHY_QCOM_QMP_PCIE": "y",
    "CONFIG_PHY_QCOM_QMP_PCIE_8996": "y",
    "CONFIG_PHY_QCOM_QMP_UFS": "y",
    "CONFIG_PHY_QCOM_QMP_USB": "y",
    "CONFIG_PHY_QCOM_QUSB2": "y",
    "CONFIG_PHY_QCOM_USB_SNPS_FEMTO_V2": "y",
    "CONFIG_BRIDGE": "m",
    "CONFIG_BRIDGE_NF_EBTABLES": "n",
    "CONFIG_BRIDGE_NETFILTER": "m",
    "CONFIG_BRIDGE_IGMP_SNOOPING": "y",
    "CONFIG_BRIDGE_MRP": "n",
    "CONFIG_BRIDGE_CFM": "n",
    "CONFIG_NETFILTER_XT_MATCH_PHYSDEV": "n",
    "CONFIG_IP_NF_NAT": "m",
    "CONFIG_NF_NAT": "m",
    "CONFIG_NETFILTER_XT_TARGET_NETMAP": "n",
    "CONFIG_NETFILTER_XT_TARGET_REDIRECT": "n",
    "CONFIG_NETFILTER_XT_TARGET_MASQUERADE": "n",
    "CONFIG_IP_NF_TARGET_MASQUERADE": "m",
    "CONFIG_IP_NF_TARGET_NETMAP": "n",
    "CONFIG_IP_NF_TARGET_REDIRECT": "n",
    # Turn on regularly used filystems
    "CONFIG_EROFS_FS": "y",
    "CONFIG_SQUASHFS": "y",
    "CONFIG_SQUASHFS_XZ": "y",
    "CONFIG_XFS_FS": "m",
    "CONFIG_XFS_SUPPORT_V4": "y",
    "CONFIG_XFS_SUPPORT_ASCII_CI": "y",
    "CONFIG_XFS_QUOTA": "y",
    "CONFIG_XFS_POSIX_ACL": "y",
    "CONFIG_XFS_RT": "n",
    "CONFIG_XFS_ONLINE_SCRUB": "n",
    "CONFIG_XFS_WARN": "n",
    "CONFIG_XFS_DEBUG": "n",
    "CONFIG_BTRFS_FS": "m",
    "CONFIG_BTRFS_FS_POSIX_ACL": "y",
    "CONFIG_BTRFS_FS_RUN_SANITY_TESTS": "y",
    "CONFIG_BTRFS_DEBUG": "y",
    "CONFIG_BTRFS_ASSERT": "n",
    "CONFIG_BTRFS_FS_REF_VERIFY": "n",
    "CONFIG_CEPH_FS": "n",
    "CONFIG_CODA_FS": "n",
    "CONFIG_AFS_FS": "n",
    "CONFIG_FS_ENCRYPTION": "y",
    "CONFIG_FS_ENCRYPTION_ALGS": "y",
    "CONFIG_FS_VERITY": "y",
    "CONFIG_FS_VERITY_BUILTIN_SIGNATURES": "n",
    "CONFIG_FSCACHE": "n",
    "CONFIG_NETFS_SUPPORT": "m",
    "CONFIG_NETFS_STATS": "n",
    "CONFIG_ISO9660_FS": "m",
    "CONFIG_JOLIET": "y",
    "CONFIG_ZISOFS": "y",
    "CONFIG_UDF_FS": "m",
    "CONFIG_FAT_DEFAULT_UTF8": "y",
    "CONFIG_EXFAT_FS": "m",
    "CONFIG_EXFAT_DEFAULT_IOCHARSET": '"utf8"',
    "CONFIG_NETWORK_FILESYSTEMS": "y",
    "CONFIG_NFS_FS": "m",
    "CONFIG_NFS_V2": "y",
    "CONFIG_NFS_V3": "y",
    "CONFIG_NFS_DISABLE_UDP_SUPPORT": "y",
    "CONFIG_NFS_V3_ACL": "n",
    "CONFIG_NFS_V4": "n",
    "CONFIG_NFS_SWAP": "n",
    "CONFIG_NFS_FSCACHE": "n",
    "CONFIG_NFSD": "n",
    "CONFIG_GRACE_PERIOD": "m",
    "CONFIG_LOCKD": "m",
    "CONFIG_LOCKD_V4": "y",
    "CONFIG_NFS_COMMON": "y",
    "CONFIG_SUNRPC": "m",
    "CONFIG_SUNRPC_GSS": "m",
    "CONFIG_SUNRPC_DEBUG": "n",
    "CONFIG_RPCSEC_GSS_KRB5": "m",
    "CONFIG_CIFS": "m",
    "CONFIG_CIFS_STATS2": "y",
    "CONFIG_CIFS_ALLOW_INSECURE_LEGACY": "y",
    "CONFIG_CIFS_DEBUG": "y",
    "CONFIG_CIFS_UPCALL": "n",
    "CONFIG_CIFS_XATTR": "n",
    "CONFIG_CIFS_DEBUG2": "n",
    "CONFIG_CIFS_DEBUG_DUMP_KEYS": "n",
    "CONFIG_CIFS_DFS_UPCALL": "n",
    "CONFIG_CIFS_SWN_UPCALL": "n",
    "CONFIG_SMB_SERVER": "n",
    "CONFIG_SMBFS": "m",
    "CONFIG_NLS_UCS2_UTILS": "m",
    "CONFIG_XOR_BLOCKS": "m",
    "CONFIG_CRYPTO_BLAKE2B": "m",
    "CONFIG_CRYPTO_XXHASH": "m",
    "CONFIG_RAID6_PQ": "m",
    "CONFIG_RAID6_PQ_BENCHMARK": "y",
    "CONFIG_CRC_ITU_T": "m",
    "CONFIG_ZLIB_DEFLATE": "m",
    "CONFIG_ZSTD_COMPRESS": "m",
    # Enable the hardware to use the filesystems
    "CONFIG_CDROM": "m",
    "CONFIG_BLK_DEV_SR": "m",
    "CONFIG_CHR_DEV_SG": "m",
    "CONFIG_USB_EHCI_HCD": "y",
    "CONFIG_USB_EHCI_ROOT_HUB_TT": "n",
    "CONFIG_USB_EHCI_FSL": "n",
    "CONFIG_USB_EHCI_HCD_PLATFORM": "n",
    "CONFIG_USB_SISUSBVGA": "n",
    "CONFIG_USB_EHCI_TT_NEWSCHED": "y",
    "CONFIG_BCM_SBA_RAID": "n",
    "CONFIG_NETFS_DEBUG": "n",
}
leftovers = []
for key in x13s_options:
    leftovers.append(key)

options = {}

new_lines = []
for line in lines:
    if line.startswith("#"):
        if "is not set" in line:
            foo = line.split("is not set")[0].strip()
            key = foo.split("#")[1].strip()
            new_lines.append((key, "not set"))
        else:
            new_lines.append(line)
    elif line == "\n":
        new_lines.append(line)
    else:
        key = line.split("=")[0]
        value = line.split("=")[1]
        new_lines.append((key, value))

output_lines = []
for line in new_lines:
    if isinstance(line, tuple):
        key, value = line
        if key in x13s_options:
            if value != x13s_options[key]:
                output_lines.append(f"{key}={x13s_options[key]}\n")
            else:
                output_lines.append(f"{key}={value}")
            leftovers.remove(key)
        elif key in anomalies:
            output_lines.append(f"{key}={anomalies[key]}\n")
        elif value != "not set":
            output_lines.append(f"{key}={value}")
        else:
            output_lines.append(f"# {key} is not set\n")
    else:
        output_lines.append(line)

for extra_config in leftovers:
    output_lines.append(f"{extra_config}={x13s_options[extra_config]}\n")

with open(outputfile, "w") as f:
    f.writelines(output_lines)

print("Done!")
print(leftovers)
