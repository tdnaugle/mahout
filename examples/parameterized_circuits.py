#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import qiskit
from qiskit.circuit import QuantumCircuit, Parameter
import cirq
from braket.devices import LocalSimulator
from braket.circuits import Circuit, FreeParameter
import sympy

# pull data, setup parameters for two-qubit angle encoding example

# use first example observation of our toy dataset
x1 = 2.0734511513692637
x2 = 5.84336233567701

####
# Specify Circuits and Parameters
####
# qiskit
qk_x1_param = Parameter("x1")
qk_x2_param = Parameter("x2")
qk_qc = QuantumCircuit(2)
qk_qc.rx(qk_x1_param, 0)
qk_qc.rx(qk_x2_param, 1)

# cirq
cq_x1_param= sympy.Symbol('x1')
cq_x2_param = sympy.Symbol('x2')
q0, q1 = cirq.LineQubit.range(2)
cq_qc = cirq.Circuit(
    cirq.rx(cq_x1_param)(q0),
    cirq.rx(cq_x2_param)(q1)
)

# bra ket
bk_x1_param = FreeParameter("x1")
bk_x2_param = FreeParameter("x2")
bk_qc = Circuit()
bk_qc.rx(0, angle=bk_x1_param) # error when using sympy symbol as a parameter
bk_qc.rx(1, angle=bk_x2_param) # error when using sympy symbol as a parameter


# draw all three circuits to check sameness
print(qk_qc.draw())
print(cq_qc)
print(bk_qc)

###
# Execute Circuits
###

# qiskit
qk_qc = qk_qc.assign_parameters({qk_x1_param: x1, qk_x2_param: x2})
qk_simulator = qiskit.Aer.get_backend('statevector_simulator')
job = qiskit.execute(qk_qc, qk_simulator)
qk_result = job.result()
qk_final_state_vector = qk_result.get_statevector()

# cirq
cq_resolver = cirq.ParamResolver({cq_x1_param: x1, cq_x2_param: x2})
cq_simulator = cirq.Simulator()
cq_result = cq_simulator.simulate(cq_qc, param_resolver=cq_resolver)
cq_final_state_vector = cq_result.final_state_vector

# bra ket
bk_qc.state_vector()
bk_simulator = LocalSimulator()
bk_qc_bound = bk_qc.make_bound_circuit({"x1": x1, "x2": x2})
bk_result = bk_simulator.run(bk_qc_bound, shots=0).result()
bk_final_state_vector = bk_result.result_types[0].value


# check final state vectors for sameness
print(qk_final_state_vector)
print(cq_final_state_vector)
print(bk_final_state_vector)

