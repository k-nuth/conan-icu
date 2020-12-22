[![Download](https://api.bintray.com/packages/k-nuth/kth/icu%3Akth/images/download.svg) ](https://bintray.com/k-nuth/kth/icu%3Akth/_latestVersion)
[![Build Status](https://travis-ci.org/k-nuth/conan-icu.svg?branch=stable%2F68.2)](https://travis-ci.org/kth/conan-icu)
[![Build status](https://ci.appveyor.com/api/projects/status/github/k-nuth/conan-icu?branch=stable%2F68.2&svg=true)](https://ci.appveyor.com/project/k-nuth/conan-icu)
[![Build Status](https://api.cirrus-ci.com/github/k-nuth/conan-icu.svg?branch=master)](https://cirrus-ci.com/github/k-nuth/conan-icu)

[Conan.io](https://conan.io) package recipe for [*icu*](http://site.icu-project.org).

ICU is a mature, widely used set of C/C++ and Java libraries providing Unicode and Globalization support for software applications.

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/k-nuth/kth/icu%3Akth).

## For Users: Use this package

### Basic setup

    $ conan install icu/68.2@kth/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    icu/68.2@kth/stable


Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to Knuth conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create knuth/stable


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| with_unit_tests      | False |  [True, False] |
| silent      | True |  [True, False] |
| data_packaging      | archive |  ['files', 'archive', 'library', 'static'] |
| shared      | True |  [True, False] |

## Add Remote

    $ conan remote add kth "https://api.bintray.com/conan/k-nuth/kth"

## Upload

    $ conan upload icu/68.2@kth/stable --all -r kth


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package icu.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/k-nuth/conan-icu.git/blob/stable/68.2/LICENSE.md)

