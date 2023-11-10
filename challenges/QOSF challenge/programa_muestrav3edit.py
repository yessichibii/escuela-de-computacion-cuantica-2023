import qiskit
from qiskit import QuantumCircuit,execute,Aer,transpile,BasicAer
from qiskit.circuit.library import SwapGate,QFT,CZGate,SGate,TGate,GroverOperator
from qiskit.algorithms import Grover
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
import math

def inicializador(circuit,total_qubits):
    circuit.x(0)
    circuit.x(3)
    circuit.h(4)
    circuit.h(5)
    circuit.h(7)
    circuit.h(8)
    return circuit

#comprobar que el sumador funciona
def inicializador2(circuit,total_qubits): 
    circuit.x(4)
    circuit.x(5)
    circuit.x(7)
    return circuit

def contadorqubits(circuit,total_qubits):
    qubits=total_qubits
    bits=total_qubits-1
    contador=QuantumCircuit(qubits,bits)

    #inicializador de qft
    completo=QuantumCircuit(12,12)
    completoprueba=QuantumCircuit(12,12)
    qft=QFT(3)
    invqft=QFT(3,0,True,True)
    completo_1=completo.compose(circuit)
    completo_2=completo_1.compose(qft,qubits=[9,10,11])
    ctgate = TGate().control(1)
    #inversion de qft
    completo_2.append(ctgate, [4, 9])
    completo_2.cs(4,10)
    completo_2.cz(4,11)
    
    completo_2.barrier()
    completo_2.append(ctgate, [5, 9])
    completo_2.cs(5,10)
    completo_2.cz(5,11)

    completo_2.barrier()
    completo_2.append(ctgate, [7, 9])
    completo_2.cs(7,10)
    completo_2.cz(7,11)

    completo_2.barrier()
    completo_2.append(ctgate, [8, 9])
    completo_2.cs(8,10)
    completo_2.cz(8,11)
    
    completo_3=completo_2.compose(invqft,qubits=[9,10,11])
    completo_3.barrier()
    return completo_3

#coloca las todos los estados que tengo suma de 2
def prob2(circuit):
    completo=QuantumCircuit(14,14)
    completo_1=completo.compose(circuit)
    completo_1.x(11)
    completo_1.x(9)
    completo_1.ccx(9,10,12)
    completo_1.ccx(11,12,13)
    completo_1.z(13) # recordatorio z
    completo_1.h(13)
    
    return completo_1

# crea a grover 
def instalargrover(circuit):
    completo=QuantumCircuit(17,17)
    completo_1=completo.compose(circuit)
    #revertir compuerta
    completo_1.barrier()
    completo_1.ccx(9,10,12)
    completo_1.h(range(4,6))
    completo_1.h(range(7,9))
    completo_1.x(range(4,6))
    completo_1.x(range(7,9))
    completo_1.barrier()

    completo_1.h(13)
    completo_1.x(13)
    completo_1.barrier()
    completo_1.ccx(4,5,15)
    completo_1.ccx(7,8,14)
    completo_1.ccx(15,14,13)
    completo_1.barrier()
    completo_1.x(13)
    completo_1.z(13)
    completo_1.x(13)
    completo_1.barrier()
    completo_1.ccx(4,5,15)
    completo_1.ccx(7,8,14)
    completo_1.ccx(15,14,13)

    completo_1.barrier()
    completo_1.x(range(4,6))
    completo_1.x(range(7,9))
    completo_1.h(range(4,6))
    completo_1.h(range(7,9))
    completo_1.x(13)
    completo_1.h(13)

    return completo_1

#la condicion que acepta solo a las dos casos 1100 y 1001 ambos casos tiene 1 en a y 0 en c
def ganador(circuit):
    completo=QuantumCircuit(17,17)
    completo_1=completo.compose(circuit)
    completo_1.x(7)
    completo_1.h(13)
    completo_1.z(13)
    completo_1.x(13)
    completo_1.ccx(4,7,13)
    
    completo_1.z(13)
    
    return completo_1 

#crea las medicione qubtis con cbit
def medicion(circuit,inicio,fin,total_qubits=-1):
    if total_qubits!=-1:
        for i in range(total_qubits):
            circuit.measure(i,i)
    else:
        for i in range(inicio,fin+1):
            circuit.measure(i,i)
    return circuit

#crea una barrera 
def separador(circuit):
    circuit.barrier()
    return circuit

#imprime el circuito
def impresion_circuito(circuit):
    print(circuit)

def main():
    #inicializacion de parametros para qiskit 
    bits=qubits=9
    simulacion=Aer.get_backend('qasm_simulator') #crear una instancia de simulacion
    simulacion2=BasicAer.get_backend('statevector_simulator')
    circuit=QuantumCircuit(qubits,bits)         #Crear un circuito con 9 qubits para el primer parametro y 9 bits para el segundo parametro
    circuit=inicializador(circuit,total_qubits=qubits)
    
    circuit=separador(circuit)
    circuit_1=contadorqubits(circuit,3)
    circuit2=prob2(circuit_1)            # identifica los arreglos que sus bits sumen 2
    circuit3=instalargrover(circuit2)    #crea grover de  4 para los estados de supeporsicion
    circuit3.barrier()
    
    

    circuit3=ganador(circuit3)   #busca solo las dos ultimas opciones 1100 y 1001
    circuit3.barrier()

    circuit3=instalargrover(circuit3) #aplifica las dos opciones de arriba
    circuit3.barrier()

    circuit3=medicion(circuit3,4,8)

    impresion_circuito(circuit3)
    job=execute(circuit3,simulacion,shot=1000)
    #job2=execute(circuit3,simulacion2)
    result=job.result()
    #result2=job2.result()
    #vector=result2.get_statevector(circuit3)
    #print(vector)
    counts=result.get_counts(circuit3)
    print(counts)
    #plot_histogram(counts,sort='value_desc')


    return 0

if __name__=='__main__':
    main()