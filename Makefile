all:
	# python generate_povray_inc.py
	povray generate[sk] generate_spins.pov
	# This will crop the Figure
	convert skyrmion.png -gravity center -crop 1800x1000+0+160 skyrmion.png

clean:
	rm *.inc
	rm *.jpg *.png
