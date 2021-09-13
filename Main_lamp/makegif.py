from PIL import Image
import imageio

'''   -- Example --
dir =           '/Users/Administrador/Desktop/07-06-21/2/'
image_format =  '.png'
gif_name =      'compiled.gif'
duration_frame = 0.1 # Seconds.
loop_times =     0         # 0 to infinite.
images_number =  58        # start name in 0. e.g. 0 to 58.
'''

def make_gif(dir, image_format, gif_name, duration_frame, loop_times, images_number):
    images = []
    for x in range(images_number+1):
        try:
            images.append(Image.open(dir + str(x) + image_format))
        except:
            pass
    imageio.mimsave(dir + gif_name, images, duration = duration_frame, loop=loop_times) 

#make_gif('/home/pi/Desktop/Lamp Chip/Main_lamp/Fotos_processo/05-07-2021-16-22/', '.png', 'compiled_loop.gif', 0.1, 0, 58 )
