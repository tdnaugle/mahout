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
from qumat.qumat import QuMat
import numpy as np

# Example usage
backend_config = {
    'backend_name': 'qiskit',  # 'qiskit', 'cirq'
    'backend_options': {
        'simulator_type': 'statevector_simulator',
        'shots': 1024
    }
}

qumat_instance = QuMat(backend_config)

data_vector1 = [1 / np.sqrt(2), 1 / np.sqrt(2)]  # Example data vector 1
data_vector2 = [1 / np.sqrt(2), -1 / np.sqrt(2)]  # Example data vector 2

qumat_instance.create_empty_circuit(len(data_vector1))
kernel_value = qumat_instance.calculate_kernel(data_vector1, data_vector2)

print(f"Kernel value: {kernel_value}")