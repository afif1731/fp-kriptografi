import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# Parameter Lorenz
sigma, rho, beta = 10, 28, 8/3

def lorenz_system(state, dt):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz]) * dt

# Runge-Kutta 4 untuk Lorenz
def rk4_lorenz(initial_state, dt, steps):
    trajectory = [initial_state]
    state = np.array(initial_state)
    for _ in range(steps):
        k1 = lorenz_system(state, dt)
        k2 = lorenz_system(state + 0.5 * k1, dt)
        k3 = lorenz_system(state + 0.5 * k2, dt)
        k4 = lorenz_system(state + k3, dt)
        state += (k1 + 2*k2 + 2*k3 + k4) / 6
        trajectory.append(state)
    return np.array(trajectory)

# Generate dataset
initial_state = [0.1, 0.1, 0.1]
dt = 0.01
steps = 10000
data = rk4_lorenz(initial_state, dt, steps)

class LorenzDataset(Dataset):
    def __init__(self, data):
        self.x = torch.tensor(data[:-1], dtype=torch.float32)
        self.y = torch.tensor(data[1:], dtype=torch.float32)
    
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

dataset = LorenzDataset(data)
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

class LorenzANN(nn.Module):
    def __init__(self):
        super(LorenzANN, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(3, 8),
            nn.ReLU(),
            nn.Linear(8, 8),
            nn.ReLU(),
            nn.Linear(8, 3)
        )
    
    def forward(self, x):
        return self.model(x)

# Inisialisasi model
model = LorenzANN()
criterion = nn.MSELoss()
optimizer = optim.RMSprop(model.parameters(), lr=0.001)

# Training loop
epochs = 10
for epoch in range(epochs):
    total_loss = 0
    for x_batch, y_batch in dataloader:
        optimizer.zero_grad()
        outputs = model(x_batch)
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(dataloader)}")
print("RK4 model is ready")


def generate_random(model, seed, steps=1):
    state = torch.tensor(seed, dtype=torch.float32).unsqueeze(0)
    for _ in range(steps):
        state = model(state)
    return int((state[0, 0].item() * 1e6) % 23)  # Modulo sesuai dengan ElGamal

# Contoh penggunaan
# seed = [0.1, 0.1, 0.1]
# k = generate_random(model, seed)
# print("Generated random value:", k)