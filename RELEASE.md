Publication Instructions
-------------------------------
http://peterdowns.com/posts/first-time-with-pypi.html

Updating Instructions
----------------------------

First, release a new version and push to github repo.

Then update the setup.py file to reflect the new version.

adding a tag
-----------------
git tag 0.1 -m "Adds a tag so that we can put this on PyPI."

run registering and updating

How to upgrade
*****************
1) After commiting changes, make a new release tag and change the setup.py file to reflect this

2) Then push with tags
  git push github master --tags

3) run the test registering and uploading using
  python setup.py register -r pypitest
  python setup.py sdist upload -r pypitest

  python setup.py register -r pypi
  python setup.py sdist upload -r pypi


4) upgrade package
  pip install clustergrammer --upgrade
  pip show clustergrammer