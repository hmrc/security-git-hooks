# security-git-hooks

The purpose of these pre-commit hooks is to check file types and content against pre-defined rules in order to identify potential secrets in GitHub commits. Managing sensitive content before it is committed can prevent the Leak Detection Service triggering an alert, and reduces the potential for secrets requiring manual removal from Git histories. Please note that, at the time of writing, these hooks do not check for the presence of a `repository.yaml` file, and have no relationship with the LDS exclusions defined there.

### Installing the pre-commit framework

We have opted to fork the pre-commit project and advise members of the HMRC organisation to install from our source. Instructions for installing the framework directly from the maintainer can be found at  the [pre-commit website](https://pre-commit.com/).

In order to install per our recommendation: 

* Clone [this fork](https://github.com/hmrc/pre-commit)
* Navigate to the root of the pre-commit repository on your machine, and run `pip install . `


### Getting started 

* Navigate to the root directory of a repository you wish to run hooks in.
* Run the command `pre-commit install`.
* Create a `.pre-commit-config.yaml` file. This is how the pre-commit framework installs and runs selected hooks, and must be included in any repository utilising the framework.
    * The following content, pasted directly into your `.pre-commit-config.yaml` file, will install the two hooks from this repository.
<pre>
repos:
-   repo: https://github.com/hmrc/security-git-hooks
    rev: master
    hooks:
    -   id: secrets_filecontent
        exclude: ".tar$|.gz$|.jar$|.7z$|.rar$|.bz2$|.zip$|.gzip$|.war$|.ear$|.xlsx$|.xls$|
                |.docx$|.doc$|.pptx$|.pdf$|.jpg$|.png$|.jpeg$|.tif$|.tiff$|.gif$|.bmp$|.webp$|.svg$|.ico$|.psd$|.exe$|.dll$|.dmg$|.de$|.rpm$"
    -   id: secrets_filename
        exclude: ".tar$|.gz$|.jar$|.7z$|.rar$|.bz2$|.zip$|.gzip$|.war$|.ear$|.xlsx$|.xls$|
                |.docx$|.doc$|.pptx$|.pdf$|.jpg$|.png$|.jpeg$|.tif$|.tiff$|.gif$|.bmp$|.webp$|.svg$|.ico$|.psd$|.exe$|.dll$|.dmg$|.de$|.rpm$"

</pre>

* `repo` - Points to the repository containing the hook(s). Can be set to `local` for running/testing your own hooks, although additional information (which wouold usually be included in the `.pre-commit-hooks.yaml` is required if this is the case).



* `hooks` - Declares the `id`, and optionally the local `name` of the hook. There is the option to include the `language`, the `entrypoint`, and a list of any files to `exclude`, although this information should not be included generally as it can be found in the `.pre-commit-hooks.yaml` file. The exclusions have been provided as part of the configuration file to provide additional user choice in this case. The default exclusions here are in line with the filetypes excluded by the Leak Detection Service itself, although any changes made to your exclusion list will not affect leak detection alerting. Please note that the exclusions must be provided as [Python compliant regex](https://www.debuggex.com/cheatsheet/regex/python) (which is very similar to PCRE).


    See [here](https://pre-commit.com/#plugins) for more information on the `.pre-commit-config.yaml` document format.

### Usage

If you wish to run hooks without committing, pre-commit can be used as a general scanning tool with the `pre-commit run --all-files` or `pre-commit run <hook name>` commands, providing git is initialised and pre-commit installed in the relevant repository.

You can forgo the pre-commit hooks entirely by use of the `--no-verify` flag, although due to the relationship between the `secrets-filename` and `secrets-filecontent` hooks and the Leak Detection Service, an LDS alert will be triggered by the commit for any files not on the exemption list contained within your `repository.yaml` file.

You can automatically update hooks to point directly at the latest tagged version of a hook by using `pre-commit autoupdate`, or alternatively, `pre-commit autoupdate --bleeding-edge` will point at the latest version of master.

### Installing other hooks or writing your own

The developers of the pre-commit framework have written various hooks, which can be found [here](https://github.com/pre-commit/pre-commit-hooks) along with additional information about the framework. We have included some popular hooks in this repository, however if you see a hook you would like to use which is external to the HMRC organisation, please check the license and post in the `#community-security` slack channel. Additionally, if you have written a hook and wish to include it in this repository, please submit a pull request with an update to the `README` and `.pre-commit-config.yaml` files. The decision to host hooks in our own repository was taken as a security measure, as the hook update mechanism potentially allows for malicious code to be executed, should it be checked in to the repository holding the hook.

Pre-commit hooks themselves can be written in any language, however for a list of languages currently supported by the framework, please see [here](https://pre-commit.com/#new-hooks)

### Hooks in this respository

`secrets-filename` -  Checks against the LDS file extension ruleset as defined [here](https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf#L142)

`secrets-filecontent` - Checks against the LDS file content ruleset as defined [here](https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf#L92)

You can test the hooks by cloning this repository and running `pytest` in the root directory.



