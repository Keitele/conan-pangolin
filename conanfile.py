#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import get
from conan.tools.files import apply_conandata_patches
from conan.tools.files import export_conandata_patches

class PangolinConan(ConanFile):
    name         = 'pangolin'
    version      = '0.8'
    license      = 'MIT'
    url          = 'https://github.com/stevenlovegrove/Pangolin.git'
    description  = ''
    settings     = 'os', 'compiler', 'build_type', 'arch'

    options      = {
        'shared':  [True, False],
        'fPIC':    [True, False],
    }
    default_options = { "shared": True, "fPIC": True, 
                        "eigen/*:shared": True,
                        "opengl/*:shared": True,
                        "glew/*:shared": True,
                        }
    exports_sources = "patches/*.patch"

    def requirements(self):
        self.requires("eigen/3.4.0")
        self.requires("opengl/system")
        self.requires("glew/2.2.0")

    def source(self):
        get(self, **self.conan_data["sources"][self.version])
        apply_conandata_patches(self)
        
    def export_sources(self):
        export_conandata_patches(self)
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        # cmake_layout(self)

        ## Project folder structure
        self.folders.source = "."
        self.folders.build = os.path.join("build", str(self.settings.build_type))
        self.folders.generators = os.path.join(self.folders.build, "generators")

        ### Will be used in the Conan cache, equivalent to 'cpp_info'
        # self.cpp.package.libs = ['pango_core', 'pango_display', 'pango_vars']#collect_libs(self)
        # self.cpp.package.includedirs = [
        #                                  "components/pango_core/include", 
        #                                 ] # includedirs is already set to 'include' by

        # self.cpp.package.libdirs = [ "lib" ]         # libdirs is already set to 'lib' by
        # self.cpp.package.libs = [] 

        ### ###
        ## for EDITABLE packages:
        ## self.cpp.source - describe artifacts under self.source_folder
        self.cpp.source.includedirs = [
                                        "components/pango_core/include", 
                                        "components/pango_display/include",
                                        "components/pango_geometry/include",
                                        "components/pango_glgeometry/include",
                                        "components/pango_image/include",
                                        "components/pango_packetstream/include",
                                        "components/pango_plot/include",
                                        "components/pango_python/include",
                                        "components/pango_scene/include",
                                        "components/pango_tools/include",
                                        "components/pango_vars/include",
                                        "components/pango_video/include",
                                        "components/pango_opengl/include",
                                        "components/pango_windowing/include",
                                        ]
        ## for EDITABLE packages:
        ## self.cpp.build - describe artifacts under self.build_folder
        ## "libs" will be merged with "cpp.package.libs"
        self.cpp.build.libdirs = ["."]  # map to ./build/<build_type>

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_TOOLS"] = False
        tc.variables["BUILD_EXAMPLES"] = False
        tc.variables["BUILD_ASAN"] = False
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        # self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "pangolin")

        self.cpp_info.components["pango_core"].set_property("cmake_target_name", "pango_core")
        self.cpp_info.components["pango_core"].libs = [ "pango_core" ]
        self.cpp_info.components["pango_display"].set_property("cmake_target_name", "pango_display")
        self.cpp_info.components["pango_display"].libs = [ "pango_display" ]
        self.cpp_info.components["pango_display"].requires = [ "pango_core", "pango_opengl", "pango_windowing", "pango_vars" ]

        self.cpp_info.components["pango_geometry"].set_property("cmake_target_name", "pango_geometry")
        self.cpp_info.components["pango_geometry"].defines = ["HAVE_EIGEN"]
        self.cpp_info.components["pango_geometry"].libs = [ "pango_geometry" ]
        self.cpp_info.components["pango_geometry"].requires = [ "pango_core", "pango_image", "tinyobj", "eigen::eigen" ]

        self.cpp_info.components["pango_glgeometry"].set_property("cmake_target_name", "pango_glgeometry")
        self.cpp_info.components["pango_glgeometry"].libs = [ "pango_glgeometry" ]
        self.cpp_info.components["pango_glgeometry"].requires = [ "pango_geometry", "pango_opengl" ]

        self.cpp_info.components["pango_image"].set_property("cmake_target_name", "pango_image")
        self.cpp_info.components["pango_image"].libs = [ "pango_image" ]
        self.cpp_info.components["pango_image"].requires = [ "pango_core" ]

        self.cpp_info.components["pango_opengl"].set_property("cmake_target_name", "pango_opengl")
        self.cpp_info.components["pango_opengl"].defines = ["HAVE_GLEW", "HAVE_EIGEN"]
        self.cpp_info.components["pango_opengl"].libs = [ "pango_opengl" ]
        self.cpp_info.components["pango_opengl"].requires = [ "pango_core", "pango_image", "eigen::eigen", "glew::glew", "opengl::opengl" ]
        self.cpp_info.components["pango_opengl"].system_libs.append("OpenGL")
        self.cpp_info.components["pango_opengl"].system_libs.append("GLEW")

        self.cpp_info.components["pango_packetstream"].set_property("cmake_target_name", "pango_packetstream")
        self.cpp_info.components["pango_packetstream"].libs = [ "pango_packetstream" ]
        self.cpp_info.components["pango_packetstream"].requires = [ "pango_core" ]

        self.cpp_info.components["pango_plot"].set_property("cmake_target_name", "pango_plot")
        self.cpp_info.components["pango_plot"].libs = [ "pango_plot" ]
        self.cpp_info.components["pango_plot"].requires = [ "pango_display" ]

        self.cpp_info.components["pango_python"].set_property("cmake_target_name", "pango_python")
        self.cpp_info.components["pango_python"].libs = [ "pango_python" ]
        self.cpp_info.components["pango_python"].requires = [ "pango_core", "pango_display", "pango_plot", "pango_video", "pango_vars" ]

        self.cpp_info.components["pango_scene"].set_property("cmake_target_name", "pango_scene")
        self.cpp_info.components["pango_scene"].libs = [ "pango_scene" ]
        self.cpp_info.components["pango_scene"].requires = [ "pango_opengl" ]

        self.cpp_info.components["pango_tools"].set_property("cmake_target_name", "pango_tools")
        self.cpp_info.components["pango_tools"].libs = [ "pango_tools" ]
        self.cpp_info.components["pango_tools"].requires = [ "pango_display", "pango_video" ]

        self.cpp_info.components["pango_vars"].set_property("cmake_target_name", "pango_vars")
        self.cpp_info.components["pango_vars"].libs = [ "pango_vars" ]
        self.cpp_info.components["pango_vars"].requires = [ "pango_core" ]

        self.cpp_info.components["pango_video"].set_property("cmake_target_name", "pango_video")
        self.cpp_info.components["pango_video"].libs = [ "pango_video" ]
        self.cpp_info.components["pango_video"].requires = [ "pango_core", "pango_image", "pango_packetstream" ]

        self.cpp_info.components["pango_windowing"].set_property("cmake_target_name", "pango_windowing")
        self.cpp_info.components["pango_windowing"].libs = [ "pango_windowing" ]
        self.cpp_info.components["pango_windowing"].requires = [ "pango_core", "pango_opengl" ]

        self.cpp_info.components["tinyobj"].set_property("cmake_target_name", "tinyobj")
        self.cpp_info.components["tinyobj"].libs = [ "tinyobj" ]
        self.cpp_info.components["tinyobj"].requires = []