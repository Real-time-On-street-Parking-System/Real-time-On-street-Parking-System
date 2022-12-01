import torch.nn as nn
import torch
import torch.nn.functional as F

class PredictNet(nn.Module):
    def __init__(self,input_size=1,hidden_size=64,num_layers=1):
        super(PredictNet,self).__init__()
        self.rnn = nn.GRU(input_size= input_size,hidden_size=hidden_size,num_layers=num_layers)
        self.output = nn.Linear(hidden_size,1)

    def forward(self,x):
        x = self.rnn(x)[0]
        x = self.output(x)
        return x

class Engine:
    count = 0
    save_every_epochs = 50

    def __init__(self) -> None:
        super(Engine,self).__init__()    

    def train(self,model,data=None,gt=None):
        L, B, C = 5, 8, 1
        data = torch.randn(L,B,C)
        gt = torch.randn(L,B,1)

        predict = model(data)
        loss = F.mse_loss(predict,gt)
        loss.backward()
        
        self.count +=1
        if self.count % self.save_every_epochs:
            self.save_model(model)

    def eval(model,data):
        with torch.no_grad():
            return model(data)

    def save_model(model):
        torch.save({
            'model_state_dict': model.state_dict(),
        })

model = PredictNet()
engine = Engine()