# Windows client changes

Core/extras split: 25 October 2026. Baseline: upstream `072db6cc335c1c0bad41b965986738eb3840ab6d`.

## Core Windows contribution (`codex/windows-client-pr`)

The client-only build uses MinGW-w64 UCRT64 with a native Windows executable, the existing Dynarmic ARM64 runtime and freestanding ARM64 SRE libraries. The ELF loader, engine and desktop architecture are inherited from upstream.

Compatibility fixes cover the conflicting Windows mutex shim that caused startup hangs, guest/host ABI and file handling, framebuffer texture state, ProgramState resume behavior needed for intro/death sequences, the AAPCS64 scene transition return convention, and Game Over dismissal. The existing F2 keyboard editor now preserves bindings across restarts.

For 1.4.13 the Dynarmic exclusive-instruction path retains the original guest instructions. The older 1.4.12 path retains its legacy STXR compatibility rewriting. Original APK/APKM files, game libraries, level data, scripts and boss values are not edited; source-file integrity alone does not establish Android runtime equivalence.

Build/package scripts include preflight diagnostics, host/guest smoke modes, a standalone local APKM importer and six focused core tests. ARM64 linking uses response files for long Windows source paths. The starter defaults to the primary tested version, 1.4.13.

## Separate optional contribution (`codex/windows-extras`)

The extras branch builds on the core branch and adds the validated 1.4.13 mod adapter, magic/health/sword upgrades capped at 8, inventory item giving, legacy upgrade repair with backups, live F3 XYZ, physics recording/analysis and optional FPS/performance simulation with ±1/±5 controls. Those implementations and their two tests are absent from the core diff. The existing upstream menus and practice features remain inherited code.

## Review scope

The upstream README, project workflows, Android dependencies and default tracked configuration are preserved. Local preferences, generated products and original game data are excluded. The full pre-split version is retained on `codex/windows-complete-backup`. This is a local branch split; nothing was published. Integration with newer upstream commits still needs review before merging.
