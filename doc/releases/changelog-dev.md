:orphan:

# Release 0.24.0-dev (development release)

<h3>New features since last release</h3>

* Speed up measuring of commuting Pauli operators
  [(#2425)](https://github.com/PennyLaneAI/pennylane/pull/2425)

  The code that checks for qubit wise commuting (QWC) got a performance boost that is noticable
  when many commuting paulis of the same type are measured.

<h3>Improvements</h3>

* The `gradients` module now uses faster subroutines and uniform
  formats of gradient rules.
  [(#2452)](https://github.com/XanaduAI/pennylane/pull/2452)

* Wires can be passed as the final argument to an `Operator`, instead of requiring
  the wires to be explicitly specified with keyword `wires`. This functionality already
  existed for `Observable`'s, but now extends to all `Operator`'s.
  [(#2432)](https://github.com/PennyLaneAI/pennylane/pull/2432)

  ```pycon
  >>> qml.S(0)
  S(wires=[0])
  >>> qml.CNOT((0,1))
  CNOT(wires=[0, 1])
  ```
  
* Instead of checking types, objects are processed in `QuantumTape`'s based on a new `_queue_category` property.
  This is a temporary fix that will disappear in the future. 
  [(#2408)](https://github.com/PennyLaneAI/pennylane/pull/2408)

* The `qml.taper` function can now be used to consistently taper any additional observables such as dipole moment,
  particle number, and spin operators using the symmetries obtained from the Hamiltonian.
  [(#2510)](https://github.com/PennyLaneAI/pennylane/pull/2510)
  
<h3>Breaking changes</h3>

* The properties `eigval` and `matrix` from the `Operator` class were replaced with the 
  methods `eigval()` and `matrix(wire_order=None)`.
  [(#2498)](https://github.com/PennyLaneAI/pennylane/pull/2498)
  
* `Operator.decomposition()` is now an instance method, and no longer accepts parameters.
  [(#2498)](https://github.com/PennyLaneAI/pennylane/pull/2498)

<h3>Bug fixes</h3>

* Fixed a bug where `QNGOptimizer` did not work with operators
  whose generator was a Hamiltonian.
  [(#2524)](https://github.com/PennyLaneAI/pennylane/pull/2524)


<h3>Deprecations</h3>

<h3>Bug fixes</h3>

* Fixes a bug in `DiagonalQubitUnitary._controlled` where an invalid operation was queued
  instead of the controlled version of the diagonal unitary.
  [(#2525)](https://github.com/PennyLaneAI/pennylane/pull/2525)

<h3>Documentation</h3>

* The centralized [Xanadu Sphinx Theme](https://github.com/XanaduAI/xanadu-sphinx-theme)
  is now used to style the Sphinx documentation.
  [(#2450)](https://github.com/PennyLaneAI/pennylane/pull/2450)

<h3>Contributors</h3>

This release contains contributions from (in alphabetical order):

Guillermo Alonso-Linaje, Mikhail Andrenkov, Utkarsh Azad, Christian Gogolin, Christina Lee, Maria Schuld
