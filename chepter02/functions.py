import pandas as pd
import numpy as np
import settings

'''
handle UncodeDecodeError,default use UTF8
if other Error Occured,return None
parameters:
    filename:TXT/CSV FileName
    sep:colums delimeter,default is ','
return:
    file to pandas datasheet 
'''


def my_read_csv(filename, sep=',', error_bad_lines=False, warn_bad_lines=True, typeDict=None):
    try:
        ppd = pd.read_csv(filename, sep=sep, error_bad_lines=False, dtype=typeDict)
    except UnicodeDecodeError:
        # 编码可采用gbk、ansi、gb18030、mbcs、dbcs
        ppd = pd.read_csv(filename, sep=sep, encoding='ansi', error_bad_lines=False, dtype=typeDict)
    except Exception as e:
        ppd = None
        print(e)
    finally:
        return ppd


'''
整合PlayCountsList数据，相同的ZXCode记录合并，Duration和PlayCounts累加
parameters: 
    playCountsList: List of DataFrames
return:
    DataFrame of merged playcounts
'''


def getMergedPlayCounts(playCountsList):
    playCounts = pd.concat(playCountsList, sort=False).groupby('ZXCode', as_index=False)['Duration', 'PlayCount'].sum()
    playCounts.loc[:, 'ZXCode'] = playCounts.loc[:, 'ZXCode'].astype(np.object)

    return playCounts


'''
读取PlayCounts数据，数据应有表头"ZXCode,Duration,PlayCounts"
parameter: 
    playCountsFile: List of playCounts filename
    types:each Field's data type
return:
    List of playCounts DataFrames
'''


def getPlayCounts(playCountsFile, types=None):
    playCountsList = []
    for file in playCountsFile:
        p = my_read_csv(file, typeDict=types)
        p = p.dropna(axis=1, how='all')
        for column in p.columns:
            if column not in ['ZXCode', 'Duration', 'PlayCount']:
                p = p.drop(columns=[column])
        # print(p.info())
        playCountsList.append(p)
    return getMergedPlayCounts(playCountsList)


def main():
    allPrograms = my_read_csv(settings.allProgramFile.get('filename'),
                              typeDict=settings.allProgramFile.get('types'))

    print(allPrograms.shape[0])
    print(allPrograms[allPrograms['CREATETIME'] < settings.timePoint].loc[:, 'FILESIZE'].sum())
    print(allPrograms[allPrograms['CREATETIME'] < settings.timePoint].shape[0])
    all = allPrograms.shape[0]
    mmm = 48286
    zhanbi1 = 100 * mmm / all
    allsize = allPrograms.loc[:, 'FILESIZE'].sum() / 1024 / 1024 / 1024
    mmmsize = 33203093814 / 1024 / 1024 / 1024
    zhanbi2 = 100 * mmmsize / allsize

    print('节目总量%d，连续三个月零点播总量%d，占比%.2f%%;节目占用总存储容量：%.1fT，连续三个月零点播占用存储容量：%.1fT，占比%.2f%%' % (
        all, mmm, zhanbi1, allsize, mmmsize, zhanbi2))
    pass


if __name__ == '__main__':
    main()
