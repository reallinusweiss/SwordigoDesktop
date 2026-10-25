# Source and dependency notices

The `codex/windows-client-pr` branch contains core Windows compatibility changes on top of SwordigoDesktop, including the host, ARM64 SRE sources, focused tests, vendored source dependencies and Windows build/package scripts. Original upstream history and component notices are retained.

Baseline: https://github.com/TheAevoraLabs/SwordigoDesktop/commit/072db6cc335c1c0bad41b965986738eb3840ab6d

Build instructions: WINDOWS_CLIENT.md and tools/windows/build.ps1. Exact Windows toolchain/package versions and SHA-256 hashes are in tools/windows/packages.lock.json. Game APK/APKM packages, original game libraries and extracted game data are not supplied by this contribution.

Any distributed binary must identify its actual corresponding source commit or source archive. The frozen local release archives dated 2026-10-23 are separate historical snapshots; their source archive does not describe every later documentation or packaging edit in this working branch.

Bundled runtime dependencies retain their own license terms. Their packaged notices are under licenses/dependencies and licenses/vendored. MSYS2 recipes/source starting point: https://github.com/msys2/MINGW-packages . The package lock includes build tools as well as runtime libraries and is not a complete corresponding-source bundle for every DLL. Complete the matching source/access and any required build/relinking information for affected GPL/LGPL dependencies before distributing a public binary release.

This branch is prepared for review, not an announced official release. No game data is included and no public repository URL or release tag has been invented for the contributor.
