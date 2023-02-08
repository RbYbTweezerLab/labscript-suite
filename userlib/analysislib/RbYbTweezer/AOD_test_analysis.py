import lyse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from time import gmtime, strftime

# Is this script being run from within an interactive lyse session?
if lyse.spinning_top:
    # If so, use the filepath of the current shot
    h5_path = lyse.path
else:
    # If not, get the filepath of the last shot of the lyse DataFrame
    df = lyse.data()
    h5_path = df.filepath.iloc[-1]

# Instantiate a lyse.Run object for this shot
run = lyse.Run(h5_path)

# Get a dictionary of the global variables used in this shot
run_globals = run.get_globals()

# Extract the images 'before' and 'after' generated from camera.expose
images = [im.astype('uint16') for  im in run.get_images('Flea2_FW','images', 'probe_1', 'probe_2')]
# andor_images = run.get_images('z_insitu_ccd', 'test', 'frame_1', 'frame_2', 'frame_3')


# Compute the difference of the two images, after casting them to signed integers
# (otherwise negative differences wrap to 2**16 - 1 - diff)
# diff = images[1].astype('int16') - images[0].astype('int16')
# absorption = np.divide(diff,(images[1].astype('int16') - images[2].astype('int16')))

# andor_diff = andor_images[1].astype('int16') - andor_images[0].astype('int16')
# andor_absorption = np.divide(andor_diff,(andor_images[1].astype('int16') - andor_images[2].astype('int16')))


fig, axes = plt.subplots(nrows=1,ncols=2)

kwargs = {
    'cmap' : 'jet',
    'vmin' : 0,
    # 'vmax' : 9666 #2**16-1
}

axes[0].imshow(images[0], **kwargs)
axes[1].imshow(images[1], **kwargs)



fig.savefig('C:/Users/RbYbT/Desktop/Tempo/'+strftime("%d%H%M%S", gmtime())+'.png')



# axes[1,0].imshow(images[2], **kwargs)

# axes[1,1].imshow(diff, **kwargs)


# fig, axes = plt.subplots(nrows=2,ncols=2)

# kwargs = {
#     'cmap' : 'jet',
#     # 'vmin' : 0,
#     # 'vmax' : 255
# }

# axes[0,0].imshow(andor_images[0], **kwargs)
# axes[0,1].imshow(andor_images[1], **kwargs)
# axes[1,0].imshow(andor_images[2], **kwargs)

# axes[1,0].imshow(andor_diff, **kwargs)



# runmanager.set_value(ShutterTest_globals, Exposure, exptime_flea, 30e-3)      #global variable file is not in the same folder

