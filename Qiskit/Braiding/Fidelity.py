import numpy as np
import run
from matplotlib import pyplot as plt
import Parameters

def exact_statevector(tau):

    dmin, dmax, initial_state = Parameters.d_min, Parameters.d_max, Parameters.initial_state
    def initial_statevector_and_berry_phase():
        d1, d2, d3 = dmin, dmin, dmax
        d = (d1**2 + d2**2 + d3**2)**(1/2)
        D = (d1**2 + d2**2 + d3**2 + 4) ** (1/2)

        state_even_g = np.array([0, d2 * d3 + 1j * d1 * d, -d1 ** 2 - d3 ** 2, d1 * d2 - 1j * d3 * d])
        state_even_e1 = np.array([1j * (-2 + D), d3, d2, d1])
        state_even_e2 = np.array([0, d2 * d3 - 1j * d1 * d, -d1 ** 2 - d3 ** 2, d1 * d2 + 1j * d3 * d])
        state_even_e3 = np.array([-1j * (2 + D), d3, d2, d1])

        state_odd_g = np.array([1j * d1, 1j * d2, -1j * d3, 2 + D])
        state_odd_e1 = np.array([-d1 * d2 + 1j * d3 * d, d1**2 + d3**2, d2 * d3 + 1j * d1 * d, 0])
        state_odd_e2 = np.array([-1j * d1, -1j * d2, 1j * d3, -2 + D])
        state_odd_e3 = np.array([-d1 * d2 - 1j * d3 * d, d1**2 + d3**2, d2 * d3 - 1j * d1 * d, 0])

        state_even_g = state_even_g / np.linalg.norm(state_even_g)
        state_even_e1 = state_even_e1 / np.linalg.norm(state_even_e1)
        state_even_e2 = state_even_e2 / np.linalg.norm(state_even_e2)
        state_even_e3 = state_even_e3 / np.linalg.norm(state_even_e3)

        state_odd_g = state_odd_g / np.linalg.norm(state_odd_g)
        state_odd_e1 = state_odd_e1 / np.linalg.norm(state_odd_e1)
        state_odd_e2 = state_odd_e2 / np.linalg.norm(state_odd_e2)
        state_odd_e3 = state_odd_e3 / np.linalg.norm(state_odd_e3)

        if initial_state == "even g":
            statevector = state_even_g
            berry_phase = np.pi / 2
        elif initial_state == 'even e1':
            statevector = state_even_e1
            berry_phase = 0
        elif initial_state == 'even e2':
            statevector = state_even_e2
            berry_phase = -np.pi / 2
        elif initial_state == 'even e3':
            statevector = state_even_e3
            berry_phase = 0
        elif initial_state == 'odd g':
            statevector = state_odd_g
            berry_phase = 0
        elif initial_state == 'odd e1':
            statevector = state_odd_e1
            berry_phase = np.pi / 2
        elif initial_state == 'odd e2':
            statevector = state_odd_e2
            berry_phase = 0
        elif initial_state == 'odd e3':
            statevector = state_odd_e3
            berry_phase = -np.pi / 2
        return statevector, berry_phase

    def energy(t, tau):
        if initial_state == "even g":
            energy = -1 - (dmin ** 2 + dmax ** 2 + (dmin + (dmax - dmin) * t / tau) ** 2) ** (1 / 2)
        elif initial_state == 'even e1':
            energy =  1 - (4 + dmin ** 2 + dmax ** 2 + (dmin + (dmax - dmin) * t / tau) ** 2) ** (1 / 2)
        elif initial_state == 'even e2':
            energy = -1 + (dmin ** 2 + dmax ** 2 + (dmin + (dmax - dmin) * t / tau) ** 2) ** (1 / 2)
        elif initial_state == 'even e3':
            energy = 1 + (4 + dmin ** 2 + dmax ** 2 + (dmin + (dmax - dmin) * t / tau) ** 2) ** (1 / 2)
        elif initial_state == 'odd g':
            energy = -1 - (4 + dmin ** 2 + dmax ** 2 + (dmin + (dmax - dmin) * t / tau) ** 2) ** (1 / 2)
        elif initial_state == 'odd e1':
            energy = 1 - (dmin ** 2 + dmax ** 2 + (dmin + (dmax - dmin) * t / tau) ** 2) ** (1 / 2)
        elif initial_state == 'odd e2':
            energy = -1 + (4 + dmin ** 2 + dmax ** 2 + (dmin + (dmax - dmin) * t / tau) ** 2) ** (1 / 2)
        elif initial_state == 'odd e3':
            energy = 1 + (dmin ** 2 + dmax ** 2 + (dmin + (dmax - dmin) * t / tau) ** 2) ** (1 / 2)
        return energy


    t_list = np.linspace(0, tau, 3000)
    energy_list = []
    for t in t_list:
        energy_list.append(energy(t, tau))

    initial_statevector, berry_phase = initial_statevector_and_berry_phase()
    dynamic_phase = - 6 * np.trapz(energy_list, t_list)
    total_phase = np.exp(1j * (berry_phase + dynamic_phase))
    final_state = initial_statevector * total_phase
    return final_state, total_phase



def fidelity_tau():
    """
    Generates fidelity plot by varying tau while fixing dt. N is fixed to tau * 30.
    The plot is for 6MZM system with even ground initial state.
    """

    tau_list = np.arange(0, 30, 0.2)
    statevector_list = []
    fidelity_list = []
    for i in range(len(tau_list)):
        tau = tau_list[i]
        N = int(tau * 30)
        final_state, total_phase = exact_statevector(tau)
        sim_statevector = run.run(tau, N)
        fidelity = np.vdot(sim_statevector, final_state) * np.vdot(final_state, sim_statevector)
        statevector_list.append(sim_statevector)
        fidelity_list.append(fidelity)

    plt.title("Fidelity against Period")
    plt.xlabel("Tau")
    plt.ylabel("Fidelity")
    plt.scatter(tau_list, fidelity_list)
    plt.show()

    f = open("result/Fidelity_Tau_" + str(Parameters.initial_state) + ".txt", "a")
    #plt.savefig("result/Fidelity_Tau_" + str(Parameters.initial_state) + ".png")
    f.write("dmin, dmax : " + str(Parameters.d_min) + ", " + str(Parameters.d_max) + "\n")
    f.write("Initial State: " + str(Parameters.initial_state) + "\n")
    f.write("Tau Lists: \n")
    f.write(str(tau_list) + "\n")
    f.write("Fidelity Lists: \n")
    f.write(str(fidelity_list))
    f.close()

fidelity_tau()


