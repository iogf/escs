##############################################################################
# clone repo.
cd ~/projects
git clone git@github.com:iogf/escs.git escs-code
##############################################################################
# clone wiki.
cd ~/projects
git clone git@github.com:iogf/escs.wiki.git escs.wiki-code
##############################################################################
cd /home/tau/projects/escs.wiki-code/
git pull
##############################################################################
# create staging branch for wiki.
cd /home/tau/projects/escs.wiki-code/
git branch -a
git checkout -b staging
git push --set-upstream origin staging
##############################################################################
# push wiki docs.
cd /home/tau/projects/escs.wiki-code/
git status
git add *
git commit -a 
git push

##############################################################################
# clean .pyc files.
cd /home/tau/projects/escs-code/
find . -name "*.pyc" -exec rm -f {} \;
##############################################################################
# push code.
cd /home/tau/projects/escs-code/
git status
git add *
git commit -a 
git push
##############################################################################
git commit -m 'Fixing setup.py version.'
##############################################################################
# check patch patch.
cd /home/tau/projects/escs-code/
git checkout -b user-patch-name staging
git pull https://github.com/user/escs.git user-patch-name

# merge the patch.
git checkout staging
git merge --no-ff user-patch-name
git push origin staging
##############################################################################
# check out all.
cd /home/tau/projects/escs-code/
git checkout *
##############################################################################
# create staging branch.
cd /home/tau/projects/escs-code/
git branch -a
git checkout -b staging
git push --set-upstream origin staging
##############################################################################
# merge staging into main.
cd /home/tau/projects/escs-code/
git checkout main
git merge staging
git push
git checkout staging
##############################################################################
# merge staging into staging.
cd /home/tau/projects/escs-code/
git checkout staging
git merge staging
git checkout staging
git push

##############################################################################
# delete the staging branch.
cd /home/tau/projects/escs-code/
git branch -d staging
git push origin :staging
git fetch -p 
##############################################################################
# check diffs.
cd /home/tau/projects/escs-code/
git diff
git checkout *
##############################################################################
# install from pip requirements.
cd ~/projects/escs-code
pip install .
##############################################################################
# install escs. 
cd ~/projects/escs-code
sudo bash -i
python setup.py install
rm -fr build
exit
##############################################################################
# preview markdown docs.
cd /home/tau/projects/escs-code
markdown README.md > README.html
google-chrome README.html
rm README.html
##############################################################################
# generate table of contents TOC.
cd /home/tau/projects/escs-code
gh-md-toc BOOK.md >> table.md
escs table.md
rm table.md
##############################################################################
# build tarball.
cd /home/tau/projects/escs-code
python setup.py sdist 
rm -fr dist
rm MANIFEST
##############################################################################
# upload to pypi with twine.
cd ~/projects/escs-code
python setup.py sdist 
twine upload dist/*
rm -fr dist
##############################################################################
# install ycmd from source.

cd ~/bin/
git clone git@github.com:ycm-core/ycmd.git ycmd-code
cd ycmd-code
ls
git submodule update --init --recursive
ls

# Install ycmd-git.
cd ~/bin/
git clone git@github.com:ycm-core/ycmd.git ycmd-code
cd ycmd-code
ls
git submodule update --init --recursive

python build.py --all

mkdir build
cd build
cmake ../cpp -DUSE_PYTHON2=OFF -DUSE_LIBCLANG_COMPLETER=ON
make VERBOSE=1
##############################################################################
# Run tests.

cd projects/escs-code/tests
python -m unittest test_clipboard.py
