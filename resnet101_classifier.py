import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
import cv2
import numpy as np
from skimage.io import imread 
import matplotlib.pyplot as plt
import glob

class CustomDataset(Dataset):
    def __init__(self, data, bins, transform=None):
        
        self.data = data
        self.transform = transform
        self.bins = bins
        self.encode = {
            150: 0,
            180: 1,
            210: 2,
            240: 3,
            270: 4,
            300: 5,
            330: 6,
            360: 7
        }

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        img = np.array(Image.open(self.data[index]).convert('RGB'))
        img = cv2.resize(img, (48,48))
        img = (img - np.min(img)) / (np.max(img) - np.min(img) + 0.0001)
        img = np.reshape(img, (3, 48,48))

        assert not np.isnan(img).any()

        img = Image.open(self.data[index]).convert('RGB')
        # if np.isnan(img).any():
        #     print(img)

        # plt.imshow(img)
        # plt.show()
        
        if self.transform is not None:
            img = self.transform(img)
            
        assert '_500_' in self.data[index]
        raw_label = int(self.data[index].split('_500_')[1].split('.png')[0])
        binned_label_int = self.find_nearest(raw_label)
        encoded_label = self.encode[binned_label_int]
        
        return img, encoded_label
    
    def viz(self):
        img = imread(self.data.iloc[0, 0])
        plt.imshow(img)

    def find_nearest(self, value):
        idx = (np.abs(self.bins-np.ceil(value))).argmin()
        return self.bins[idx]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

root = "/home/kashis/Desktop/misc/Capstone/GIS-AI project/Pivot GIS Project/images_classification"
num_classes = 8
classes = [150, 180, 210, 240, 270, 300, 330, 360]

dataset = CustomDataset(glob.glob(root+"/*.png"), bins = classes, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

model = models.resnet101(pretrained=True)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, num_classes)

model.load_state_dict(torch.load('resnet101_custom_dataset.pth'))

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

num_epochs = 50
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in dataloader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()

        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)

    epoch_loss = running_loss / len(dataset)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}")

torch.save(model.state_dict(), 'resnet101_custom_dataset.pth')
