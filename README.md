##security-git-hooks

The purpose of these pre-commit hooks is to check against pre-defined rules in order to identify potential secrets in GitHub commits. Managing the content before it is committed can prevent the Leak Detection Service triggering an alert, and reduces the potential for secrets requiring manual removal from Git histories. Please note that, at the time of writing, these hooks do not check for the presence of a `repository.yaml` file.

###Installing the pre-commit framework

[this will change per installing package from our fork]

Run `pip3 install pre-commit`

 The `pre-commit install` command should then be run in relevant local repositories prior to first committing staged changes. The hooks will then run for every subsequent commit.

Further information can be found at the [pre-commit website](https://pre-commit.com/)

###Getting started 

A `.pre-commit-config.yaml` file is required in the root of the GitHub project directory in order to run the desired hooks against commits to that repository. The configuration file in this repository contains the details for every hook held here, so you can remove any you don't wish to use and/or directly copy over the configuration for new hooks without pulling down the entire current version of the file.


The basic format of the `.pre-commit-config.yaml` document is as follows:
<pre>
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v1.2.3
    hooks:
    -   id: trailing-whitespace
</pre>

* `repo` - Points to the repository containing the hook(s). Can be set to `local` for running/testing your own hooks which are yet to be checked in. This will point towards this repository, as we have opted to centralise the hooks we use as a security measure.

* `hooks` - Declares the `id`, and optionally the `name` of the hook, as well as the `language`, the `entrypoint`, and a list of any files to `exclude`.

See [here](https://pre-commit.com/#plugins) for more information on the `.pre-commit-config.yaml` document format.


You can forgo the pre-commit hooks entirely by use of the `--no-verify` flag, although due to the relationship between the `secrets-filename` and `secrets-filecontent` hooks and the Leak Detection Service, an LDS alert will be triggered by the commit for any files not on the LDS exception list.

###Installing other hooks or writing your own

The developers of the pre-commit framework have written various hooks, which can be found [here](https://github.com/pre-commit/pre-commit-hooks) along with additional information about the framework. We have included some popular hooks in this repository, however if you see a hook you would like to use which is external to the HMRC organisation, please post in `#team-platsec` or submit a pull request. Additionally, if you have written a hook and wish to include it in this repository, please submit a pull request with an update to the ReadMe and .pre-commit-config.yaml files

Pre-commit hooks themselves can be written in any language, however for a list of languages currently supported by the framework, please see [here](https://pre-commit.com/#new-hooks)

##Hooks in this respository

`secrets-filename` -  Checks against the LDS file extension ruleset as defined [here](https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf#L142)

`secrets-filecontent` - Checks against the LDS file content ruleset as defined [here](https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf#L92)

The test documents for these hooks can be found [here](), [here]() and [here](). 

If you wish to exclude certain files, file types or strings from these hooks, this can be done by updating the exclude parameter in the `.pre-commit-config.yaml` file. Please note that the exclusions must be provided as [Python compliant regex](https://www.debuggex.com/cheatsheet/regex/python) (which is very similar to PCRE). The known binary file types detailed [here](https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf#L76) are already on the exclusion list for the `secrets-filename` and `secrets-filecontent` hooks. Please note that any additional files excluded here will not be excluded by the Leak Detection Service.
