# Contribution

## Pull requests

### Code style

The code style (line length, variable names, some PEP8, ...) is automatically tested for a PR with 
[Pylint](https://www.pylint.org/). You can also test it locally in advance, see 
[documentation](http://pylint.pycqa.org/en/latest/). 

### Commit message

The rules for commit messages are automatically tested in a PR with commitlint. If you want to test locally, 
please see the [documentation](https://commitlint.js.org/#/guides-local-setup). There are a few rules for commit 
rules (inspired by 
[Commit Message rules for TYPO3 CMS](https://docs.typo3.org/m/typo3/guide-contributionworkflow/master/en-us/Appendix/CommitMessage.html)):

#### Summary line (first line)

A summary line starts with a keyword and a brief summary of what the change does. The complete summary can be a 
maximum of 80 characters long.

Possible keywords are:

* `[BUGFIX]` Fix for a bug
* `[FEATURE]` New feature (also small additions)
* `[DOCS]` Documentation changes
* `[SECURITY]` Change fixes a security issue
* `[TASK]` Anything not covered by the above categories

After the keyword and a space, make sure to start the brief summary with a capital letter (sentence-case). Please 
write this message in imperative mood.

#### Description (Message body)

No rules, decide for yourself.

### Tests

There are no automatic software tests. Please test your adjustments on your device before you create a pull request.
I will do it too.
