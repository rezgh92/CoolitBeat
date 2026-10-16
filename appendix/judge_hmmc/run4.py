from heleshaw import run
print("--- die zone, 350 W/cm2, 10 mm pitch (5 mm half-cell), dTout 12.9 K")
run([(0.0,2.15)],[(2.85,5.0)],L=5.0,q=3.5e6,dTout=12.9,label="die zone as proposed: 4.3 mm slots, 0.7 wall")
run([(0.0,2.15)],[(2.85,5.0)],L=5.0,q=3.5e6,dTout=12.9,kfz_mult=1e4,label="  same, fluid well-mixed in z")
run([(0.0,0.4)],[(4.6,5.0)],L=5.0,q=3.5e6,dTout=12.9,H=1.5,label="die zone fixed: 0.8 mm openings, H1.5")
