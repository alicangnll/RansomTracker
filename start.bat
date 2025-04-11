del instance\data.db
python -m flask db init
python -m flask db migrate
python -m flask db upgrade
python -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
python -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
del migrations\*
del migrations\versions\*
del migrations\versions
del migrations