## Darkunion

**Description**: I dug up an open-source kernel module that is part of a certain
unknown application whitelist software, with a few rashly documented
vulnerabilities. No one got a chance to exploit the vulns before the project got
altogether dropped. Maybe you could take a shot at it?

**Category**: pwn

**Suggested Points**: 400-500

**Author's note**: This is a two-stage kernel challenge that revolves around an
(obviously) broken application whitelister/applocker like program. To make the
bugs more obvious, and to make this challenge more revolve around the
exploitation phase rather than the more (boring) reading and finding the bug
phase, a `KNOWN_BUGS` file is created, which hints at where the bug is located
(without really giving away how to exploit the bug).

All the files (with the obvious exception of the `flag.server.img` file) is
expected to be given to the player (i.e. including full source), since the
entire kernel module is considered substantial. While the player cannot actually
build the kernel module (as they do not have the kernel headers, nor the actual
kernel version that is built against), they can use the source code to expedite
the tedious reverse engineering step.

When deploying this challenge, you must first rename the flag.server.img file to
be named flag.img. It is suggested to run a docker container with qemu with a
xinetd/socat server setup calling qemu, copying the bzImage, flag.server.img,
ramdisk.img, and run.sh files only. There should be some sort of rate limiting/
PoW mechanism to limit the number of running instances at any time, (though
within qemu we already limit each qemu connection to up to 60 seconds, with 10
seconds of CPU runtime).
