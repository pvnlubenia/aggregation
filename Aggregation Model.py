#
# An agent-based model of aggregation
# Largely based on Sayama
# https://math.libretexts.org/Bookshelves/Applied_Mathematics/Book%3A_Introduction_to_the_Modeling_and_Analysis_of_Complex_Systems_(Sayama)/19%3A_Agent-Based_Models/19.03%3A_Agent-Environment_Interaction
# See pdf "An agent-based model with environment-agent interaction using Python" for more details
#



### Needed libraries ###

import random as rd
import numpy as np
import matplotlib.pyplot as plt
import os



### Initialize class to create slime mold cells ###

class agent:
    pass



### Create slime mold cells ###

def create_agents():
    
    # Allow list of slime mold cells, the environment, and updated environment to be accessed outside the function
	global agents_list, env, next_env
    
    # Initialize list
	agents_list = []
    
    # Create specified number of slime mold cells
	for each_agent in range(n_agents):
        
        # Create an agent
		agent_ = agent()
        
        # Assign to a random location
		agent_.x = rd.randint(0, width-1)
		agent_.y = rd.randint(0, width-1)
        
        # Place slime mold cell on the list
		agents_list.append(agent_)
    
    # Initialize environment and updated environment
	env = np.zeros([width, width])
	next_env = np.zeros([width, width])



### Simulate change in cAMP concentration and chemotaxis of slime mold cells ###

def update():
    
    # Allow list of slime mold cells, the environment, and updated environment to be accessed outside the function
	global agents_list, env, next_env
    
    # cAMP concentration in each grid cell diffuses (based on diffusion equation) and decays
	for x in range(width):
		for y in range(width):
			next_env[x, y] = env[x, y] + D*((env[(x+1)%width, y] + env[(x-1)%width, y] + env[x, (y+1)%width]
												+ env[x, (y-1)%width] - 4*env[x, y])/(dh)**2)*dt - k*env[x, y]*dt
	# Variables for environment and updated environment are updated
    env, next_env = next_env, env
    
    # Each agent secretes cAMP
	for agent_ in agents_list:
		env[agent_.x, agent_.y] += f*dt

    # Chemotaxis of slime mold cells with probability based on a sigmoid function
	for agent_ in agents_list:
		new_x, new_y = (agent_.x + rd.randint(-1,2))%width, (agent_.y + rd.randint(-1,2))%width
		if np.exp((env[new_x, new_y] - env[agent_.x, agent_.y])/0.1)/(1 + np.exp((env[new_x, new_y]
				- env[agent_.x, agent_.y])/0.1)) > rd.random():
			agent_.x, agent_.y = new_x, new_y



### Visualize the state ###

def visualize():
    
    # Initialize subplots
	fig, ax = plt.subplots()
    
    # Plot the environment using grayscale gradient: light color for low cAMP concentration, dark color for high cAMP concentration
	ax.imshow(env, cmap = plt.cm.binary, vmin = 0, vmax = 1)
	
    # Coordinates of the slime mold cells
    x = [agent_.x for agent_ in agents_list]
	y = [agent_.y for agent_ in agents_list]
    
    # Plot the reversed coordinates (to be consistent with the plotting of plt.imshow)
	ax.plot(y, x, 'b.')
    
    # Title
	ax.set_title('Slime Mold Aggregation' + '\n' + 'Time: ' + str(time))
	
    # Horizontal axis label
    ax.set_xlabel(str(n_agents) + ' Cells || ' + 'cAMP Diffusion: ' + str(D) + '\n' + 'cAMP Decay: '
								+ str(k) + ' || cAMP Secretion: ' + str(f))
	
    # Remove extra tick marks on the axes
    ax.set_xticks([])
	ax.set_yticks([])
    
    # Prepare format of file name
	filename = 'Aggregation'
    
    # Starting filename count
	i = 1
    
    # Check if filename already exists; add 1 if it does
	while os.path.exists('{}{:d}.png'.format(filename, i)):
		i += 1
	
    # Save figure
    plt.savefig('{}{:d}.png'.format(filename, i), bbox_inches = 'tight', dpi = 300)



### Simulation ###

# Number of slime mold cells
n_agents = 1000

# Number of rows/columns in spatial array
width = 100

# cAMP diffusion constant
D = 0.001

# Spatial step size
dh = 0.01

# Time step size
dt = 0.01

# cAMP decay constant
k = 0.1

# cAMP secretion rate by a slime mold cell
f = 1.5

# Create slime mold cells
create_agents()

# Needed for label of initial state
time = 0

# Visualize initial state
visualize()

# Update the model 500 times
for i in range(5):
    for j in range(100):
        update()
    
    # Compute number of iterations
    time = (i+1)*(j+1)
    
    # Visualize the state every 100interations
    visualize()






