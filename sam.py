
import os
from shutil import copyfile


input()
t=os.getcwd()
try:
	os.mkdir('songs')
except Exception:
	pass
for (root,dirs,files) in os.walk(os.getcwd()): 
    print('checking in ',root )
    for i in files:
    	if (i.endswith('.mp3')):
    		try:
    			copyfile(root+'/'+i,t+'/songs/'+i)
    		except Exception:
    			k=i.split('.')
    			k=k[0]+'1.mp3'
    			
    		


    print('--------------------------------')