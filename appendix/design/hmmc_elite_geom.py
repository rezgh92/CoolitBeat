import math
rho=1005.0; Q=18/60e3  # m3/s
print("== Hydraulic sizing at 18 LPM (PG25) ==")
for name,q,ucap in (("port (16 mm bore)",Q,1.5),("trough end (Q/2, both-end fed)",Q/2,0.86),("perimeter loop (Q/2)",Q/2,1.0),("outlet trough end (Q/2, 1.5x)",Q/2,0.57),("outlet loop (Q/2, 1.5x)",Q/2,0.67)):
    A=q/ucap*1e6; print(f"{name:38s} q={q*6e4:5.1f} LPM  u<={ucap:.2f} m/s -> A>={A:5.0f} mm2  head={0.5*rho*ucap**2:4.0f} Pa")
d=16e-3; u=Q/(math.pi/4*d*d); print(f"16 mm port velocity {u:.2f} m/s; 20 mm: {Q/(math.pi/4*0.02**2):.2f} m/s")
# troughs at 6 mm depth
print("troughs at 6.0 mm depth: inlet 175/6=%.0f mm wide, outlet 260/6=%.0f mm wide, +3 mm wall = %.0f mm of 108"%(175/6,260/6,175/6+260/6+3))
print("troughs at 4.0 mm depth (LP15): inlet 150/4=%.1f, outlet 225/4=%.1f -> %.1f mm"%(150/4,225/4,150/4+225/4+3))
# slots
n_in=14; q_slot=Q/n_in; print(f"\nuniform TTV: {n_in} inlet slots, {q_slot*6e4:.2f} LPM/slot, half-slot {q_slot/2*6e4:.2f} LPM")
A_slot=3.3*6.5; u_s=q_slot/2/(A_slot*1e-6); print(f"feed slot 3.3 x 6.5 mm = {A_slot:.1f} mm2 -> entry u {u_s:.2f} m/s, head {0.5*rho*u_s**2:.0f} Pa; branch 2.4 kPa -> ratio {2400/(0.5*rho*u_s**2):.0f} (need >=15)")
# comb
n_h=92; d_h=0.5e-3; A_h=n_h*math.pi/4*d_h**2; u_h=q_slot/A_h; K=3.0
print(f"comb: {n_h} x 0.5 mm holes/slot, open {A_h*1e6:.1f} mm2, jet u {u_h:.2f} m/s, dP(K={K}) {K*0.5*rho*u_h**2/1e3:.2f} kPa; total holes {n_h*n_in}, q/hole {q_slot/n_h*6e4*1e3:.1f} mL/min")
# grate descent
A_open=0.5*108*3.3/1.0  # 50% of slot floor
print(f"grate descent velocity {q_slot/(A_open*1e-6):.3f} m/s (cap 0.5)")
# zoned real package
A_die=4*2.6*3.3; A_hbm=16*1.1*1.2; A_tot=117; A_rest=A_tot-A_die-A_hbm
w={"die":3.0,"hbm":0.32,"rest":0.04}
tot=A_die*w["die"]+A_hbm*w["hbm"]+A_rest*w["rest"]
f_die=A_die*w["die"]/tot; f_hbm=A_hbm*w["hbm"]/tot; f_rest=A_rest*w["rest"]/tot
N=n_h*n_in
print(f"\nzoning (H-Z2): die {A_die:.1f} cm2 gets {f_die*100:.0f}% ({f_die*18:.1f} LPM), HBM {A_hbm:.1f} cm2 {f_hbm*100:.1f}%, rest {A_rest:.1f} cm2 {f_rest*100:.1f}%")
print(f"holes: die {f_die*N:.0f} ({f_die*N/A_die:.1f}/cm2, {f_die*N/A_die*0.33:.1f} per cm of slot), HBM {f_hbm*N:.0f} ({f_hbm*N/A_hbm:.1f}/cm2), rest {f_rest*N:.0f}")
n_die_in=7; q_die=f_die*Q/n_die_in; A_slot5=4.3*6.5; u5=q_die/2/(A_slot5*1e-6)
print(f"die-zone inlet slots: {n_die_in}, {q_die*6e4:.2f} LPM each; 4.3 x 6.5 mm slot (10 mm pitch) entry u {u5:.2f} m/s head {0.5*rho*u5**2:.0f} Pa; branch 2.2+1.1 kPa -> ratio {3300/(0.5*rho*u5**2):.0f}")
u_ch=0.083*3*(5/4)/(5/4); print(f"die-zone channel velocity ~{0.083*3:.2f} m/s (Re ~{19*3:.0f}), friction ~{0.23*(5/4)**2*3:.2f} kPa")
# heights
stack=[("base (as-bonded; 0.8 finished)",1.0),("skived fins",2.0),("tie grate G (etched)",0.5),("lower plenum P (etched)",1.5),("comb C (etched)",0.4),("feed slots in block B (pockets)",6.5),("block floor / window plate",0.7),("troughs (bow-tie)",6.0),("cover (post-tied)",2.5)]
print("\n== stack-up standard =="); h=0
for n,t in stack: h+=t; print(f"  {n:36s} {t:4.1f} mm  (cum {h:4.1f})")
lp=[1.0,1.5,0.5,1.2,0.4,5.0,0.7,5.0,2.5]; print("low-profile 18:",sum(lp)); lp15=[1.0,1.5,0.5,1.0,0.4,4.5,0.7,4.0,2.0]; print("LP15:",sum(lp15))
# mass
body=148*152; core=11.7+9.4; lam=(0.5*0.5+1.5*0.6+0.4*0.9)*body/1e3*0.01*100  # cm3
lam=(0.5*0.5+1.5*0.6+0.4*0.9)/10*body/100  # mm*frac -> cm3: (mm thickness * fraction)/10 * area(cm2)
blk=11.5/10*body/100*0.45; cov=2.5/10*body/100; ears=30
tot_cm3=core+lam+blk+cov+ears; print(f"\nmass: core {core:.0f} + laminates {lam:.0f} + block {blk:.0f} + cover {cov:.0f} + ears {ears} = {tot_cm3:.0f} cm3 -> {tot_cm3*8.94/1e3:.2f} kg")
# Rubin-class plate 110x120 body, 16 mm
b2=110*120; m2=(1.0+2.0*0.4)/10*b2/100*0.6 + (0.5*0.5+1.5*0.6+0.4*0.9)/10*b2/100 + 9/10*b2/100*0.45 + 2.0/10*b2/100 + 10
print(f"Rubin-class plate ~{m2*8.94/1e3:.2f} kg")
# tie stress
for burst in (1.5,3.0):
    s=burst*0.25/(0.10*0.5); print(f"tie stress at burst {burst} MPa, 50% bonded tips: {s:.1f} MPa (SF vs 70 MPa yield {70/s:.1f}; with Kt 2.5 {70/s/2.5:.1f}; vs 220 UTS {220/s:.1f})")
# cost roll-up
cost10={"OFE Cu material (2.3 kg incl. swarf, $11/kg)":26,"skived core 0.10/0.15x2.0 over 117 cm2":40,"3 etched laminates (G,P,C)":36,"CNC manifold block (pockets, troughs, posts, bores)":80,"cover plate + port stubs":14,"one-shot vacuum diffusion bond cycle":55,"screen cartridge, plug, dP taps":15,"finish lapping + inspection":12,"mounting frame, spring screws":20,"100% He leak + flow/dP test":8}
cost100={"OFE Cu material (2.3 kg incl. swarf, $11/kg)":24,"skived core 0.10/0.15x2.0 over 117 cm2":24,"3 etched laminates (G,P,C)":16,"CNC manifold block (pockets, troughs, posts, bores)":34,"cover plate + port stubs":6,"one-shot vacuum diffusion bond cycle":32,"screen cartridge, plug, dP taps":8,"finish lapping + inspection":6,"mounting frame, spring screws":14,"100% He leak + flow/dP test":5}
s10=sum(cost10.values()); s100=sum(cost100.values())
print(f"\ncost 15 kW-class: subtotal 10k ${s10}, 100k ${s100}; with 12% yield/scrap/overhead: ${s10*1.12:.0f} / ${s100*1.12:.0f}")
print(f"Rubin-class (0.45x area, same process count): ~${(s10*1.12*0.7):.0f} / ${(s100*1.12*0.72):.0f}")
