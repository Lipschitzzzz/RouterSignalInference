import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
import torch
import torch.nn.backends
from torch.utils.data import DataLoader,TensorDataset
from sklearn.model_selection import train_test_split
from torch.utils.tensorboard import SummaryWriter
import datetime

#--------------------------网络定义-------------------------------------
class DNNNet(torch.nn.Module):#supervised

    def __init__(self,input_dim,DNNlayer,is_bsnorm=False):
        super(DNNNet, self).__init__()     # 继承 __init__ 功能

        # Sequential是模块的有序容器。
        # 数据以定义的相同顺序通过所有模块。您可以使用顺序容器快速的组合一个网络。
        def block(in_feat, out_feat):
            layers = [torch.nn.Linear(in_feat, out_feat)]
            if is_bsnorm:
                layers.append(torch.nn.BatchNorm1d(out_feat, 0.8))
            layers.append(torch.nn.LeakyReLU(0.2, inplace=False))
            return layers

        self.net = torch.nn.Sequential(
            *block(input_dim, DNNlayer[0]),
            *block(DNNlayer[0], DNNlayer[1]),
            *block(DNNlayer[1], DNNlayer[2]),
            torch.nn.Linear(DNNlayer[2], 2),
        )
       
    def forward(self, x):
        ''' 定义前向传递函数'''
        # .squeeze() 返回一个删除输入张量中维度大小为1的张量
        return self.net(x).squeeze(1)#???
    
    def cal_loss(self, pred, target):
        ''' 定义损失计算函数 '''

        loss = torch.pow(pred-target,2)
        return loss
class DNNcls(torch.nn.Module):
    def __init__(self,input_dim,num_cls,DNNlayer,l1_strength,l2_strength,is_bsnorm=False):
        super(DNNcls, self).__init__()     # 继承 __init__ 功能
        self.l1_strength = l1_strength
        self.l2_strength = l2_strength
        # Sequential是模块的有序容器。
        # 数据以定义的相同顺序通过所有模块。您可以使用顺序容器快速的组合一个网络。
        def block(in_feat, out_feat):
            layers = [torch.nn.Linear(in_feat, out_feat)]
            if is_bsnorm:
                layers.append(torch.nn.BatchNorm1d(out_feat, 0.8))
            layers.append(torch.nn.LeakyReLU(0.2, inplace=False))
            return layers

        self.net = torch.nn.Sequential(
            *block(input_dim, DNNlayer[0]),
            *block(DNNlayer[0], DNNlayer[1]),
            *block(DNNlayer[1], DNNlayer[2]),
            torch.nn.Linear(DNNlayer[2], num_cls)
        )
       
    def forward(self, x):
        ''' 定义前向传递函数'''
        # .squeeze() 返回一个删除输入张量中维度大小为1的张量
        return self.net(x).squeeze(1)#???
    
    def cal_loss(self, pred, target):
        ''' 定义损失计算函数 '''

        loss = torch.pow(pred-target,2)
        return loss
    
class ResidualNet(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim1, hidden_dim2, output_dim,n_blocks,is_bsnorm):
        super(ResidualNet, self).__init__()
        self.n_blocks = n_blocks
        self.fc1 = torch.nn.Linear(input_dim, hidden_dim1)
        self.fc2 = torch.nn.Linear(hidden_dim1, hidden_dim1)

        def block(in_feat, out_feat):
            layers = [torch.nn.Linear(in_feat, out_feat)]
            if is_bsnorm:
                layers.append(torch.nn.BatchNorm1d(out_feat, 0.8))
            layers.append(torch.nn.LeakyReLU(0.2, inplace=False))
            return layers

        self.residual_layers = torch.nn.Sequential(
            *block(hidden_dim1, hidden_dim2),
            *block(hidden_dim2, hidden_dim1)
        )
        self.fc3 = torch.nn.Linear(hidden_dim1, output_dim)  # 输出层，预测位置的维度为2
    def cal_loss(self, pred, target):
        ''' 定义损失计算函数 '''

        loss = torch.pow(pred-target,2)
        return loss
    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        for _ in range(self.n_blocks):
            x = self.residual_layers(x) + x
        x = self.fc3(x)
        return x
#--------------------------数据预处理函数-------------------------------------

def get_device():
    ''' 判断GPU是否可用,可用则返回cuda,否则返回cpu'''
    return 'cuda' if torch.cuda.is_available() else 'cpu'


def prep_dataloader(df,feature_name,label_name,mode,batch_size,n_jobs=0):
    # torch.set_default_tensor_type(torch.FloatTensor)
    if label_name == 'class':
        y=torch.tensor(df[label_name].values,dtype=torch.int64)  
    else:
        y=torch.tensor(df[label_name].values).float() 
    x=torch.tensor(df[feature_name].values).float()#feature_name为网络输入向量的名字

    dataset = TensorDataset(x,y)

    dataloader = DataLoader(
        dataset, batch_size,
        shuffle=(mode == 'train' or mode == 'mixed_train'), drop_last=False,
        num_workers=n_jobs, pin_memory=True)                            # 构造数据加载器
    return dataloader


def convert_to_truevalue(df):
    '''
    将数据转换成真实值:
    actual value = RSRP(IE value - 157)
    actual value = RSRQ(IE value - 87)/2
    actual value = SINR(IE value - 46)/2  
    '''
    for col in df.columns:
        if col.find('Rsrp') != -1:
            df[col] = df[col] - 157

        elif col.find('Rsrq') != -1:
            df[col] = (df[col] - 87)/2

        elif col.find('Sinr') != -1:
            df[col] = (df[col] - 46)/2

    return df
def pci_ordered(df,config):
    #按pci标号重新整理
    colums = config['colums']
    df_in_pciorder = pd.DataFrame(data=df[['servTa','servRssi','x','y','class']],columns=colums+['x','y','class'])
    for i in range(len(df)):
        if i%1000==0:
            print('ordering in pci:sample {}/{}'.format(i,len(df)))
        for j in ['servPci','nbrPci_1','nbrPci_2','nbrPci_3','nbrPci_4','nbrPci_5']:
            pci = int(df.loc[i,j])
            if pci != 0:
                if j == 'servPci':
                    name_source = ['servRsrp', 'servRsrq','servSinr']
                else:
                    name_source = ['nbrRsrp_'+j[-1], 'nbrRsrq_'+j[-1],'nbrSinr_'+j[-1]]

                name_target = ['rsrp_'+str(pci),'rsrq_'+str(pci),'sinr_'+str(pci)]
                df_in_pciorder.loc[i,name_target] = df.loc[i,name_source].values
    return df_in_pciorder

def pci_ordered_testset(df,config):
    #按pci标号重新整理
    colums = config['colums']
    df_in_pciorder = pd.DataFrame(data=df[['servTa','servRssi']],columns=colums)
    for i in range(len(df)):
        # if i%10==0:
        #     print('ordering in pci:testset {}/{}'.format(i,len(df)))
        for j in ['servPci','nbrPci_1','nbrPci_2','nbrPci_3','nbrPci_4','nbrPci_5']:
            pci = int(df.loc[i,j])
            if pci != 0:
                if j == 'servPci':
                    name_source = ['servRsrp', 'servRsrq','servSinr']
                else:
                    name_source = ['nbrRsrp_'+j[-1], 'nbrRsrq_'+j[-1],'nbrSinr_'+j[-1]]

                name_target = ['rsrp_'+str(pci),'rsrq_'+str(pci),'sinr_'+str(pci)]
                df_in_pciorder.loc[i,name_target] = df.loc[i,name_source].values
    return df_in_pciorder

def smoothing(df,window_size,feature_list):
    # feature_list = ['servRsrp', 'servRsrq','servSinr', 'servRssi', 
    #             'nbrRsrp_1', 'nbrRsrq_1', 'nbrSinr_1', 
    #             'nbrRsrp_2', 'nbrRsrq_2', 'nbrSinr_2',
    #             'nbrRsrp_3', 'nbrRsrq_3', 'nbrSinr_3', 
    #             'nbrRsrp_4', 'nbrRsrq_4', 'nbrSinr_4', 
    #             'nbrRsrp_5','nbrRsrq_5', 'nbrSinr_5'
    #             ]
    for col in feature_list:
        smoothed_arr = np.convolve(df[col], np.ones(window_size) / window_size, mode='same')
        df[col] = smoothed_arr
        
    return df[window_size:-window_size]
def data_process_init(mode,source_path,config,is_convert=True,save_path=None,is_save=False):
    '''
    读取文件夹下的所有点的.log文件并解析,合并并返回dataframe\n
    total.xlsx:未按pci整理的所有点数据\n
    total_in_pciorder.xlsx:按pci整理后的所有点数据
    '''
    if not os.path.exists(os.path.join(save_path,mode)):
        os.mkdir(os.path.join(save_path,mode))
    if not os.path.exists(os.path.join(save_path,'total')):
        os.mkdir(os.path.join(save_path,'total'))

    filelist = os.listdir(source_path)
    filelist = [i for i in filelist if i.endswith('.log')]
    total = pd.DataFrame()
    for i,filename in enumerate(filelist):
        with open(os.path.join(source_path,filename), encoding="utf-8") as f:
            data = []
            row = 0
            for line in f.readlines():
                # print(line)
                line_splited = re.split('[\t| \n]',line)
                line_splited = [i for i in line_splited if i !='']
                if row != 0:
                    line_splited = [int(i) for i in line_splited]
                data.append(line_splited)
                row += 1
            df = pd.DataFrame(data=data[1:],columns=data[0])
            x = re.split('[_]',filename)[1]
            y = re.split('[_]',filename)[2]
            df[['x','y']] = [float(x),float(y)]
            df['class'] = i
            # if is_smoothing:
            #     df = smoothing(df,window_size=ws)
            total = pd.concat([total,df],ignore_index=True)

            if is_save is True:
                if save_path != None:
                    save_name = '{}_{}_raw.xlsx'.format(x,y)
                    df.to_excel(os.path.join(save_path,mode,save_name),index=False)
                else:
                    print('ERROR:save_path is none.')
        if i%10==0:
            print('loading data:point {}/{}:{}'.format(i,len(filelist),filename))
    if is_convert is True:
        total = convert_to_truevalue(total)
    #按pci标号重新整理
    df_in_pciorder = pci_ordered(df=total,config=config)
    if is_save is True:
        if save_path != None:
            # df_in_pciorder.to_excel(os.path.join(save_path,'total','total_in_pciorder(converted {}).xlsx'.format(is_convert)),index=False)
            total.to_excel(os.path.join(save_path,'total',mode+'(converted {}).xlsx'.format(is_convert)),index=False)

    return total,df_in_pciorder

def data_split(mode,features_train,label_name,data_normed,config,valid_ratio=0.2):
    #数据切分
    if mode == 'train':

        train_normed_filled = data_normed.sample(frac=1,ignore_index=True,replace=False,random_state=config['random_seed'])

        tr_set_raw = train_normed_filled[0:-int(len(train_normed_filled)*(valid_ratio))]
        tr_set_loader = prep_dataloader(df=tr_set_raw,feature_name=features_train,
                                        label_name=label_name,
                                        mode='train',batch_size=config['batch_size'])

        val_set_raw = train_normed_filled[-int(len(train_normed_filled)*(valid_ratio)):]
        val_set_loader = prep_dataloader(df=val_set_raw,feature_name=features_train,
                                         label_name=label_name,
                                         mode='valid',batch_size=config['batch_size'])
        return tr_set_loader,val_set_loader
    elif mode == 'test':
        test_normed_filled = data_normed.sample(frac=1,ignore_index=True,replace=False,random_state=config['random_seed'])

        tt_set_raw = test_normed_filled
        tt_set_loader = prep_dataloader(df=tt_set_raw,feature_name=features_train,
                                        label_name=label_name,
                                        mode='test',batch_size=config['batch_size'])

        return tt_set_loader
#--------------------------训练与测试相关函数-------------------------------------
#------------------------------------------------------------------------------
def valid(valid_set, model, device):
    model.eval()                                # 设置模型为测试模式，不会反向传输参数
    total_loss = 0
    for x, y in valid_set:                         
        x, y = x.to(device), y.to(device)       
        with torch.no_grad():                   # 取消梯度计算(加快运行速度)
            pred = model(x)                     # 前向计算
            rmse_loss = torch.sqrt(torch.mean(model.cal_loss(pred, y)))  # 计算损失
        total_loss += rmse_loss.detach().cpu().item() * len(x)  # 累加损失值
    total_loss = total_loss / len(valid_set.dataset)              # 计算平均的损失值

    return total_loss

def valid_cls(model, val_loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for x, labels in val_loader:
            x = x.to(device)
            labels = labels.to(device)
            outputs = model(x)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += np.array((predicted == labels)).sum().item()

    accuracy_val = correct / total
    return accuracy_val 

def test(tt_set, model, device):
    model.eval()                                
    preds,targets = [],[]
    for x,y in tt_set:                            
        x,y= x.to(device),y.to(device)                       
        with torch.no_grad():                   
            pred = model(x)                     
            preds.append(pred.detach().cpu())   # 记录每一批数据的预测值
            targets.append(y.detach().cpu())
    targets = torch.cat(targets, dim=0).numpy()
    preds = torch.cat(preds, dim=0).numpy()     # 融合每一批数据的预测值，并将其转化为numpy数据
    return preds,targets

def supervised_train(tr_set, valid_set, model, config, model_save_path,device,writer):
    '''训练 DNN '''
    n_epochs = config['n_epochs']  # 设置最大的训练轮次
    # 设置优化器
    optimizer = getattr(torch.optim, config['optimizer'])(
        model.parameters(), **config['optim_hparas'])
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 300, gamma=0.5, last_epoch=-1)
    
    # scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[300,600,1000,1500,2000], gamma=0.5)

    min_mse = 1000.
    loss_record = {'train': [], 'dev': []}      # 记录训练过程中的损失值
    early_stop_cnt = 0
    epoch = 0
    while epoch < n_epochs:
        model.train()                           # 将模型设置为训练模式
        for x, y in tr_set:                     # 开始迭代数据加载器
            optimizer.zero_grad()               # 设置梯度值为0
            x, y = x.to(device), y.to(device)   # 将数据转移到device中
            pred = model(x)                     # 前向传播
            rmse_loss = torch.sqrt(torch.mean(model.cal_loss(pred, y)))  # 计算损失
            rmse_loss.backward()                 # 启动反向传播，计算梯度
            optimizer.step()                    # 利用计算出来的梯度，更新参数
            loss_record['train'].append(rmse_loss.detach().cpu().item())
        scheduler.step()

        # 在完成一个epoch的训练后，在验证集上测试模型的效果
        
        dev_mse = valid(valid_set, model, device)
        writer.add_scalar("loss of supervised_train", dev_mse, epoch)
        if dev_mse < min_mse:
            # 若在验证集上得到更好的效果，则及时保存模型的参数
            min_mse = dev_mse
            print('Saving supervised_train model (epoch = {:4d}, loss = {:.4f})'
                .format(epoch + 1, min_mse))
            torch.save(model.state_dict(), model_save_path)  
            early_stop_cnt = 0
        else:
            early_stop_cnt += 1                         # 统计模型效果连续不变好的次数

        epoch += 1
        loss_record['dev'].append(dev_mse)
        if early_stop_cnt > config['early_stop']:
            # 如果模型连续不变好的次数大于预设值，则停止训练
            # 这往往代表模型已经不能够训练得到更好的结果，及时停止训练是一个较好的策略
            break

    print('Finished training after {} epochs'.format(epoch))
    return min_mse, loss_record 

def cls_train(tr_set, valid_set, model, criterion, config, is_save,model_save_path,device,writer):
    model.train()
    
    n_epochs = config['n_epochs']  # 设置最大的训练轮次
    # 设置优化器
    optimizer = getattr(torch.optim, config['optimizer'])(
        model.parameters(), **config['optim_hparas'])
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 300, gamma=0.5, last_epoch=-1)
    
    epoch = 0
    correct_per_epoch = []
    total = 0
    losses_per_epoch = []
    accuracies_per_epoch = []
    min_accu = 0.1
    early_stop_cnt = 0
    while epoch < n_epochs:
        correct = 0
        total = 0
        losses = []
        accuracies = []
        for x, labels in tr_set:
            x = x.to(device)
            labels = torch.LongTensor(labels)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(x)
            loss = criterion(outputs, labels)

            # # L1 正则化
            # l1_reg = torch.tensor(0., device=device)
            # for param in model.parameters():
            #     l1_reg += torch.norm(param, 1)
            
            # # L2 正则化
            # l2_reg = torch.tensor(0., device=device)
            # for param in model.parameters():
            #     l2_reg += torch.norm(param, 2)**2  # 求L2范数的平方
            
            # loss += model.l1_strength * l1_reg + model.l2_strength * l2_reg.sqrt()  # 对平方的L2范数求平方根

            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            a = np.array((predicted == labels)).sum().item()
            correct += a
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
        scheduler.step()

        writer.add_scalar("loss of cls", np.mean(losses), epoch)
        accuracy_epoch = correct / total #整体准确率
        accuracies_per_epoch.append(accuracy_epoch)
        losses_per_epoch.append(np.mean(losses))
        dev_accu = valid_cls(model, valid_set,device)
        if dev_accu > min_accu:
            # 若在验证集上得到更好的效果，则及时保存模型的参数
            min_accu = dev_accu
            print('Saving model (epoch = {:4d}, clsaccu = {:.4f})'
                .format(epoch + 1, min_accu))
            if is_save:
                torch.save(model.state_dict(), model_save_path)  
            early_stop_cnt = 0
        else:
            early_stop_cnt += 1                         # 统计模型效果连续不变好的次数
        if early_stop_cnt > config['early_stop']:
            # 如果模型连续不变好的次数大于预设值，则停止训练
            # 这往往代表模型已经不能够训练得到更好的结果，及时停止训练是一个较好的策略
            break
        # print("epoch{}/{} accu of cls: ".format(epoch,n_epochs),accuracy_epoch)
        epoch += 1
    print('Finished training after {} epochs'.format(epoch))
    
    return accuracies_per_epoch, losses_per_epoch
    
    
def Training(data_source_path,is_dropna,is_smooth,data_save_path,model_save_path,features_train,valid_ratio,config):
    '''
    输入参数说明：
    data_source_path:训练集.log文件所在文件夹路径
    data_save_path:.log预处理后转换成.xlsx保存至文件夹的路径
    model_save_path:训练模型保存路径，也是推理阶段模型加载读入路径
    is_convert:是否转换成真实值，如rsrp(dbm)=rsrp-157，默认为True
    is_save:是否保存.xlsx，第一次运行建议保存，后续可以直接从data_save_path中读取，无需重复预处理，设置为False

    返回参数：
    loss:训练阶段验证集的距离误差

    '''
    #创建一些必要的文件夹
    if not os.path.exists(data_save_path):
        os.mkdir(data_save_path)
    if not os.path.exists(os.path.join(data_save_path,'total')):
        os.mkdir(os.path.join(data_save_path,'total'))
    if not os.path.exists(model_save_path):
        os.mkdir(model_save_path)
    if not os.path.exists(os.path.join(os.path.abspath(os.path.join(data_source_path,'../..')),'Tensorboard_summary')):
        os.mkdir(os.path.join(os.path.abspath(os.path.join(data_source_path,'../..')),'Tensorboard_summary'))
   
    #获取训练数据
    device = get_device()
    ##先判断是否存在预处理过的文件，是则直接读取，反之进入预处理流程
    if os.path.exists(os.path.join(data_save_path,'total','train_pci_ordered.xlsx')):
        train_pci_ordered = pd.read_excel(os.path.join(data_save_path,'total','train_pci_ordered.xlsx'))
    else:
        train_total,train_pci_ordered = data_process_init(
                                                            source_path=data_source_path,
                                                            config=config,
                                                            is_convert=True,
                                                            mode='train',
                                                            save_path=data_save_path,
                                                            is_save=True
                                                            )
        train_pci_ordered.to_excel(os.path.join(data_save_path,'total',
                                                'train_pci_ordered.xlsx'),index=False) 
        train_total.to_excel(os.path.join(data_save_path,'total',
                                            'train_total.xlsx'),index=False)
    #数据预处理
    scaler = MinMaxScaler(feature_range=(0, 1))
    train_normed = pd.DataFrame(data=scaler.fit_transform(train_pci_ordered[config['colums']]),columns=config['colums'])
    train_normed[['x','y','class']] = train_pci_ordered[['x','y','class']]
    if not is_dropna:
        train_normed = train_normed.fillna(value=config['fillvalue'])

        train_normed.to_excel(os.path.join(data_save_path,'total',
                                                'train_normed(fillna).xlsx'),index=False)
    else:
        train_normed = train_normed.dropna(subset=features_train).reset_index(drop=True)
        
        train_normed.to_excel(os.path.join(data_save_path,'total',
                                                'train_normed(dropna).xlsx'),index=False)
        if is_smooth:
            train_normed = smoothing(df=train_normed,window_size=config['window_size'],feature_list=config['features_train'])

    #切分数据集
    tr_set_loader,val_set_loader = data_split(
                                                mode='train',
                                                features_train=features_train,
                                                data_normed=train_normed,
                                                label_name=['x','y'],
                                                valid_ratio=valid_ratio,
                                                config=config)
    #获取当前时间,开始训练
    print('-----------------training------------------')
    now = datetime.datetime.now()
    date = now.strftime('D%Y%m%d_%Hh%Mm%Ss')
    TIMESTAMP = "{0:%Y-%m-%dT%H-%M-%S}".format(now)
    tb_log_dir = os.path.join(os.path.join(os.path.abspath(os.path.join(data_source_path,'../..')),'Tensorboard_summary'),
                              TIMESTAMP)

    writer = SummaryWriter(tb_log_dir,flush_secs=10)
    modelname = date + ' DNNlayer{} batch={}.pth'.format(config['layer'],config['batch_size'])
    modelfile_save_path = os.path.join(model_save_path,modelname)#.ph文件

    model = DNNNet(input_dim=len(features_train),DNNlayer=config['layer'],is_bsnorm=config['is_bsnorm']).to(device)
    model_loss, model_loss_record = supervised_train(tr_set_loader, val_set_loader, model, 
                                                     config, modelfile_save_path,device,writer)

    print('model_loss: ',model_loss)

    return model_loss, model_loss_record

def Test_in_group(model_read_path,features_train,tt_set_loader,config):
    print('-----------------testing------------------')
    model = DNNNet(len(features_train),DNNlayer=config['layer'],is_bsnorm=config['is_bsnorm']).to(get_device())
    ckpt = torch.load(model_read_path, map_location='cpu')  # 载入先前保存的模型参数
    model.load_state_dict(ckpt)
    preds,targets = test(tt_set=tt_set_loader,model=model,device=get_device())
    position_erro = np.sqrt(np.sum(abs(preds-targets)**2,axis=1))
    return preds,position_erro

def Infering(model_read_path,data_save_path,tt_list,config,s,is_smoothing):
    col = ['seqNo', 'ueId', 'timeStamp', 'servPci', 'servRsrp', 'servRsrq',
       'servSinr', 'servTa', 'servRssi', 'nbrPci_1', 'nbrRsrp_1', 'nbrRsrq_1',
       'nbrSinr_1', 'nbrPci_2', 'nbrRsrp_2', 'nbrRsrq_2', 'nbrSinr_2',
       'nbrPci_3', 'nbrRsrp_3', 'nbrRsrq_3', 'nbrSinr_3', 'nbrPci_4',
       'nbrRsrp_4', 'nbrRsrq_4', 'nbrSinr_4', 'nbrPci_5', 'nbrRsrp_5',
       'nbrRsrq_5', 'nbrSinr_5']
    features_train = config['features_train']
    tt_df = pd.DataFrame(data=tt_list,columns=col)
    # tt_df[['x','y']] = [x,y]
    #转真实值
    tt_df_real = convert_to_truevalue(tt_df)
    #pci排序整理
    tt_pciordered = pci_ordered_testset(tt_df_real,config=config)

    #归一化
    scaler = MinMaxScaler(feature_range=(0, 1))
    train_df = pd.read_excel(os.path.join(data_save_path,'total','train_pci_ordered.xlsx'))
    scaler.fit(X=train_df[config['colums']])
    test_normed = pd.DataFrame(data=scaler.transform(tt_pciordered[config['colums']]),columns=config['colums'])
    # test_normed[['x','y']] = [x,y]
    # test_normed_filled = test_normed.fillna(value=config['fillvalue'])
    test_normed = test_normed.dropna(subset=features_train).reset_index()
    if len(test_normed) == 0:
        return np.nan
    if is_smoothing:
        mean_arr = []
        for j in range(0,len(test_normed)-s,s):
            mean = test_normed.iloc[j:j+s,:].mean()
            # df_smoothed = pd.concat([df_smoothed,mean.values],axis='index',ignore_index=True)
            mean_arr.append(mean)
        test_normed = pd.DataFrame(columns=test_normed.columns,data=mean_arr)
    x=torch.tensor(test_normed[features_train].values).float()#feature_name为网络输入向量的名字

    #获取model_save_path中最新的.pth
    list=os.listdir(model_read_path)
    list.sort(key=lambda fn: os.path.getmtime(os.path.join(model_read_path,fn)) if not os.path.isdir(os.path.join(model_read_path,fn)) else 0)
    pth_file = list[-1]
    print('curren selected model: ',pth_file)
    s = re.split('[ (,)]',list[-1])
    DNNlayer_test = (int(s[2]),int(s[4]),int(s[6]))
    model = DNNNet(len(features_train),DNNlayer=DNNlayer_test,is_bsnorm=config['is_bsnorm']).to(get_device())
    ckpt = torch.load(os.path.join(model_read_path,pth_file), map_location='cpu')  # 载入先前保存的模型参数
    model.load_state_dict(ckpt)
    model.eval() 
    with torch.no_grad():                   
        pred = model(x)                     
        # preds.append(pred.detach().cpu())   # 记录每一批数据的预测值
    return pred



def plot_CDFcurve(position_erro,label,title,fig_size=(8,5)):
    hist, bin_edges = np.histogram(a=position_erro, bins=10000, range=(0,6), weights=None, density=False)
    i = np.cumsum(hist/sum(hist))
    index = np.where(i<=0.8)[0][-1]
    accu_80_raw = bin_edges[index]
    index = np.where(i<=0.9)[0][-1]
    accu_90_raw = bin_edges[index]
    position_erro_cdf = i
    plt.figure(figsize=fig_size)
    plt.plot(bin_edges[:-1],position_erro_cdf,'r-',linewidth=1,label=label)
    plt.title(title)
    plt.xlabel('Positioning erro/m')
    plt.ylabel('CDF')
    plt.grid(ls='--')
    plt.legend()
    print('supervised test erro@80: ',accu_80_raw)
    print('supervised test erro@90: ',accu_90_raw)
    print('supervised test erro.mean: ',np.mean(position_erro))


