import os

# 输入输出文件夹
BASEDIR = 'G:/零点播'
# ssh出的全量统计数据
sshFile = {
    'filename': os.path.join(BASEDIR, 'baiming.csv'),
    'types': {'CSP_CODE': str, 'NAME': str, 'CREATE_PEOPLE': str}
}
# CP代码和CP名称对照表
cpFile = os.path.join(BASEDIR, 'spname.xlsx')
# 全量数据文件（文本）
allProgramFile = {
    'filename': os.path.join(BASEDIR, '点播全量.TXT'),
    #                    'filename':os.path.join(BASEDIR,'全量点播数据.txt'),
    'types': {'CONTENTNAME': str, 'CONTENTCODE': str, 'TELECOMCODE': str, 'CREATETIME': str, 'FILESIZE': int}
}
# 播放数据文件，多个填写到列表中
playCountsFile = [
    os.path.join(BASEDIR, '7月1日至今有播放记录节目清单.txt'),
    os.path.join(BASEDIR, '201909点播(1).txt'),
    os.path.join(BASEDIR, '20191011点播.txt'),
]
# 播放数据文件的字段类型
playCountsTypes = {'ZXCode': str, 'Duration': float, 'PlayCount': int}

# 输出文件，0次点播和N次点播
outExcelFile = {
    0: os.path.join(BASEDIR, 'zero1010_0.xlsx'),
    3: os.path.join(BASEDIR, 'zero1010_3.xlsx'),
}
allOutputFile = os.path.join(BASEDIR, '全量数据1011.csv')
# 截至日期
timePoint = '20190701000000'
