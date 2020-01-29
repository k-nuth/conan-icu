#
# Copyright (c) 2016-2020 Knuth Project.
#
# This file is part of Knuth Project.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import glob
import platform
import shutil
from conans import ConanFile, tools, AutoToolsBuildEnvironment
from kthbuild import KnuthConanFile

class ICUBase(KnuthConanFile):
    def recipe_dir(self):
        return os.path.dirname(os.path.abspath(__file__))

    name = "icu"
    version = "64.2"
    homepage = "http://site.icu-project.org"
    license = "ICU"
    description = "ICU is a mature, widely used set of C/C++ and Java libraries " \
                  "providing Unicode and Globalization support for software applications."
    url = "https://github.com/k-nuth/conan-icu"
    topics = ("conan", "icu", "icu4c", "i see you", "unicode")
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _env_build = None
    short_paths = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "data_packaging": ["files", "archive", "library", "static"],
               "with_unit_tests": [True, False],
               "silent": [True, False],
               "verbose": [True, False],
               "microarchitecture": "ANY",
               "fix_march": [True, False],
               "march_id": "ANY",
               }

    default_options = {"shared": False,
                       "fPIC": True,
                       "data_packaging": "archive",
                       "with_unit_tests": False,
                       "silent": True,
                       "verbose": True,
                       "microarchitecture": '_DUMMY_',
                       "fix_march": False,
                       "march_id": '_DUMMY_',
                        }

    # 64.2 url: "https://github.com/unicode-org/icu/releases/download/release-64-2/icu4c-64_2-src.tgz"
    # 64.2 sha256: "627d5d8478e6d96fc8c90fed4851239079a561a6a8b9e48b0892f24e82d31d6c"
    source_url = "https://github.com/unicode-org/icu/releases/download/release-{0}/icu4c-{1}-src.tgz".format(version.replace('.', '-'), version.replace('.', '_'))
    data_url = "https://github.com/unicode-org/icu/releases/download/release-{0}/icu4c-{1}-data.zip".format(version.replace('.', '-'), version.replace('.', '_'))

    @property
    def _the_os(self):
        return self.settings.get_safe("os") or self.settings.get_safe("os_build")

    @property
    def _the_arch(self):
        return self.settings.get_safe("arch") or self.settings.get_safe("arch_build")

    @property
    def _is_msvc(self):
        return self.settings.compiler == "Visual Studio"

    @property
    def _is_mingw(self):
        return self._the_os == "Windows" and self.settings.compiler == "gcc"

    def build_requirements(self):
        if self._the_os == "Windows":
            self.build_requires("msys2/20161025")

    def config_options(self):
        KnuthConanFile.config_options(self)

    def configure(self):
        KnuthConanFile.configure(self)

    # def source(self):
    #     tools.get(**self.conan_data["sources"][self.version])
    #     os.rename("icu", self._source_subfolder)

    def source(self):
        self.output.info("Fetching sources: {0}".format(self.source_url))
        tools.get(self.source_url)
        # os.rename(self.name, 'sources')
        os.rename(self.name, self._source_subfolder)

    def _replace_pythonpath(self):
        if self._is_msvc:
            srcdir = os.path.join(self.build_folder, self._source_subfolder, "source")
            configure = os.path.join(self._source_subfolder, "source", "configure")

            tools.replace_in_file(configure,
                                    'PYTHONPATH="$srcdir/data"',
                                    'PYTHONPATH="%s\\data"' % srcdir)
            tools.replace_in_file(configure,
                                    'PYTHONPATH="$srcdir/test/testdata:$srcdir/data"',
                                    'PYTHONPATH="%s\\test\\testdata;%s\\data"' % (srcdir, srcdir))

    def _workaround_icu_20545(self):
        if tools.os_info.is_windows:
            # https://unicode-org.atlassian.net/projects/ICU/issues/ICU-20545
            srcdir = os.path.join(self.build_folder, self._source_subfolder, "source")
            makeconv_cpp = os.path.join(srcdir, "tools", "makeconv", "makeconv.cpp")
            tools.replace_in_file(makeconv_cpp,
                                  "pathBuf.appendPathPart(arg, localError);",
                                  "pathBuf.append('/', localError); pathBuf.append(arg, localError);")

    def build(self):
        for filename in glob.glob("patches/*.patch"):
            self.output.info('applying patch "%s"' % filename)
            tools.patch(base_path=self._source_subfolder, patch_file=filename)

        if self._is_msvc:
            run_configure_icu_file = os.path.join(self._source_subfolder, 'source', 'runConfigureICU')

            flags = "-%s" % self.settings.compiler.runtime
            if self.settings.get_safe("build_type") == 'Debug':
                flags += " -FS"
            tools.replace_in_file(run_configure_icu_file, "-MDd", flags)
            tools.replace_in_file(run_configure_icu_file, "-MD", flags)

        self._replace_pythonpath() # ICU 64.1
        self._workaround_icu_20545()

        self._env_build = AutoToolsBuildEnvironment(self)
        if not self.options.get_safe("shared"):
            self._env_build.defines.append("U_STATIC_IMPLEMENTATION")
        if tools.is_apple_os(self._the_os):
            self._env_build.defines.append("_DARWIN_C_SOURCE")
            if self.settings.get_safe("os.version"):
                self._env_build.flags.append(tools.apple_deployment_target_flag(self._the_os,
                                                                            self.settings.os.version))

        build_dir = os.path.join(self.build_folder, self._source_subfolder, 'build')
        os.mkdir(build_dir)

        with tools.vcvars(self.settings) if self._is_msvc else tools.no_op():
            with tools.environment_append(self._env_build.vars):
                with tools.chdir(build_dir):
                    # workaround for https://unicode-org.atlassian.net/browse/ICU-20531
                    os.makedirs(os.path.join("data", "out", "tmp"))

                    self.run(self._build_config_cmd, win_bash=tools.os_info.is_windows)
                    if self.options.get_safe("silent"):
                        silent = '--silent' if self.options.silent else 'VERBOSE=1'
                    else:
                        silent = '--silent'
                    command = "make {silent} -j {cpu_count}".format(silent=silent,
                                                                    cpu_count=tools.cpu_count())
                    self.run(command, win_bash=tools.os_info.is_windows)
                    if self.options.get_safe("with_unit_tests"):
                        command = "make {silent} check".format(silent=silent)
                        self.run(command, win_bash=tools.os_info.is_windows)
                    command = "make {silent} install".format(silent=silent)
                    self.run(command, win_bash=tools.os_info.is_windows)

        self._install_name_tool()

    def package(self):
        if self._is_msvc:
            for dll in glob.glob(os.path.join(self.package_folder, 'lib', '*.dll')):
                shutil.move(dll, os.path.join(self.package_folder, 'bin'))

        self.copy("LICENSE", dst="licenses", src=os.path.join(self.source_folder, self._source_subfolder))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "share"))

    @staticmethod
    def detected_os():
        if tools.OSInfo().is_macos:
            return "Macos"
        if tools.OSInfo().is_windows:
            return "Windows"
        return platform.system()

    @property
    def cross_building(self):
        if tools.cross_building(self.settings):
            if self._the_os == self.detected_os():
                if self._the_arch == "x86" and tools.detected_architecture() == "x86_64":
                    return False
            return True
        return False

    @property
    def build_config_args(self):
        prefix = self.package_folder.replace('\\', '/')
        platform = {("Windows", "Visual Studio"): "Cygwin/MSVC",
                    ("Windows", "gcc"): "MinGW",
                    ("AIX", "gcc"): "AIX/GCC",
                    ("AIX", "xlc"): "AIX",
                    ("SunOS", "gcc"): "Solaris/GCC",
                    ("Linux", "gcc"): "Linux/gcc",
                    ("Linux", "clang"): "Linux",
                    ("Macos", "gcc"): "MacOSX",
                    ("Macos", "clang"): "MacOSX",
                    ("Macos", "apple-clang"): "MacOSX"}.get((str(self._the_os),
                                                             str(self.settings.compiler)))
        arch64 = ['x86_64', 'sparcv9', 'ppc64']
        bits = "64" if self._the_arch in arch64 else "32"
        args = [platform,
                "--prefix={0}".format(prefix),
                "--with-library-bits={0}".format(bits),
                "--disable-samples",
                "--disable-layout",
                "--disable-layoutex"]

        if self.cross_building:
            if self._env_build.build:
                args.append("--build=%s" % self._env_build.build)
            if self._env_build.host:
                args.append("--host=%s" % self._env_build.host)
            if self._env_build.target:
                args.append("--target=%s" % self._env_build.target)

        if self.options.get_safe("data_packaging"):
            args.append("--with-data-packaging={0}".format(self.options.data_packaging))
        else:
            args.append("--with-data-packaging=static")
        datadir = os.path.join(self.package_folder, "lib")
        datadir = datadir.replace("\\", "/") if tools.os_info.is_windows else datadir
        args.append("--datarootdir=%s" % datadir)  # do not use share
        bindir = os.path.join(self.package_folder, "bin")
        bindir = bindir.replace("\\", "/") if tools.os_info.is_windows else bindir
        args.append("--sbindir=%s" % bindir)

        if self._is_mingw:
            mingw_chost = 'i686-w64-mingw32' if self._the_arch == 'x86' else 'x86_64-w64-mingw32'
            args.extend(["--build={0}".format(mingw_chost),
                         "--host={0}".format(mingw_chost)])

        if self.settings.get_safe("build_type") == "Debug":
            args.extend(["--disable-release", "--enable-debug"])
        if self.options.get_safe("shared"):
            args.extend(["--disable-static", "--enable-shared"])
        else:
            args.extend(["--enable-static", "--disable-shared"])
        if not self.options.get_safe("with_unit_tests"):
            args.append('--disable-tests')
        return args

    @property
    def _build_config_cmd(self):
        return "../source/runConfigureICU %s" % " ".join(self.build_config_args)

    def _install_name_tool(self):
        if tools.is_apple_os(self._the_os):
            with tools.chdir(os.path.join(self.package_folder, 'lib')):
                for dylib in glob.glob('*icu*.{0}.dylib'.format(self.version)):
                    command = 'install_name_tool -id {0} {1}'.format(os.path.basename(dylib), dylib)
                    self.output.info(command)
                    self.run(command)

    def package_id(self):
        KnuthConanFile.package_id(self)

        del self.info.options.with_unit_tests   # ICU unit testing shouldn't affect the package's ID
        del self.info.options.silent            # Verbosity doesn't affect package's ID
        del self.info.options.verbose           # Verbosity doesn't affect package's ID
        del self.info.options.microarchitecture #TODO(fernando): implement it
        del self.info.options.fix_march
        del self.info.options.march_id          #TODO(fernando): implement it

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def package_info(self):
        def lib_name(lib):
            name = lib
            if self.settings.os == "Windows":
                if not self.options.shared:
                    name = 's' + name
                if self.settings.build_type == "Debug":
                    name += 'd'
            return name

        libs = ['icuin' if self.settings.os == "Windows" else 'icui18n',
                'icuio', 'icutest', 'icutu', 'icuuc',
                'icudt' if self.settings.os == "Windows" else 'icudata']
        self.cpp_info.libs = [lib_name(lib) for lib in libs]
        self.cpp_info.bindirs.append('lib')

        data_dir_name = self.name
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            data_dir_name += 'd'
        data_dir = os.path.join(self.package_folder, 'lib', data_dir_name, self.version)
        vtag = self.version.split('.')[0]
        data_file = "icudt{v}l.dat".format(v=vtag)
        data_path = os.path.join(data_dir, data_file).replace('\\', '/')
        if self.options.get_safe("data_packaging") in ["files", "archive"]:
            self.env_info.ICU_DATA.append(data_path)

        if not self.options.shared:
            self.cpp_info.defines.append("U_STATIC_IMPLEMENTATION")
        if self.settings.os == 'Linux':
            self.cpp_info.libs.append('dl')

        if self.settings.os == 'Windows':
            self.cpp_info.libs.append('advapi32')