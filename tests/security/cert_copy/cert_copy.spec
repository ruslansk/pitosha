# -*- mode: python -*-
a = Analysis(['cert_copy.py'],
             pathex=['C:\\Projects\\hello'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='cert_copy.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
