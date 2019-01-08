[![Download](https://api.bintray.com/packages/bitprim/bitprim/icu%3Abitprim/images/download.svg) ](https://bintray.com/bitprim/bitprim/icu%3Abitprim/_latestVersion)
[![Build Status](https://travis-ci.org/bitprim/conan-icu.svg?branch=stable%2F63.1)](https://travis-ci.org/bitprim/conan-icu)
[![Build status](https://ci.appveyor.com/api/projects/status/github/bitprim/conan-icu?branch=stable%2F63.1&svg=true)](https://ci.appveyor.com/project/bitprim/conan-icu)

[Conan.io](https://conan.io) package recipe for [*icu*](http://site.icu-project.org).

ICU is a mature, widely used set of C/C++ and Java libraries providing Unicode and Globalization support for software applications.

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/bitprim/bitprim/icu%3Abitprim).

## For Users: Use this package

### Basic setup

    $ conan install icu/63.1@bitprim/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    icu/63.1@bitprim/stable


Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to bitprim conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create bitprim/stable


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| with_unit_tests      | False |  [True, False] |
| silent      | True |  [True, False] |
| data_packaging      | archive |  ['files', 'archive', 'library', 'static'] |
| shared      | True |  [True, False] |

## Add Remote

    $ conan remote add bitprim "https://api.bintray.com/conan/bitprim/bitprim"

## Upload

    $ conan upload icu/63.1@bitprim/stable --all -r bitprim


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package icu.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/bitprim/conan-icu.git/blob/stable/63.1/LICENSE.md)

## Patches

Some of the MINGW patches have been obtained from the MINGW ICU Package of Alexpux's Github repository [MINGW-packages](https://github.com/Alexpux/MINGW-packages/tree/master/mingw-w64-icu).

