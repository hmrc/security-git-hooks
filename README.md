# security-git-hooks

The purpose of these pre-commit Git hooks is to check file types and content against pre-defined rules in order to identify potentially sensitive information prior to commit. Managing sensitive content before it is committed to GitHub helps maintain our overall security posture, and also helps prevent the Leak Detection Service (LDS) triggering an alert, thus reducing the potential for secrets requiring manual removal from Git histories and for keys which would then require cycling.  

*NOTE:* These hooks do not check for the presence of a `repository.yaml` file and have no relationship with the LDS exemptions defined there. Our pre-commit hooks use inline exclusions. Simply add a comment on the line above the content containing the string `LDS ignore`, and the hook will skip the line. **NB** - This functionality will soon be extended to the LDS itself - see [this ticket](https://jira.tools.tax.service.gov.uk/browse/BDOG-192) for details, however please be mindful that your `repository.yaml` exclusions will need to be maintained for now.

## Installation

`pip3 install pre-commit`


## Getting started 

* Navigate to the root directory of a repository you wish to run hooks in.
* Run the command: `pre-commit install`.
* If there is no `.pre-commit-config.yaml` file present, create one. This is how the pre-commit framework installs and runs selected hooks.  This file must be included in any repository utilising the framework.  The following content, pasted directly into your `.pre-commit-config.yaml` file, will install all hooks present in this repository. Alternatively, if you have chosen to clone this repository, you can directly copy the `.pre-commit-config.yaml` contained here into whichever directory you're running hooks in.

```
repos:
-   repo: https://github.com/hmrc/security-git-hooks
    rev: v1.0.0-beta9
    hooks:
    -   id: secrets_filecontent
        name: Checking staged files for sensitive content
        exclude: ".tar$|.gz$|.jar$|.7z$|.rar$|.bz2$|.zip$|.gzip$|.war$|.ear$|.xlsx$|.xls$|
                |.docx$|.doc$|.pptx$|.pdf$|.jpg$|.png$|.jpeg$|.tif$|.tiff$|.gif$|.bmp$|.webp$|.svg$|.ico$|.psd$|.exe$|.dll$|.dmg$|.de$|.rpm$"
    -   id: secrets_filename
        name: Checking staged files for sensitive file types
        exclude: ".tar$|.gz$|.jar$|.7z$|.rar$|.bz2$|.zip$|.gzip$|.war$|.ear$|.xlsx$|.xls$|
                |.docx$|.doc$|.pptx$|.pdf$|.jpg$|.png$|.jpeg$|.tif$|.tiff$|.gif$|.bmp$|.webp$|.svg$|.ico$|.psd$|.exe$|.dll$|.dmg$|.de$|.rpm$"
    -   id: hooks_version_check
        name: Checking local hooks against latest release
        verbose: true

```

### Quick test
In order to quickly check if everything is working as expected, test with:

* Change into your selected repository.
* Create a dummy file to test the file type check: `touch fake.key.pem`
* Create a dummy file to test the file content check: `echo aws_secret_access_key = 1ye+VarkHMg7o6MNjwWIqOYICe03lfA+KPPAmeaY > fake.aws.file`
* Test with: `git add -A && git commit -m 'testing pre-commits'`

You should see the following output:
```
$ git add -A && git commit -m 'testing pre-commits'
Check file content for potential secrets.................................Failed
hookid: secrets_filecontent

fake.key.pem may contain sensitive information due to the file type

Check filenames for potential secrets....................................Failed
hookid: secrets_filename

Potentially sensitive string matching rule: aws_2 found on line 1 of fake.aws.file

```

### Definitions
* `repo` - Points to the repository containing the hook(s). Can be set to `local` for running/testing your own hooks, although additional information (which wouold usually be included in the `.pre-commit-hooks.yaml` is required if this is the case).

* `hooks` - Declares the `id`, and optionally the local `name` of the hook. There are further options to include `language`,  `entrypoint`, and a list of any files to `exclude`. Although this information should not be included generally as it can be found in the `.pre-commit-hooks.yaml` file, the exclusions have been provided as part of the configuration file to provide additional user choice in this case. The default exclusions here are in line with the filetypes excluded by the Leak Detection Service itself, although any changes made to your exclusion list will not affect the Leak Detection Service.  

See [here](https://pre-commit.com/#plugins) for more information on the `.pre-commit-config.yaml` document format.

*NOTE:* Exclusions must be provided as [Python compliant regex](https://www.debuggex.com/cheatsheet/regex/python)

## Usage

If you wish to run hooks without committing, pre-commit can be used as a general scanning tool with the `pre-commit run --all-files` or `pre-commit run <hook name>` commands, providing Git is initialised and pre-commit installed in the relevant repository.

You can forgo the pre-commit hooks entirely by use of the `--no-verify` flag, although due to the relationship between the `secrets-filename` and `secrets-filecontent` hooks and the Leak Detection Service, an LDS alert will be triggered by the commit for any files not on the exemption list contained within your `repository.yaml` file.

You can update hooks to point directly at the latest tagged version of a hook by using `pre-commit autoupdate`, or alternatively, `pre-commit autoupdate --bleeding-edge` will point at the latest version of main.

### Installing other hooks or writing your own

The developers of the pre-commit framework have written various hooks, which can be found [here](https://github.com/hmrc/pre-commit-hooks) along with additional information about the framework. If you see a hook you would like to use which is external to the HMRC organisation, please check the license and post in the `#community-security` slack channel so we can mirror it if appropriate. Additionally, if you have written a hook and wish to include it in this repository, please submit a pull request with an update to the `README` and `.pre-commit-config.yaml` files. The decision to host hooks exclusively in our own repository was taken as a security measure, **as the hook mechanism allows for any malicious code to be executed, should it be checked in to the repository which holds the hook**. This is a set recommendation to all users in the HMRC organisation.

Pre-commit hooks themselves can be written in any language, however for a list of languages currently supported by the framework, please see [here](https://pre-commit.com/#new-hooks)

## Hooks in this respository

`secrets-filename` -  Checks against the LDS file extension ruleset as defined [here](https://github.com/hmrc/app-config-base/blob/HEAD/leak-detection.conf#L142)

`secrets-filecontent` - Checks against the LDS file content ruleset as defined [here](https://github.com/hmrc/app-config-base/blob/HEAD/leak-detection.conf#L92)

`hooks-version-check` - Checks the tag from your `.pre-commit-config.yaml` file against the latest tagged release in the repository. This is an information only hook, and will provide output but always pass.

You can test the hooks by cloning this repository and running `tox` in the root directory.
