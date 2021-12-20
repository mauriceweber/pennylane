# Copyright 2018-2021 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This submodule contains the discrete-variable quantum operations that do
not depend on any parameters.
"""
# pylint:disable=abstract-method,arguments-differ,protected-access
import cmath
import numpy as np
from scipy.linalg import block_diag

import pennylane as qml
from pennylane.operation import AnyWires, Observable, Operation
from pennylane.utils import pauli_eigs
from pennylane.wires import Wires

INV_SQRT2 = 1 / qml.math.sqrt(2)


class Hadamard(Observable, Operation):
    r"""Hadamard(wires)
    The Hadamard operator

    .. math:: H = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1\\ 1 & -1\end{bmatrix}.

    **Details:**

    * Number of wires: 1
    * Number of parameters: 0

    Args:
        wires (Sequence[int] or int): the wire the operation acts on
    """
    num_wires = 1
    eigvals = pauli_eigs(1)
    matrix = np.array([[INV_SQRT2, INV_SQRT2], [INV_SQRT2, -INV_SQRT2]])

    @property
    def num_params(self):
        return 0

    def label(self, decimals=None, base_label=None):
        return base_label or "H"

    @classmethod
    def _matrix(cls, *params):
        return cls.matrix

    @classmethod
    def _eigvals(cls, *params):
        return cls.eigvals

    @staticmethod
    def compute_diagonalizing_gates(wires):
        r"""Diagonalizing gates of this operator.

        These gates rotate the specified wires such that they
        are in the eigenbasis of the Hadamard operator:

        .. math:: H = U^\dagger Z U

        where :math:`U = R_y(-\pi/4)`.

        Args:
            wires (Iterable): wires that the operator acts on

        Returns:
            list[.Operator]: list of diagonalizing gates

        **Example**

        >>> qml.Hadamard.compute_diagonalizing_gates(wires=[0])
        [RY(-0.7853981633974483, wires=[0])]
        """
        return [qml.RY(-np.pi / 4, wires=wires)]

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for specified wires. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.Hadamard.decomposition`.

        Args:
            wires (Any, Wires): Wire that the operator acts on.

        Returns:
            list[Operator]: decomposition of the Operator into lower level operations

        **Example:**

        >>> qml.Hadamard.compute_decomposition(0)
        [PhaseShift(1.5707963267948966, wires=[0]),
        RX(1.5707963267948966, wires=[0]),
        PhaseShift(1.5707963267948966, wires=[0])]

        """
        decomp_ops = [
            qml.PhaseShift(np.pi / 2, wires=wires),
            qml.RX(np.pi / 2, wires=wires),
            qml.PhaseShift(np.pi / 2, wires=wires),
        ]
        return decomp_ops

    def adjoint(self):
        return Hadamard(wires=self.wires)

    def single_qubit_rot_angles(self):
        # H = RZ(\pi) RY(\pi/2) RZ(0)
        return [np.pi, np.pi / 2, 0.0]


class PauliX(Observable, Operation):
    r"""PauliX(wires)
    The Pauli X operator

    .. math:: \sigma_x = \begin{bmatrix} 0 & 1 \\ 1 & 0\end{bmatrix}.

    **Details:**

    * Number of wires: 1
    * Number of parameters: 0

    Args:
        wires (Sequence[int] or int): the wire the operation acts on
    """
    num_wires = 1
    basis = "X"
    eigvals = pauli_eigs(1)
    matrix = np.array([[0, 1], [1, 0]])

    @property
    def num_params(self):
        return 0

    def label(self, decimals=None, base_label=None):
        return base_label or "X"

    @classmethod
    def _matrix(cls, *params):
        return cls.matrix

    @classmethod
    def _eigvals(cls, *params):
        return cls.eigvals

    @staticmethod
    def compute_diagonalizing_gates(wires):
        r"""Diagonalizing gates of this operator.

        These gates rotate the specified wires such that they
        are in the eigenbasis of PauliX:

        .. math:: X = H^\dagger Z H.

        Args:
           wires (Iterable): wires that the operator acts on

        Returns:
           list[.Operator]: list of diagonalizing gates

        **Example**

        >>> qml.PauliX.compute_diagonalizing_gates(wires=[0])
        [Hadamard(wires=[0])]
        """
        return [Hadamard(wires=wires)]

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for specified wire. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.PauliX.decomposition`.

        Args:
            wires (Any, Wires): Wire that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.PauliX.compute_decomposition(0)
        [PhaseShift(1.5707963267948966, wires=[0]),
        RX(3.141592653589793, wires=[0]),
        PhaseShift(1.5707963267948966, wires=[0])]

        """
        decomp_ops = [
            qml.PhaseShift(np.pi / 2, wires=wires),
            qml.RX(np.pi, wires=wires),
            qml.PhaseShift(np.pi / 2, wires=wires),
        ]
        return decomp_ops

    def adjoint(self):
        return PauliX(wires=self.wires)

    def _controlled(self, wire):
        CNOT(wires=Wires(wire) + self.wires)

    def single_qubit_rot_angles(self):
        # X = RZ(-\pi/2) RY(\pi) RZ(\pi/2)
        return [np.pi / 2, np.pi, -np.pi / 2]


class PauliY(Observable, Operation):
    r"""PauliY(wires)
    The Pauli Y operator

    .. math:: \sigma_y = \begin{bmatrix} 0 & -i \\ i & 0\end{bmatrix}.

    **Details:**

    * Number of wires: 1
    * Number of parameters: 0

    Args:
        wires (Sequence[int] or int): the wire the operation acts on
    """
    num_wires = 1
    basis = "Y"
    eigvals = pauli_eigs(1)
    matrix = np.array([[0, -1j], [1j, 0]])

    @property
    def num_params(self):
        return 0

    def label(self, decimals=None, base_label=None):
        return base_label or "Y"

    @classmethod
    def _matrix(cls, *params):
        return cls.matrix

    @classmethod
    def _eigvals(cls, *params):
        return cls.eigvals

    @staticmethod
    def compute_diagonalizing_gates(wires):
        r"""Diagonalizing gates of this operator.

        These gates rotate the specified wires such that they
        are in the eigenbasis of PauliY:

        .. math:: Y = U^\dagger Z U

        where :math:`U=HSZ`.

        Args:
            wires (Iterable): wires that the operator acts on

        Returns:
            list[.Operator]: list of diagonalizing gates

        **Example**

        >>> qml.PauliY.compute_diagonalizing_gates(wires=[0])
        [PauliZ(wires=[0]), S(wires=[0]), Hadamard(wires=[0])]
        """
        return [
            PauliZ(wires=wires),
            S(wires=wires),
            Hadamard(wires=wires),
        ]

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for specified wire. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance. 
        See also :meth:`~.PauliY.decomposition`.

        Args:
            wires (Any, Wires): Single wire that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.PauliY.compute_decomposition(0)
        [PhaseShift(1.5707963267948966, wires=[0]),
        RY(3.141592653589793, wires=[0]),
        PhaseShift(1.5707963267948966, wires=[0])]

        """
        decomp_ops = [
            qml.PhaseShift(np.pi / 2, wires=wires),
            qml.RY(np.pi, wires=wires),
            qml.PhaseShift(np.pi / 2, wires=wires),
        ]
        return decomp_ops

    def adjoint(self):
        return PauliY(wires=self.wires)

    def _controlled(self, wire):
        CY(wires=Wires(wire) + self.wires)

    def single_qubit_rot_angles(self):
        # Y = RZ(0) RY(\pi) RZ(0)
        return [0.0, np.pi, 0.0]


class PauliZ(Observable, Operation):
    r"""PauliZ(wires)
    The Pauli Z operator

    .. math:: \sigma_z = \begin{bmatrix} 1 & 0 \\ 0 & -1\end{bmatrix}.

    **Details:**

    * Number of wires: 1
    * Number of parameters: 0

    Args:
        wires (Sequence[int] or int): the wire the operation acts on
    """
    num_wires = 1
    basis = "Z"
    eigvals = pauli_eigs(1)
    matrix = np.array([[1, 0], [0, -1]])

    @property
    def num_params(self):
        return 0

    def label(self, decimals=None, base_label=None):
        return base_label or "Z"

    @classmethod
    def _matrix(cls, *params):
        return cls.matrix

    @classmethod
    def _eigvals(cls, *params):
        return cls.eigvals

    @staticmethod
    def compute_diagonalizing_gates(wires):
        """Diagonalizing gates of this operator.

        Args:
            wires (Iterable): wires that the operator acts on

        Returns:
            list[.Operator]: list of diagonalizing gates

        **Example**

        >>> qml.PauliZ.compute_diagonalizing_gates(wires=[0])
        []
        """
        return []

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for the specified wire. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.PauliZ.decomposition`.

        Args:
            wires (Any, Wires): Single wire that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.PauliZ.compute_decomposition(0)
        [PhaseShift(3.141592653589793, wires=[0])]

        """
        return [qml.PhaseShift(np.pi, wires=wires)]

    def adjoint(self):
        return PauliZ(wires=self.wires)

    def _controlled(self, wire):
        CZ(wires=Wires(wire) + self.wires)

    def single_qubit_rot_angles(self):
        # Z = RZ(\pi) RY(0) RZ(0)
        return [np.pi, 0.0, 0.0]


class S(Operation):
    r"""S(wires)
    The single-qubit phase gate

    .. math:: S = \begin{bmatrix}
                1 & 0 \\
                0 & i
            \end{bmatrix}.

    **Details:**

    * Number of wires: 1
    * Number of parameters: 0

    Args:
        wires (Sequence[int] or int): the wire the operation acts on
    """
    num_wires = 1
    basis = "Z"
    op_eigvals = np.array([1, 1j])
    op_matrix = np.array([[1, 0], [0, 1j]])

    @property
    def num_params(self):
        return 0

    @classmethod
    def _matrix(cls, *params):
        return cls.op_matrix

    @classmethod
    def _eigvals(cls, *params):
        return cls.op_eigvals

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for the specified wire. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.S.decomposition`.

        Args:
            wires (Any, Wires): Single wire that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.S.compute_decomposition(0)
        [PhaseShift(1.5707963267948966, wires=[0])]

        """
        return [qml.PhaseShift(np.pi / 2, wires=wires)]

    def adjoint(self):
        return S(wires=self.wires).inv()

    def single_qubit_rot_angles(self):
        # S = RZ(\pi/2) RY(0) RZ(0)
        return [np.pi / 2, 0.0, 0.0]


class T(Operation):
    r"""T(wires)
    The single-qubit T gate

    .. math:: T = \begin{bmatrix}
                1 & 0 \\
                0 & e^{\frac{i\pi}{4}}
            \end{bmatrix}.

    **Details:**

    * Number of wires: 1
    * Number of parameters: 0

    Args:
        wires (Sequence[int] or int): the wire the operation acts on
    """
    num_wires = 1
    basis = "Z"
    op_matrix = np.array([[1, 0], [0, cmath.exp(1j * np.pi / 4)]])
    op_eigvals = np.array([1, cmath.exp(1j * np.pi / 4)])

    @property
    def num_params(self):
        return 0

    @classmethod
    def _matrix(cls, *params):
        return cls.op_matrix

    @classmethod
    def _eigvals(cls, *params):
        return cls.op_eigvals

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for the specified wire. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.T.decomposition`.

        Args:
            wires (Any, Wires): Single wire that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.T.compute_decomposition(0)
        [PhaseShift(0.7853981633974483, wires=[0])]

        """
        return [qml.PhaseShift(np.pi / 4, wires=wires)]

    def adjoint(self):
        return T(wires=self.wires).inv()

    def single_qubit_rot_angles(self):
        # T = RZ(\pi/4) RY(0) RZ(0)
        return [np.pi / 4, 0.0, 0.0]


class SX(Operation):
    r"""SX(wires)
    The single-qubit Square-Root X operator.

    .. math:: SX = \sqrt{X} = \frac{1}{2} \begin{bmatrix}
            1+i &   1-i \\
            1-i &   1+i \\
        \end{bmatrix}.

    **Details:**

    * Number of wires: 1
    * Number of parameters: 0

    Args:
        wires (Sequence[int] or int): the wire the operation acts on
    """
    num_wires = 1
    basis = "X"
    op_matrix = 0.5 * np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]])
    op_eigvals = np.array([1, 1j])

    @property
    def num_params(self):
        return 0

    @classmethod
    def _matrix(cls, *params):
        return cls.op_matrix

    @classmethod
    def _eigvals(cls, *params):
        return cls.op_eigvals

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for the specified wire. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.SX.decomposition`.

        Args:
            wires (Any, Wires): Single wire that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.SX.compute_decomposition(0)
        [RZ(1.5707963267948966, wires=[0]),
        RY(1.5707963267948966, wires=[0]),
        RZ(-3.141592653589793, wires=[0]),
        PhaseShift(1.5707963267948966, wires=[0])]

        """
        decomp_ops = [
            qml.RZ(np.pi / 2, wires=wires),
            qml.RY(np.pi / 2, wires=wires),
            qml.RZ(-np.pi, wires=wires),
            qml.PhaseShift(np.pi / 2, wires=wires),
        ]
        return decomp_ops

    def adjoint(self):
        return SX(wires=self.wires).inv()

    def single_qubit_rot_angles(self):
        # SX = RZ(-\pi/2) RY(\pi/2) RZ(\pi/2)
        return [np.pi / 2, np.pi / 2, -np.pi / 2]


class CNOT(Operation):
    r"""CNOT(wires)
    The controlled-NOT operator

    .. math:: CNOT = \begin{bmatrix}
            1 & 0 & 0 & 0 \\
            0 & 1 & 0 & 0\\
            0 & 0 & 0 & 1\\
            0 & 0 & 1 & 0
        \end{bmatrix}.

    .. note:: The first wire provided corresponds to the **control qubit**.

    **Details:**

    * Number of wires: 2
    * Number of parameters: 0

    Args:
        wires (Sequence[int]): the wires the operation acts on
    """
    num_wires = 2
    basis = "X"
    matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

    @property
    def num_params(self):
        return 0

    def label(self, decimals=None, base_label=None):
        return base_label or "⊕"

    @classmethod
    def _matrix(cls, *params):
        return CNOT.matrix

    def adjoint(self):
        return CNOT(wires=self.wires)

    def _controlled(self, wire):
        Toffoli(wires=Wires(wire) + self.wires)

    @property
    def control_wires(self):
        return Wires(self.wires[0])


class CZ(Operation):
    r"""CZ(wires)
    The controlled-Z operator

    .. math:: CZ = \begin{bmatrix}
            1 & 0 & 0 & 0 \\
            0 & 1 & 0 & 0\\
            0 & 0 & 1 & 0\\
            0 & 0 & 0 & -1
        \end{bmatrix}.

    .. note:: The first wire provided corresponds to the **control qubit**.

    **Details:**

    * Number of wires: 2
    * Number of parameters: 0

    Args:
        wires (Sequence[int]): the wires the operation acts on
    """
    num_wires = 2
    basis = "Z"
    eigvals = np.array([1, 1, 1, -1])
    matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])

    @property
    def num_params(self):
        return 0

    def label(self, decimals=None, base_label=None):
        return base_label or "Z"

    @classmethod
    def _matrix(cls, *params):
        return cls.matrix

    @classmethod
    def _eigvals(cls, *params):
        return cls.eigvals

    def adjoint(self):
        return CZ(wires=self.wires)

    @property
    def control_wires(self):
        return Wires(self.wires[0])


class CY(Operation):
    r"""CY(wires)
    The controlled-Y operator

    .. math:: CY = \begin{bmatrix}
            1 & 0 & 0 & 0 \\
            0 & 1 & 0 & 0\\
            0 & 0 & 0 & -i\\
            0 & 0 & i & 0
        \end{bmatrix}.

    .. note:: The first wire provided corresponds to the **control qubit**.

    **Details:**

    * Number of wires: 2
    * Number of parameters: 0

    Args:
        wires (Sequence[int]): the wires the operation acts on
    """
    num_wires = 2
    basis = "Y"
    matrix = np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, -1j],
            [0, 0, 1j, 0],
        ]
    )

    @property
    def num_params(self):
        return 0

    def label(self, decimals=None, base_label=None):
        return base_label or "Y"

    @classmethod
    def _matrix(cls, *params):
        return cls.matrix

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for the specified wires. The decomposition defines an Operator 
        as a product of more fundamental gates:


        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.CY.decomposition`.

        Args:
            wires (Iterable, Wires): Wires that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.CY.compute_decomposition(0)
        [CRY(3.141592653589793, wires=[0, 1]), S(wires=[0])]

        """
        return [qml.CRY(np.pi, wires=wires), S(wires=wires[0])]

    def adjoint(self):
        return CY(wires=self.wires)

    @property
    def control_wires(self):
        return Wires(self.wires[0])


class SWAP(Operation):
    r"""SWAP(wires)
    The swap operator

    .. math:: SWAP = \begin{bmatrix}
            1 & 0 & 0 & 0 \\
            0 & 0 & 1 & 0\\
            0 & 1 & 0 & 0\\
            0 & 0 & 0 & 1
        \end{bmatrix}.

    **Details:**

    * Number of wires: 2
    * Number of parameters: 0

    Args:
        wires (Sequence[int]): the wires the operation acts on
    """
    num_wires = 2
    basis = "X"
    matrix = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])

    @property
    def num_params(self):
        return 0

    @classmethod
    def _matrix(cls, *params):
        return cls.matrix

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for the specified wires. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.SWAP.decomposition`.

        Args:
            wires (Iterable, Wires): Wires that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.SWAP.compute_decomposition((0,1))
        [CNOT(wires=[0, 1]), CNOT(wires=[1, 0]), CNOT(wires=[0, 1])]

        """
        decomp_ops = [
            qml.CNOT(wires=[wires[0], wires[1]]),
            qml.CNOT(wires=[wires[1], wires[0]]),
            qml.CNOT(wires=[wires[0], wires[1]]),
        ]
        return decomp_ops

    def adjoint(self):
        return SWAP(wires=self.wires)

    def _controlled(self, wire):
        CSWAP(wires=wire + self.wires)


class ISWAP(Operation):
    r"""ISWAP(wires)
    The i-swap operator

    .. math:: ISWAP = \begin{bmatrix}
            1 & 0 & 0 & 0 \\
            0 & 0 & i & 0\\
            0 & i & 0 & 0\\
            0 & 0 & 0 & 1
        \end{bmatrix}.

    **Details:**

    * Number of wires: 2
    * Number of parameters: 0

    Args:
        wires (Sequence[int]): the wires the operation acts on
    """
    num_wires = 2
    op_matrix = np.array([[1, 0, 0, 0], [0, 0, 1j, 0], [0, 1j, 0, 0], [0, 0, 0, 1]])
    op_eigvals = np.array([1j, -1j, 1, 1])

    @property
    def num_params(self):
        return 0

    @classmethod
    def _matrix(cls, *params):
        return cls.op_matrix

    @classmethod
    def _eigvals(cls, *params):
        return cls.op_eigvals

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for the specified wires. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.ISWAP.decomposition`.

        Args:
            wires (Iterable, Wires): Wires that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.ISWAP.compute_decomposition((0,1))
        [S(wires=[0]),
        S(wires=[1]),
        Hadamard(wires=[0]),
        CNOT(wires=[0, 1]),
        CNOT(wires=[1, 0]),
        Hadamard(wires=[1])]

        """
        decomp_ops = [
            S(wires=wires[0]),
            S(wires=wires[1]),
            Hadamard(wires=wires[0]),
            CNOT(wires=[wires[0], wires[1]]),
            CNOT(wires=[wires[1], wires[0]]),
            Hadamard(wires=wires[1]),
        ]
        return decomp_ops

    def adjoint(self):
        return ISWAP(wires=self.wires).inv()


class SISWAP(Operation):
    r"""SISWAP(wires)
    The square root of i-swap operator. Can also be accessed as ``qml.SQISW``

    .. math:: SISWAP = \begin{bmatrix}
            1 & 0 & 0 & 0 \\
            0 & 1/ \sqrt{2} & i/\sqrt{2} & 0\\
            0 & i/ \sqrt{2} & 1/ \sqrt{2} & 0\\
            0 & 0 & 0 & 1
        \end{bmatrix}.

    **Details:**

    * Number of wires: 2
    * Number of parameters: 0

    Args:
        wires (Sequence[int]): the wires the operation acts on
    """
    num_wires = 2
    op_matrix = np.array(
        [
            [1, 0, 0, 0],
            [0, INV_SQRT2, INV_SQRT2 * 1j, 0],
            [0, INV_SQRT2 * 1j, INV_SQRT2, 0],
            [0, 0, 0, 1],
        ]
    )
    op_eigvals = np.array([INV_SQRT2 * (1 + 1j), INV_SQRT2 * (1 - 1j), 1, 1])

    @property
    def num_params(self):
        return 0

    @classmethod
    def _matrix(cls, *params):
        return cls.op_matrix

    @classmethod
    def _eigvals(cls, *params):
        return cls.op_eigvals

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for the specified wires. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.SISWAP.decomposition`.

        Args:
            wires (Iterable, Wires): Wires that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.SISWAP.compute_decomposition((0,1))
        [SX(wires=[0]),
        RZ(1.5707963267948966, wires=[0]),
        CNOT(wires=[0, 1]),
        SX(wires=[0]),
        RZ(5.497787143782138, wires=[0]),
        SX(wires=[0]),
        RZ(1.5707963267948966, wires=[0]),
        SX(wires=[1]),
        RZ(5.497787143782138, wires=[1]),
        CNOT(wires=[0, 1]),
        SX(wires=[0]),
        SX(wires=[1])]

        """
        decomp_ops = [
            SX(wires=wires[0]),
            qml.RZ(np.pi / 2, wires=wires[0]),
            CNOT(wires=[wires[0], wires[1]]),
            SX(wires=wires[0]),
            qml.RZ(7 * np.pi / 4, wires=wires[0]),
            SX(wires=wires[0]),
            qml.RZ(np.pi / 2, wires=wires[0]),
            SX(wires=wires[1]),
            qml.RZ(7 * np.pi / 4, wires=wires[1]),
            CNOT(wires=[wires[0], wires[1]]),
            SX(wires=wires[0]),
            SX(wires=wires[1]),
        ]
        return decomp_ops

    def adjoint(self):
        return SISWAP(wires=self.wires).inv()


SQISW = SISWAP


class CSWAP(Operation):
    r"""CSWAP(wires)
    The controlled-swap operator

    .. math:: CSWAP = \begin{bmatrix}
            1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
            0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\
            0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\
            0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\
            0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\
            0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\
            0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\
            0 & 0 & 0 & 0 & 0 & 0 & 0 & 1
        \end{bmatrix}.

    .. note:: The first wire provided corresponds to the **control qubit**.

    **Details:**

    * Number of wires: 3
    * Number of parameters: 0

    Args:
        wires (Sequence[int]): the wires the operation acts on
    """
    is_self_inverse = True
    num_wires = 3
    matrix = np.array(
        [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
        ]
    )

    @property
    def num_params(self):
        return 0

    def label(self, decimals=None, base_label=None):
        return base_label or "SWAP"

    @classmethod
    def _matrix(cls, *params):
        return cls.matrix

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for the specified wires. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.CSWAP.decomposition`.

        Args:
            wires (Iterable, Wires): Wires that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.CSWAP.compute_decomposition((0,1,2))
        [Toffoli(wires=[0, 2, 1]), Toffoli(wires=[0, 1, 2]), Toffoli(wires=[0, 2, 1])]

        """
        decomp_ops = [
            qml.Toffoli(wires=[wires[0], wires[2], wires[1]]),
            qml.Toffoli(wires=[wires[0], wires[1], wires[2]]),
            qml.Toffoli(wires=[wires[0], wires[2], wires[1]]),
        ]
        return decomp_ops

    def adjoint(self):
        return CSWAP(wires=self.wires)

    @property
    def control_wires(self):
        return Wires(self.wires[0])


class Toffoli(Operation):
    r"""Toffoli(wires)
    Toffoli (controlled-controlled-X) gate.

    .. math::

        Toffoli =
        \begin{pmatrix}
        1 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
        0 & 1 & 0 & 0 & 0 & 0 & 0 & 0\\
        0 & 0 & 1 & 0 & 0 & 0 & 0 & 0\\
        0 & 0 & 0 & 1 & 0 & 0 & 0 & 0\\
        0 & 0 & 0 & 0 & 1 & 0 & 0 & 0\\
        0 & 0 & 0 & 0 & 0 & 1 & 0 & 0\\
        0 & 0 & 0 & 0 & 0 & 0 & 0 & 1\\
        0 & 0 & 0 & 0 & 0 & 0 & 1 & 0
        \end{pmatrix}

    **Details:**

    * Number of wires: 3
    * Number of parameters: 0

    Args:
        wires (Sequence[int]): the subsystem the gate acts on
    """
    num_wires = 3
    basis = "X"
    matrix = np.array(
        [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0],
        ]
    )

    @property
    def num_params(self):
        return 0

    def label(self, decimals=None, base_label=None):
        return base_label or "⊕"

    @classmethod
    def _matrix(cls, *params):
        return cls.matrix

    @staticmethod
    def compute_decomposition(wires):
        """Compute the decomposition for the specified wires. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.Toffoli.decomposition`.

        Args:
            wires (Iterable, Wires): Wires that the operator acts on.

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.Toffoli.compute_decomposition((0,1,2))
        [Hadamard(wires=[2]),
        CNOT(wires=[1, 2]),
        T.inv(wires=[2]),
        CNOT(wires=[0, 2]),
        T(wires=[2]),
        CNOT(wires=[1, 2]),
        T.inv(wires=[2]),
        CNOT(wires=[0, 2]),
        T(wires=[2]),
        T(wires=[1]),
        CNOT(wires=[0, 1]),
        Hadamard(wires=[2]),
        T(wires=[0]),
        T.inv(wires=[1]),
        CNOT(wires=[0, 1])]

        """
        decomp_ops = [
            Hadamard(wires=wires[2]),
            CNOT(wires=[wires[1], wires[2]]),
            T(wires=wires[2]).inv(),
            CNOT(wires=[wires[0], wires[2]]),
            T(wires=wires[2]),
            CNOT(wires=[wires[1], wires[2]]),
            T(wires=wires[2]).inv(),
            CNOT(wires=[wires[0], wires[2]]),
            T(wires=wires[2]),
            T(wires=wires[1]),
            CNOT(wires=[wires[0], wires[1]]),
            Hadamard(wires=wires[2]),
            T(wires=wires[0]),
            T(wires=wires[1]).inv(),
            CNOT(wires=[wires[0], wires[1]]),
        ]
        return decomp_ops

    def adjoint(self):
        return Toffoli(wires=self.wires)

    @property
    def control_wires(self):
        return Wires(self.wires[:2])


class MultiControlledX(Operation):
    r"""MultiControlledX(control_wires, wires, control_values)
    Apply a Pauli X gate controlled on an arbitrary computational basis state.

    **Details:**

    * Number of wires: Any (the operation can act on any number of wires)
    * Number of parameters: 0
    * Gradient recipe: None

    Args:
        control_wires (Union[Wires, Sequence[int], or int]): the control wire(s)
        wires (Union[Wires or int]): a single target wire the operation acts on
        control_values (str): a string of bits representing the state of the control
            wires to control on (default is the all 1s state)
        work_wires (Union[Wires, Sequence[int], or int]): optional work wires used to decompose
            the operation into a series of Toffoli gates

    .. note::

        If ``MultiControlledX`` is not supported on the targeted device, PennyLane will decompose
        the operation into :class:`~.Toffoli` and/or :class:`~.CNOT` gates. When controlling on
        three or more wires, the Toffoli-based decompositions described in Lemmas 7.2 and 7.3 of
        `Barenco et al. <https://arxiv.org/abs/quant-ph/9503016>`__ will be used. These methods
        require at least one work wire.

        The number of work wires provided determines the decomposition method used and the resulting
        number of Toffoli gates required. When ``MultiControlledX`` is controlling on :math:`n`
        wires:

        #. If at least :math:`n - 2` work wires are provided, the decomposition in Lemma 7.2 will be
           applied using the first :math:`n - 2` work wires.
        #. If fewer than :math:`n - 2` work wires are provided, a combination of Lemmas 7.3 and 7.2
           will be applied using only the first work wire.

        These methods present a tradeoff between qubit number and depth. The method in point 1
        requires fewer Toffoli gates but a greater number of qubits.

        Note that the state of the work wires before and after the decomposition takes place is
        unchanged.

    **Example**

    The ``MultiControlledX`` operation (sometimes called a mixed-polarity
    multi-controlled Toffoli) is a commonly-encountered case of the
    :class:`~.pennylane.ControlledQubitUnitary` operation wherein the applied
    unitary is the Pauli X (NOT) gate. It can be used in the same manner as
    ``ControlledQubitUnitary``, but there is no need to specify a matrix
    argument:

    >>> qml.MultiControlledX(control_wires=[0, 1, 2, 3], wires=4, control_values='1110')

    """
    is_self_inverse = True
    num_wires = AnyWires
    grad_method = None

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        *params,
        control_wires=None,
        wires=None,
        control_values=None,
        work_wires=None,
        do_queue=True,
    ):
        wires = Wires(wires)
        control_wires = Wires(control_wires)
        work_wires = Wires([]) if work_wires is None else Wires(work_wires)

        if len(wires) != 1:
            raise ValueError("MultiControlledX accepts a single target wire.")

        if Wires.shared_wires([wires, work_wires]) or Wires.shared_wires(
            [control_wires, work_wires]
        ):
            raise ValueError("The work wires must be different from the control and target wires")

        self._target_wire = wires[0]
        self._work_wires = work_wires
        self._control_wires = control_wires

        wires = control_wires + wires

        if not control_values:
            control_values = "1" * len(control_wires)

        control_int = self._parse_control_values(control_wires, control_values)
        self.control_values = control_values

        self._padding_left = control_int * 2
        self._padding_right = 2 ** len(wires) - 2 - self._padding_left
        self._CX = None

        self.hyperparameters["work_wires"] = self._work_wires
        self.hyperparameters["control_values"] = self.control_values

        super().__init__(*params, wires=wires, do_queue=do_queue)

    @property
    def num_params(self):
        return 0

    def _matrix(self, *params):
        if self._CX is None:
            self._CX = block_diag(
                np.eye(self._padding_left), PauliX.matrix, np.eye(self._padding_right)
            )

        return self._CX

    @property
    def control_wires(self):
        return self._control_wires

    def label(self, decimals=None, base_label=None):
        return base_label or "⊕"

    @staticmethod
    def _parse_control_values(control_wires, control_values):
        """Ensure any user-specified control strings have the right format."""
        if isinstance(control_values, str):
            if len(control_values) != len(control_wires):
                raise ValueError("Length of control bit string must equal number of control wires.")

            # Make sure all values are either 0 or 1
            if any(x not in ["0", "1"] for x in control_values):
                raise ValueError("String of control values can contain only '0' or '1'.")

            control_int = int(control_values, 2)
        else:
            raise ValueError("Alternative control values must be passed as a binary string.")

        return control_int

    def adjoint(self):
        return MultiControlledX(
            control_wires=self.wires[:-1],
            wires=self.wires[-1],
            control_values=self.control_values,
            work_wires=self._work_wires,
        )

    @staticmethod
    def compute_decomposition(
        wires=None,
        work_wires=None,
        control_values=None,
    ):
        """Compute the decomposition for the specified wires. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.MultiControlledX.decomposition`.

        Args:
            wires (Iterable, Wires): Wires that the operator acts on. Should contain both control wires
                and target wire. Target wire is the last wire in the Iterable.
            work_wires (Wires): optional work wires used to decompose
                the operation into a series of Toffoli gates.
            control_values (str): a string of bits representing the state of the control
                wires to control on (default is the all 1s state)

        Returns:
            list[Operator]: decomposition into lower level operations

        **Example:**

        >>> qml.MultiControlledX.compute_decomposition(wires=[0,1,2,3],control_values="111", work_wires=qml.wires.Wires("aux"))
        [Toffoli(wires=[2, 'aux', 3]),
        Toffoli(wires=[0, 1, 'aux']),
        Toffoli(wires=[2, 'aux', 3]),
        Toffoli(wires=[0, 1, 'aux'])]

        """

        target_wire = wires[~0]
        control_wires = wires[:~0]

        if len(control_wires) > 2 and len(work_wires) == 0:
            raise ValueError(
                f"At least one work wire is required to decompose operation: MultiControlledX"
            )

        flips1 = [
            qml.PauliX(control_wires[i]) for i, val in enumerate(control_values) if val == "0"
        ]

        if len(control_wires) == 1:
            decomp = [qml.CNOT(wires=[control_wires[0], target_wire])]
        elif len(control_wires) == 2:
            decomp = [qml.Toffoli(wires=[*control_wires, target_wire])]
        else:
            num_work_wires_needed = len(control_wires) - 2

            if len(work_wires) >= num_work_wires_needed:
                decomp = MultiControlledX._decomposition_with_many_workers(
                    control_wires, target_wire, work_wires
                )
            else:
                work_wire = work_wires[0]
                decomp = MultiControlledX._decomposition_with_one_worker(
                    control_wires, target_wire, work_wire
                )

        flips2 = [
            qml.PauliX(control_wires[i]) for i, val in enumerate(control_values) if val == "0"
        ]

        return flips1 + decomp + flips2

    @staticmethod
    def _decomposition_with_many_workers(control_wires, target_wire, work_wires):
        """Decomposes the multi-controlled PauliX gate using the approach in Lemma 7.2 of
        https://arxiv.org/pdf/quant-ph/9503016.pdf, which requires a suitably large register of
        work wires"""
        num_work_wires_needed = len(control_wires) - 2
        work_wires = work_wires[:num_work_wires_needed]

        work_wires_reversed = list(reversed(work_wires))
        control_wires_reversed = list(reversed(control_wires))

        gates = []

        for i in range(len(work_wires)):
            ctrl1 = control_wires_reversed[i]
            ctrl2 = work_wires_reversed[i]
            t = target_wire if i == 0 else work_wires_reversed[i - 1]
            gates.append(qml.Toffoli(wires=[ctrl1, ctrl2, t]))

        gates.append(qml.Toffoli(wires=[*control_wires[:2], work_wires[0]]))

        for i in reversed(range(len(work_wires))):
            ctrl1 = control_wires_reversed[i]
            ctrl2 = work_wires_reversed[i]
            t = target_wire if i == 0 else work_wires_reversed[i - 1]
            gates.append(qml.Toffoli(wires=[ctrl1, ctrl2, t]))

        for i in range(len(work_wires) - 1):
            ctrl1 = control_wires_reversed[i + 1]
            ctrl2 = work_wires_reversed[i + 1]
            t = work_wires_reversed[i]
            gates.append(qml.Toffoli(wires=[ctrl1, ctrl2, t]))

        gates.append(qml.Toffoli(wires=[*control_wires[:2], work_wires[0]]))

        for i in reversed(range(len(work_wires) - 1)):
            ctrl1 = control_wires_reversed[i + 1]
            ctrl2 = work_wires_reversed[i + 1]
            t = work_wires_reversed[i]
            gates.append(qml.Toffoli(wires=[ctrl1, ctrl2, t]))

        return gates

    @staticmethod
    def _decomposition_with_one_worker(control_wires, target_wire, work_wire):
        """Decomposes the multi-controlled PauliX gate using the approach in Lemma 7.3 of
        https://arxiv.org/pdf/quant-ph/9503016.pdf, which requires a single work wire"""
        tot_wires = len(control_wires) + 2
        partition = int(np.ceil(tot_wires / 2))

        first_part = control_wires[:partition]
        second_part = control_wires[partition:]

        gates = [
            MultiControlledX(
                control_wires=first_part,
                wires=work_wire,
                work_wires=second_part + target_wire,
            ),
            MultiControlledX(
                control_wires=second_part + work_wire,
                wires=target_wire,
                work_wires=first_part,
            ),
            MultiControlledX(
                control_wires=first_part,
                wires=work_wire,
                work_wires=second_part + target_wire,
            ),
            MultiControlledX(
                control_wires=second_part + work_wire,
                wires=target_wire,
                work_wires=first_part,
            ),
        ]

        return gates


class Barrier(Operation):
    r"""Barrier(wires)
    The Barrier operator, used to separate the compilation process into blocks or as a visual tool.

    **Details:**

    * Number of wires: AnyWires
    * Number of parameters: 0

    Args:
        only_visual (bool): True if we do not want it to have an impact on the compilation process. Default is False.
        wires (Sequence[int] or int): the wires the operation acts on
    """
    num_params = 0
    num_wires = AnyWires
    par_domain = None

    def __init__(self, only_visual=False, wires=Wires([]), do_queue=True, id=None):
        self.only_visual = only_visual
        self.hyperparameters["only_visual"] = only_visual
        super().__init__(wires=wires, do_queue=do_queue, id=id)

    @staticmethod
    def compute_decomposition(wires, only_visual=False):
        """Compute the decomposition for the specified wires. The decomposition defines an Operator 
        as a product of more fundamental gates:

        .. math:: O = O_1 O_2 \dots O_n.

        ``compute_decomposition`` is a static method and can provide the decomposition of a given
        operator without creating a specific instance.
        See also :meth:`~.Barrier.decomposition`.

        ``Barrier`` decomposes into an empty list for all arguments.

        Args:
            wires (Iterable, Wires): Wires that the operator acts on.
            only_visual (Bool): True if we do not want it to have an impact on the compilation process. Default is False.

        Returns:
            list: decomposition of the Operator into lower level operations

        **Example:**

        >>> qml.Barrier.compute_decomposition(0)
        []

        """
        return []

    def label(self, decimals=None):
        return "||"
