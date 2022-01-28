echo Compiling wat file ...
wat2wasm wat/out.wat -o wat/out.wasm 
if [ $? -eq 0 ]
then
  echo Starting python web server on port 8080
  python3 -m http.server 8080
else
  echo "Failure: Compiling error !" >&2
  exit 1
fi
