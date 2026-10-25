# Windows core client status

Core branch: `codex/windows-client-pr`; split prepared 25 October 2026. Primary runtime: original Swordigo 1.4.13 ARM64; native Windows 11 x64; AMD Radeon RX 7700 XT.

## Validation scope

Before the split, the complete working version reached the game menu, created/loaded profiles, exercised movement, jumping, combat, magic, transitions and save/restart/load. The user confirmed corrected first final-boss introduction and Game Over timing. Keyboard/touch dismissal and F2 binding persistence were also exercised internally. Those compatibility and input fixes are retained here.

The complete version previously passed a fresh build, eight focused tests, eight package checks and a standalone APKM import. The 941 imported original files matched the supplied APKM. Optional mod/debug results from that version do not validate the reduced core independently.

The split is checked with the core build, six focused tests and the packaged host/guest diagnostics. Local dated build/package reports are kept outside this source tree. These checks do not replace a complete gameplay test.

## Focused automated checks

Six core tests: `client_preflight`, `client_abi`, `client_jit`, `client_io`, `client_program_state`, `client_input`. They cover synthetic container validation, ABI helpers, JIT exclusive operations, IO-thread/mutex behavior, Lua resume behavior and keyboard configuration persistence. No original game files are needed by these tests.

The two optional adapter/physics tests belong to `codex/windows-extras`. Packaging checks exercise startup diagnostics and host/guest smoke modes in a Unicode folder with a system-only PATH.

## Remaining limitations

- No complete playthrough, device-by-device timing equivalence, repeatable instakill guarantee or speedrun leaderboard approval.
- Most gameplay verification is for 1.4.13. A separate 1.4.12 experiment reached menu/new game and movement; complete support is not established.
- Linux/editor builds, Windows 7/10 and ARM64 Windows hosts are untested for this Windows contribution.
- Existing upstream Save State / Load State are placeholders. The new 1.4.13 mod/debug implementations are deliberately on the extras branch. Existing upstream mod/network behavior is not accepted by these core checks.
- Audio decoding/device playback passed internal checks; a complete listening pass remains open.
