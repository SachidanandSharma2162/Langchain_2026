import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

class ImageClassifierNet(nn.Module):
    def __init__(self, num_classes):
        super(ImageClassifierNet, self).__init__()
        self.hidden = nn.Linear(128 * 128, 256)
        self.output = nn.Linear(256, num_classes)
        
    def forward(self, x):
        x = x.view(x.size(0), -1) 
        x = torch.sigmoid(self.hidden(x))
        x = self.output(x)
        return x

def train_image_network():
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((128, 128)),
        transforms.ToTensor()
    ])

    print("Generating synthetic 128x128 dataset for demonstration...")
    dataset = datasets.FakeData(size=1000, image_size=(1, 128, 128), num_classes=5, transform=transform)
    
    num_classes = len(dataset.classes) if hasattr(dataset, 'classes') else 5

    dataset_size = len(dataset)
    train_size = dataset_size // 2
    val_size = dataset_size - train_size
    
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    
    model = ImageClassifierNet(num_classes)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 5
    
    print(f"Training on {train_size} images, Validating on {val_size} images.")
    print(f"Input dimensions: 1x128x128 | Number of classes: {num_classes}\n")

    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for images, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
        avg_train_loss = train_loss / len(train_loader)
        
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                
        avg_val_loss = val_loss / len(val_loader)
        val_accuracy = 100 * correct / total
        
        print(f"Epoch [{epoch+1}/{epochs}] | Train Loss: {avg_train_loss:.4f} | "
              f"Val Loss: {avg_val_loss:.4f} | Val Accuracy: {val_accuracy:.2f}%")

if __name__ == "__main__":
    train_image_network()