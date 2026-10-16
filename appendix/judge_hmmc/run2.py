from heleshaw import run
g=([(0.25,0.75),(1.25,1.65)],[(2.35,2.75),(3.25,3.75)])
run(*g,label="proposal + grate, d=0.025")
run(*g,d=0.05,label="proposal + grate, d=0.05 (grid check)")
run([(0.0,1.65)],[(2.35,4.0)],label="proposal slots, no grate")
run([(0.0,1.65)],[(2.35,4.0)],kfz_mult=1e4,label="no grate, fluid well-mixed in z (1-D check)")
run([(0.0,0.5)],[(3.5,4.0)],label="1.0 mm openings, 3.0 mm land")
run([(0.0,0.5)],[(3.5,4.0)],kfz_mult=1e4,label="1.0/3.0 well-mixed in z")
run([(0.0,1.0)],[(3.0,4.0)],label="2.0 mm openings, 2.0 mm land")
