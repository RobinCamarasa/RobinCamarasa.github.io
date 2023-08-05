.PHONY: cv
	
cv:
	make -C submodules/curricullum-vitae/ all
	cp submodules/curricullum-vitae/cv.pdf static/cv.pdf
