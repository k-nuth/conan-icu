import os
# from conan.packager import ConanMultiPackager
from kthbuild import get_base_march_ids, get_builder, handle_microarchs, copy_env_vars, filter_valid_exts, filter_marchs_tests

if __name__ == "__main__":
    # builder = ConanMultiPackager(username="kth", channel="stable", archs=["x86_64"]
    #                             , remotes="https://api.bintray.com/conan/k-nuth/kth")
    # builder.add_common_builds(shared_option_name="icu:shared", pure_c=False)

    builder, name = get_builder(os.path.dirname(os.path.abspath(__file__)))
    builder.add_common_builds(shared_option_name="%s:shared" % name)

    march_ids = get_base_march_ids()

    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:

        if (settings["build_type"] == "Release" or settings["build_type"] == "Debug") \
                and not options["icu:shared"] \
                and (not "compiler.libcxx" in settings or settings["compiler.libcxx"] != "libstdc++11"):

            handle_microarchs("%s:march_id" % name, march_ids, filtered_builds, settings, options, env_vars, build_requires)
            # filtered_builds.append([settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    builder.run()
