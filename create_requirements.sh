#!/bin/bash

pip freeze > tmp-requirements.txt
echo "python==3.10.6" > requirements.txt
cat tmp-requirements.txt >> requirements.txt
rm tmp-requirements.txt
