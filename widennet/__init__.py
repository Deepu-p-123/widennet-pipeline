# widennet/__init__.py
#
# WIDENNET — Smart Contract Vulnerability Detection
# Copyright (C) 2026  Deepu P <pdeepuprakash@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Based on:
#   Osei, S. B., Ma, Z., & Huang, R. (2024).
#   Smart Contract Vulnerability Detection Using Wide and Deep Neural Network.
#   Science of Computer Programming, Vol. 238, 103172.
#   https://doi.org/10.1016/j.scico.2024.103172

"""
WIDENNET: Smart Contract Vulnerability Detection
=================================================

A deep learning pipeline for detecting reentrancy and timestamp dependence
vulnerabilities in Ethereum smart contracts using a Wide & Deep Neural Network.

Quick Start
-----------
    from widennet import predict_vulnerability

    result = predict_vulnerability("path/to/contract.sol")
    print(result)
    # {
    #   "reentrancy": "Vulnerable",
    #   "reentrancy_confidence": 0.97,
    #   "timestamp": "Safe",
    #   "timestamp_confidence": 0.82
    # }

Modules
-------
- model       : WIDENNET architecture (Wide & Deep, Keras)
- preprocess  : Solidity → bytecode → opcode normalisation
- encode      : Opcode vocabulary and embedding lookup
- train       : Model training entry point
- evaluate    : Accuracy, F1, precision, recall metrics
- predict     : Single and batch inference
- api         : FastAPI REST interface

License
-------
GNU General Public License v3.0 — see LICENSE for details.
"""

__version__ = "1.0.1"
__author__ = "Deepu P"
__email__ = "pdeepuprakash@gmail.com"
__license__ = "GPL-3.0"
__url__ = "https://github.com/Deepu-p-123/widennet-pipeline"

from widennet.model import build_widennet
from widennet.predict import predict_vulnerability

__all__ = [
    "build_widennet",
    "predict_vulnerability",
    "__version__",
]
