import torch.nn as nn
import torch.nn.functional as F

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.lupas1   = nn.Conv2d(3, 32, 3, padding=1)
        self.lupas2   = nn.Conv2d(32, 64, 3, padding=1)
        self.encolher = nn.MaxPool2d(2)
        self.juiz1    = nn.Linear(64*8*8, 128)
        self.juiz2    = nn.Linear(128, 10)

    def forward(self, x):
        x = self.encolher(F.relu(self.lupas1(x)))
        x = self.encolher(F.relu(self.lupas2(x)))
        x = x.flatten(1)
        x = F.relu(self.juiz1(x))
        return self.juiz2(x)
