import torch
import torch.nn as nn
import torch.optim as optim

X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
y = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)

class XORNet(nn.Module):
    def __init__(self):
        super(XORNet, self).__init__()
        self.hidden = nn.Linear(2, 4)
        self.output = nn.Linear(4, 1)
        
        
    def forward(self, x):
        x = torch.sigmoid(self.hidden(x))
        x = torch.sigmoid(self.output(x))
        return x

def train_xor():
    model = XORNet()
    
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.5)
    
    epochs = 5000
    
    for epoch in range(epochs):
        optimizer.zero_grad()    
        predictions = model(X)   
        loss = criterion(predictions, y) 
        loss.backward()          
        optimizer.step()         
        
        if (epoch + 1) % 1000 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

    print("\nFinal Predictions:")
    with torch.no_grad():
        for i in range(len(X)):
            pred = model(X[i]).item()
            print(f"Input: {X[i].tolist()} | Target: {y[i].item()} | Output: {pred:.4f}")

if __name__ == "__main__":
    train_xor()