import numpy as np
import trimesh
from noise import pnoise2
import matplotlib.pyplot as plt
import math
# Parameters
size = 28           # Grid size
scale = 0.875        # Standard deviation for Gaussian
size_fact = 0.1

# Generate XY grid
x = np.linspace(0, 1, size)
y = np.linspace(0, 1, size)
x, y = np.meshgrid(x, y)

def saddle(x,y):

    return (x**2)/100 - (y**2)/100

# Compute Perlin noise surface
z_top = np.array([[saddle((size_fact*(i-math.floor(size/2))),(size_fact*(j-math.floor(size/2)))) for j in range(size)] for i in range(size)])
# Normalize and scale the noise to desired amplitude
z_top = (z_top - z_top.min()) / (z_top.max() - z_top.min()) *0.9  # Normalize to [0, 1]
# z_top *= amplitude
z_top += 0.1  # Offset to ensure all points are above zero

# Flatten grid to list of (x, y, z)
vertices_top = np.column_stack((x.flatten(), y.flatten(), z_top.flatten()))
vertices_bottom = np.column_stack((x.flatten(), y.flatten(), np.zeros_like(z_top).flatten()))

print(vertices_top)

print(vertices_top.shape)


# Total vertices = top + bottom
vertices = np.vstack((vertices_top, vertices_bottom))

# plot the 3d surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_zlim([0, 2])
ax.plot_surface(x, y, z_top, cmap='viridis', edgecolor='none')
plt.title('3D Points')
plt.show()


# Faces for top surface
faces = []
for i in range(size - 1):
    for j in range(size - 1):
        idx = i * size + j
        a, b, c, d = idx, idx + 1, idx + size, idx + size + 1
        # Top
        faces.append([a, b, c])
        faces.append([b, d, c])
        # Bottom (reverse order for correct normal)
        offset = size * size
        a, b, c, d = a + offset, b + offset, c + offset, d + offset
        faces.append([c, b, a])
        faces.append([c, d, b])

# Add side walls
def side_wall(a_top, b_top, a_bot, b_bot):
    return [
        [a_top, b_top, a_bot],
        [b_top, b_bot, a_bot]
    ]

offset = size * size
for i in range(size - 1):
    # Front wall
    a, b = i, i + 1
    faces += side_wall(a, b, a + offset, b + offset)
    # Back wall
    a, b = (size * (size - 1) + i, size * (size - 1) + i + 1)
    faces += side_wall(a, b, a + offset, b + offset)
    # Left wall
    a, b = i * size, (i + 1) * size
    faces += side_wall(a, b, a + offset, b + offset)
    # Right wall
    a, b = i * size + size - 1, (i + 1) * size + size - 1
    faces += side_wall(a, b, a + offset, b + offset)

# Create the mesh
mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)

# Export to STL
mesh.export('saddle_surface_with_base.stl')
