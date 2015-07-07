# sbt-templates

Templates for creating new SBT projects. Currently this only creates the skeleton for a scala library.


##Usage

###Scala library

  `python scripts/bin/create_library.py <project_name>` 

where <project_name> is the name of the project to create.

This will then generate an SBT project with the following

- An SBT project based on sbt-auto-build and sbt-git-versioning
- An example class and test
- A .gitignore file
- Git config with origin pointing at github.com/hmrc/<project_name>
- A Travis build file
- Licences
- Readme with badges for Travis build status and Bintray links
- One commit for the above files tagged with version v0.1.0. This is necessary for sbt-git-versioning to start working.

Once this is done you may push your new project with:
  
  `git push -u origin master && git push origin v0.1.0`
