"""Exercise the staged client with a clean PATH and from a Unicode directory.
This checks host startup and missing-data diagnostics, never claims gameplay.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]

def main():
    source = Path((ROOT/'.tools/latest-package.txt').read_text(encoding='utf-8'))
    test = Path(tempfile.mkdtemp(prefix='Paketprüfung ä ', dir=ROOT/'.tools'))
    package = test/'Spiel Ordner ü'
    shutil.copytree(source,package)
    elsewhere = test/'Anderer Arbeitsordner'
    elsewhere.mkdir()
    env = os.environ.copy()
    env['PATH'] = str(Path(env['SYSTEMROOT'])/'System32') + ';' + env['SYSTEMROOT']
    env['LOCALAPPDATA'] = str(test/'user-local')
    for name in ['SWORDIGO_DATA_DIR','QT_PLUGIN_PATH','QT_QPA_PLATFORM_PLUGIN_PATH','QT_QPA_PLATFORM']:
        env.pop(name,None)
    report = {'environment':'native Windows x64, clean system-only PATH',
              'package_folder':'Spiel Ordner ü, launched from Anderer Arbeitsordner',
              'tests':[]}
    def record(name,ok,detail):
        report['tests'].append({'name':name,'status':'bestanden' if ok else 'fehlgeschlagen','detail':detail})
    hashes = json.loads((source/'SHA256SUMS.json').read_text())
    record('all packaged SHA-256 values', all(hashlib.sha256((package/p).read_bytes()).hexdigest()==h
           for p,h in hashes.items()), str(len(hashes))+' files checked')
    data = (package/'swordfare.exe').read_bytes()
    pe = struct.unpack_from('<I',data,0x3c)[0]
    record('PE x64 machine',struct.unpack_from('<H',data,pe+4)[0]==0x8664,'IMAGE_FILE_MACHINE_AMD64')
    for flag,expected in [('--help',0),('--check-data',2),('--host-smoke',0),('--guest-smoke',0)]:
        p = subprocess.run([str(package/'swordfare.exe'),flag],cwd=elsewhere,env=env,
                           capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=45)
        record(flag,p.returncode==expected,{'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    starter = subprocess.run([str(Path(env['SYSTEMROOT'])/'System32/cmd.exe'),'/d','/c',
                              str(package/'Start-Swordigo.cmd')],cwd=elsewhere,env=env,input='\n',
                             capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=30)
    log = Path(env['LOCALAPPDATA'])/'SwordigoDesktop/logs/latest.log'
    record('starter missing-data diagnostic and per-user log',starter.returncode==2 and log.is_file()
           and 'Missing or invalid ARM64 ELF game library' in log.read_text(encoding='utf-8',errors='replace'),
           {'exit':starter.returncode,'stdout':starter.stdout,'stderr':starter.stderr})
    with zipfile.ZipFile(ROOT/'dist-windows/Swordigo-Windows-x64.zip') as archive:
        bad = [n for n in archive.namelist() if Path(n).name.lower().startswith('libswordigo') or n.lower().endswith('.apk')]
        record('archive excludes original game binaries/APKs',not bad,bad)
    report['gameplay']='This clean package test excludes originals; gameplay is not tested.'
    dest=ROOT/'docs/windows-package-tests.json'
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    for result in report['tests']:print(result['status'],result['name'])
    print('Report:',dest)
    if any(t['status']!='bestanden' for t in report['tests']):raise SystemExit(1)

if __name__=='__main__':
    main()
