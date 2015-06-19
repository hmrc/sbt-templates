#!/usr/bin/env python

import sys
import argparse
import os
import distutils.core
import subprocess
import fileinput

import pyratemp


def required_environment_directory(environment_variable, description_for_error):
    directory = os.environ.get(environment_variable, None)
    if not directory:
        print "'%s' environment variable is required. You can add this to your ~/.bash_profile by adding the line %s=[%s]" % (
            environment_variable, environment_variable, description_for_error)
        exit(1)
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print "Error: '%s' environment variable points to non-existent directory: %s" % (
            environment_variable, directory)
        sys.exit(1)
    return directory


workspace = required_environment_directory("WORKSPACE", "your workspace root directory")


def to_camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def replace_variables_for_app(folder_to_search, application_name):
    for subdir, dirs, files in os.walk(folder_to_search):
        for f in files:
            file_name = os.path.join(subdir, f)
            t = pyratemp.Template(filename=os.path.join(subdir, f))
            file_content = t(UPPER_CASE_APP_NAME=application_name.upper(),
                             UPPER_CASE_APP_NAME_UNDERSCORE_ONLY=application_name.upper().replace("-", "_"),
                             APP_NAME_UNDERSCORE_ONLY=to_camel_case(application_name.replace("-", "_")),
                             APP_NAME=application_name,
                             bashbang="#!/bin/bash",
                             shbang="#!/bin/sh",
            )
            write_to_file(file_name, file_content)


def write_to_file(f, file_content):
    open_file = open(f, 'w')
    open_file.write(file_content)
    open_file.close()


def replace_in_file(file_to_search, replace_this, with_this):
    for line in fileinput.input(file_to_search, inplace=True):
        print line.replace(replace_this, with_this),


def call(command, quiet=True):
    if not quiet:
        print "calling: '" + command + "' from: '" + os.getcwd() + "'"
    ps_command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ps_command.wait()
    return ps_command


def initialise_git_repo(folder, project_name):
    os.chdir(folder)
    call('git init .')
    call('git add . -A')
    call('git commit -m \"Creating new library %s\"' % project_name)
    call('git remote add origin git@github.com/hmrc%s.git' % project_name)
    call('git tag -a -m\"creating new library\" v0.1.0')


def create_library(project_root_name, stub_template_folder):
    project_name = project_root_name
    print "Creating new library: %s" % project_name
    project_folder = os.path.normpath(os.path.join(workspace, project_name))
    if os.path.isdir(project_folder):
        print "The folder '%s' already exists, not creating front end module" % str(project_folder)
    else:
        distutils.dir_util.copy_tree(stub_template_folder, project_folder)
        replace_variables_for_app(project_folder, project_name)

        initialise_git_repo(project_folder, project_name)
        print "Created library project at '%s'." % project_folder
        print ""
        print "You can now finish by doing the following from within the folder:"
        print ""
        print "git push -u origin master && git push origin v0.1.0"
        print ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create open HMRC libraries')
    parser.add_argument('PROJECT_NAME', type=str, help='The name of the project you want to create')
    args = parser.parse_args()

    template_dir = os.path.normpath(os.path.join(os.path.realpath(__file__), "../../../templates/library"))

    create_library(args.PROJECT_NAME, template_dir)