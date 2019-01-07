#!/usr/bin/env python
import win
import gamescene
import titlescene
import gameinput

def main():
	
	win.init()
	gs = gamescene.GameScene()
	ts = titlescene.TitleScene()
	curscene = ts
	curscene.enterscene()

	while not curscene.quit:

		# handle scene transitions
		if curscene.exit:
			curscene.exit = False # Clear message
			curscene = gs if curscene.id == "Title Scene" else ts 
			curscene.enterscene()



		win.clear() 						# Clear the window back buffer.
		curscene.update()					# Do all scene updates for the current scene.
		win.flip()							# flip to the front buffer.
		gameinput.processinput()			# Handle user input.

main()
