import pandas as pd

allPrograms = pd.DataFrame({'ContentName': ['aaaa', 'bbbb', 'cccc', 'dddd'],
                    'TelecomCode': ['1111', '2222', '3333', '4444'],
                    'ZXCode': ['00110011001100110011', '00220011001100110011', '00330011001100110011', '00440011001100110011'],
                    'CreateTime':['20190101000000','20180102000000','20170103000000','20180304000000'],
                    'filesize': [2014.0, 1900.0, 1000.0, 999.2]})
playCounts1 = pd.DataFrame({'ContentName':['aaaa','bbbb','dddd'],
                           'ZXCode':['00110011001100110011', '00220011001100110011', '00440011001100110011'],
                           'Duration':[1.0,2.0,3.0],
                           'PlayCount':[10,100,1000]})
playCounts2 = pd.DataFrame({'ContentName':['aaaa','bbbb','dddd'],
                           'ZXCode':['00110011001100110011', '00220011001100110011', '00440011001100110011'],
                           'PlayCount':[15,150,1500],
                           'Duration': [5.0, 6.0, 7.0],
                            })
sshPrograms = pd.DataFrame({"CSP_CODE":['2222','3333','1111','4444','5555'],
                            "NAME":['bbbb','cccc','aaaa','dddd','eeee'],
                            "CREATE_PEOPLE":['UT','BestTV','CNTV','BestTV','UT']})
cps = pd.DataFrame({'CPCODE':['UT','BestTV','CNTV','GLST'],
                    'CPName':['UTSTarCom','百视通','央视','广联视通']})

print(allPrograms)
print(playCounts1)
print(playCounts2)
print(sshPrograms)
print(cps)


playCounts = pd.concat([playCounts1,playCounts2],sort=False)


print(playCounts)
print('--------------------------------------')

allPrograms_with_CP_CODE = pd.merge(allPrograms,sshPrograms,left_on='TelecomCode',right_on='CSP_CODE',how = 'left')
print(allPrograms_with_CP_CODE.info())
allPrograms_with_CP_NAME = pd.merge(allPrograms_with_CP_CODE,cps,left_on='CREATE_PEOPLE',right_on='CPCODE',how = 'left')
print(allPrograms_with_CP_NAME.info())

print(allPrograms_with_CP_NAME)

print('-----------------++++++++++------------------')
groupd = playCounts.groupby('ZXCode')
print(groupd['Duration','PlayCount'].sum().info())
result = pd.merge(allPrograms_with_CP_NAME,groupd['Duration','PlayCount'].sum(),left_on = 'ZXCode',right_on = 'ZXCode',how = 'left')
result = result.fillna({'CPName':'NotFound','Duration':0.0,'PlayCount':0})

result = result[(result['PlayCount'] >= 0) & (result['CreateTime'] < '20191231000000')]
#writer = pd.ExcelWriter('G:/零点播/test.xlsx')
#result.to_excel(writer,sheet_name='零点播数据',index=False,columns=['ContentName','TelecomCode','CreateTime','filesize','CPName'])
import numpy as np
cpResult = result.groupby('CPName')['filesize'].agg([np.size,np.sum])
cpResult.columns = ['节目数','占用存储']
#cpResult.to_excel(writer,sheet_name='统计数据')
#writer.save()

print(cpResult)

