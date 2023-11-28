# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyXgboost(PythonPackage):
    """XGBoost is an optimized distributed gradient boosting library designed to be
    highly efficient, flexible and portable."""

    homepage = "https://xgboost.ai/"
    pypi = "xgboost/xgboost-1.3.3.tar.gz"

    maintainers("adamjstewart")
    import_modules = ["xgboost"]

    version("2.0.2", sha256="55b5188e6da1d61f02f30a5dd8daffc3a6b5bb975a7249bf381dc1754dc89688")
    version("2.0.0", sha256="a89a4504c486043dbfdad41e5f426e2a0b4e5494a5f3ca99cf7ad85a665c79e7")
    version("1.7.6", sha256="1c527554a400445e0c38186039ba1a00425dcdb4e40b37eed0e74cb39a159c47")
    version("1.6.2", sha256="e1f5c91ba88cf8edb409d7fd2ca150dcd80b6f2115587d87365f0c10b2d4f009")
    version("1.6.1", sha256="24072028656f3428e7b8aabf77340ece057f273e41f7f85d67ccaefb7454bb18")
    version("1.5.2", sha256="404dc09dca887ef5a9bc0268f882c54b33bfc16ac365a859a11e7b24d49da387")
    version("1.3.3", sha256="397051647bb837915f3ff24afc7d49f7fca57630ffd00fb5ef66ae2a0881fb43")

    variant("pandas", default=False, description="Enable Pandas extensions for training.")
    variant(
        "scikit-learn", default=False, description="Enable scikit-learn extensions for training."
    )
    variant("dask", default=False, description="Enables Dask extensions for distributed training.")
    variant("plotting", default=False, description="Enables tree and importance plotting.")

    for ver in ["1.3.3", "1.5.2", "1.6.1", "1.6.2", "1.7.6", "2.0.0", "2.0.2"]:
        depends_on("xgboost@" + ver, when="@" + ver)

    depends_on("python@3.7:", when="@1.6:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
    # in newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", when="@:1", type="build")
    depends_on("py-pip", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))

    depends_on("py-pandas", when="+pandas", type=("build", "run"))

    depends_on("py-scikit-learn", when="+scikit-learn", type=("build", "run"))

    depends_on("py-dask", when="+dask", type=("build", "run"))
    depends_on("py-pandas", when="+dask", type=("build", "run"))
    depends_on("py-distributed", when="+dask", type=("build", "run"))

    depends_on("py-graphviz", when="+plotting", type=("build", "run"))
    depends_on("py-matplotlib", when="+plotting", type=("build", "run"))

    def patch(self):
        # https://github.com/dmlc/xgboost/issues/6706
        # 'setup.py' is hard-coded to search in Python installation prefix
        filter_file(
            "lib_path = os.path.join(sys.prefix, 'lib')",
            "lib_path = '{0}'".format(self.spec["xgboost"].libs.directories[0]),
            "setup.py",
            string=True,
        )

        # Same for run-time search
        filter_file(
            "os.path.join(curr_path, 'lib'),",
            "'{0}',".format(self.spec["xgboost"].libs.directories[0]),
            os.path.join("xgboost", "libpath.py"),
            string=True,
        )

    def install_options(self, spec, prefix):
        return ["--use-system-libxgboost"]
