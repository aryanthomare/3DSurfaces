import numpy as np
import trimesh
from noise import pnoise2
import matplotlib.pyplot as plt
# Parameters
size = 50           # Grid size
scale = 0.08         # Perlin noise scale
amplitude = 1.0     # Max height of surface

# Generate XY grid
x = np.linspace(0, 1, size)
y = np.linspace(0, 1, size)
x, y = np.meshgrid(x, y)

# Compute Perlin noise surface
z_top = np.array([[pnoise2(i * scale, j * scale) for j in range(size)] for i in range(size)])
# Normalize and scale the noise to desired amplitude
z_top = (z_top - z_top.min()) / (z_top.max() - z_top.min())  # Normalize to [0, 1]
# z_top *= amplitude
# z_top += 1.0  # Offset to ensure all points are above zero

# Flatten grid to list of (x, y, z)
vertices_top = np.column_stack((x.flatten(), y.flatten(), z_top.flatten()))
vertices_bottom = np.column_stack((x.flatten(), y.flatten(), np.zeros_like(z_top).flatten()))

print(vertices_top)

print(vertices_top.shape)


# Total vertices = top + bottom
vertices = np.vstack((vertices_top, vertices_bottom))

#plot the 3d points
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], c='b', marker='o')
# plt.title('3D Points')
# plt.show()


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
mesh.export('perlin_surface_with_base.stl')
