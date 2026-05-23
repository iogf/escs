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
rm -fr build
rm -fr escs.egg-info
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
# create scan-refactor branch.
cd /home/tau/projects/escs-code/
git branch -a
git checkout -b scan-refactor
git push --set-upstream origin scan-refactor
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

cd ~/projects/escs-code/tests
make run-all
##############################################################################
make run-unit file=test_block_sel.py
make run-unit file=test_bracket_jumps.py
make run-unit file=test_c_mode.py
make run-unit file=test_clipboard.py
make run-unit file=test_code_comments.py
make run-unit file=test_extra_mode.py
make run-unit file=test_golang_mode.py
make run-unit file=test_html_mode.py
make run-unit file=test_insert_mode.py
make run-unit file=test_line_feed.py
make run-unit file=test_line_index.py
make run-unit file=test_line_sel.py
make run-unit file=test_nbook.py
make run-unit file=test_normal_mode.py
make run-unit file=test_pane_resize.py
make run-unit file=test_python_mode.py
make run-unit file=test_qsearch.py
make run-unit file=test_range_sel.py
make run-unit file=test_sneak.py
make run-unit file=test_spacing.py
make run-unit file=test_splits.py
make run-unit file=test_tab_search.py
make run-unit file=test_tabs.py
make run-unit file=test_text_jumps.py
make run-unit file=test_text_rename.py
make run-unit file=test_text_shift.py
make run-unit file=test_undo.py
make run-unit file=test_word_jumps.py
make run-unit file=test_word_sel.py
make run-unit file=test_xleaps.py
make run-unit file=test_xstr.py
make run-unit file=test_xstr_widgets.py
make run-unit file=test_brackets_sel.py
make run-unit file=test_fsearch.py

##############################################################################
# merge scan-refactor into main.
cd /home/tau/projects/escs-code/
git checkout staging
git merge scan-refactor
git push
git checkout staging
git status
##############################################################################
cd ~
ls -la | grep ssh
cd .ssh
ls -la
cat known_hosts
##############################################################################
cd /home/tau/projects/escs-code/
git status
git checkout spawn-refactor
pip install .
cd ~
mv .escs escs.tmp
cd /home/tau/projects/escs-code/
ls
rm -fr build/
rm -fr escs-egg-info
cd ~
rm -fr ~/.escs
mv escs.tmp .escs
git checkout staging
git branch -a
##############################################################################
# Set escs as default editor.
echo .bashrc << '
export EDITOR="vim"
export VISUAL="vim"
'

source ~/.bashrc
##############################################################################
# Use openssh-askpass to push git changes.
sudo dnf install openssh-askpass
