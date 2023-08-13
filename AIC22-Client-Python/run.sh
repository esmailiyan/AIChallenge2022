rm -r dist
rm -r build
rm client.spec
pyinstaller --onefile src/client.py