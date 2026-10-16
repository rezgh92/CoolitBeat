from heleshaw import run
print("--- sensitivity: h +30% (entrance/impingement enhancement) on proposal geometry")
run([(0.25,0.75),(1.25,1.65)],[(2.35,2.75),(3.25,3.75)],h=13.2e3*1.3,label="proposal + grate, h x1.3")
print("--- fixes: narrow fin-level openings via the grate (land >> fin height)")
run([(0.0,0.4)],[(3.6,4.0)],label="H2.0, 0.8 mm openings, 3.2 mm land")
run([(0.0,0.4)],[(3.6,4.0)],H=1.0,label="H1.0, 0.8 mm openings, 3.2 mm land")
run([(0.0,0.25)],[(3.75,4.0)],H=1.0,label="H1.0, 0.5 mm openings, 3.5 mm land")
run([(0.0,0.25)],[(1.75,2.0)],L=2.0,H=1.0,label="L2 (4 mm pitch), H1.0, 0.5 mm openings")
run([(0.0,0.4)],[(3.6,4.0)],H=1.5,label="H1.5, 0.8 mm openings, 3.2 mm land")
