import sys, math
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../../model')))
from coldplate_model import ColdPlate, Fluid, PG25, K_CU, K_AL
WEG65 = Fluid("WEG 50/50 @ 65C", 1045.0, 3550.0, 1.40e-3, 0.405)
WEG25 = Fluid("WEG 50/50 @ 25C", 1070.0, 3300.0, 3.6e-3, 0.38)
WEGm40 = Fluid("WEG 50/50 @ -40C", 1095.0, 3050.0, 80e-3, 0.35)
PAO65 = Fluid("PAO-2 @ 65C", 775.0, 2300.0, 2.4e-3, 0.14)
A_MOD, FLOW, N_SW, P_SW = 84.0, 10.0, 6, 1000.0
def cartridge(name, gap, fin, H, L, base, k=K_CU, A=A_MOD, slot_w=4.0, port=14.0, orifice_kPa=0.0, hdr_u=0.5):
    side = math.sqrt(A)*10
    n_slots = max(1, int(round(side/(2*L))))
    return ColdPlate(name=name, footprint_cm2=A, fin_t_mm=fin, gap_mm=gap, fin_h_mm=H, flow_len_mm=L, base_mm=base,
                     k_solid=k, tim="direct-to-die", isothermal_cell=True, hotspot_flow_K=0.0,
                     n_parallel_paths=2*n_slots, slot_w_mm=slot_w, K_channel=3.0, K_slot=1.5,
                     header_u_m_s=hdr_u, K_header=1.0, port_bore_mm=port, K_port=2.3, orifice_dp_kPa_18=orifice_kPa)
def ev(cp, fluid, flow=FLOW, Q=N_SW*P_SW, T_in=65.0):
    # orifice_dp_kPa_18 in the model scales with (flow/18 LPM)^2; callers pass the value referenced to 18 LPM
    return cp.evaluate(Q, flow/(Q/1000.0), fluid=fluid, T_in=T_in)
