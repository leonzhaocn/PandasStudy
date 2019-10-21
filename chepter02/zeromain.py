import settings
import functions
import pandas as pd
import numpy as np

'''
这个程序是读取联通、广联提供的节目数据和播放数据，得到一定时间段内的n次点播数据
程序使用pandas进行统计
'''


def main():
    # 1、读取相关文件
    allPrograms = functions.my_read_csv(settings.allProgramFile.get('filename'),
                                        typeDict=settings.allProgramFile.get('types'))
    print('成功导入中兴全量数据%s条' % allPrograms.shape[0])
    ssh = functions.my_read_csv(settings.sshFile.get('filename'), typeDict=settings.sshFile.get('types'))
    print('成功导入SSH全量数据%s条' % ssh.shape[0])
    cp = pd.read_excel(settings.cpFile)
    print('成功导入CP对应表%s条' % cp.shape[0])
    # 读取播放数据文件，并合并成一个
    # 各读取文件格式应该相同
    playCounts = functions.getPlayCounts(settings.playCountsFile, settings.playCountsTypes)
    print('成功导入并整合播放数据，共%s条' % playCounts.shape[0])
    # 2、计算和统计相关结果
    allPrograms_with_CP_CODE = pd.merge(allPrograms, ssh, left_on='TELECOMCODE', right_on='CSP_CODE',
                                        how='left')
    allPrograms_with_CP_NAME = pd.merge(allPrograms_with_CP_CODE, cp, left_on='CREATE_PEOPLE', right_on='spid',
                                        how='left')
    print('完成全量数据、SSH数据及CP数据整合')
    allPrograms_with_CP_NAME.groupby('spname')['FILESIZE'].agg([np.size, np.sum]).to_csv(settings.allOutputFile)
    result = pd.merge(allPrograms_with_CP_NAME, playCounts, left_on='CONTENTCODE',
                      right_on='ZXCode', how='left')

    result = result.fillna({'spname': 'NotFound', 'Duration': 0.0, 'PlayCount': 0.0})
    print('完成全量数据与播放数据整合，结果数据结构为：')
    print(result.info())

    # 3、输出相关文件
    for n, file in settings.outExcelFile.items():
        # 获取N次及以下点播，timePoint时间点之前上线的节目列表
        plResult = result[(result['PlayCount'] <= n) & (result['CREATETIME'] < settings.timePoint)]
        # plResult.loc[:, 'CREATETIME'] = plResult.loc[:, 'CREATETIME'].astype(np.object)

        cpResult = plResult.groupby('spname')['FILESIZE'].agg([np.size, np.sum])
        cpResult.columns = ['节目数', '占用存储']

        # 写入一个文件两个sheet
        writer = pd.ExcelWriter(file)
        plResult.to_excel(writer, sheet_name='零点播数据', index=False,
                          columns=['CONTENTNAME', 'TELECOMCODE', 'CREATETIME', 'FILESIZE', 'spname'])
        cpResult.to_excel(writer, sheet_name='统计数据')
        writer.save()
        all = allPrograms.shape[0]
        mmm = plResult.shape[0]
        zhanbi1 = 100 * mmm / all
        allsize = allPrograms.loc[:, 'FILESIZE'].sum() / 1024 / 1024 / 1024
        mmmsize = plResult.loc[:, 'FILESIZE'].sum() / 1024 / 1024 / 1024
        zhanbi2 = 100 * mmmsize / allsize

        print('节目总量%d，连续三个月零点播总量%d，占比%.2f%%;节目占用总存储容量：%.1fT，连续三个月零点播占用存储容量：%.1fT，占比%.2f%%' % (
            all, mmm, zhanbi1, allsize, mmmsize, zhanbi2))
        allPrograms2 = allPrograms[allPrograms['CREATETIME'] < settings.timePoint]
        all = allPrograms2.shape[0]
        mmm = plResult.shape[0]
        zhanbi1 = 100 * mmm / all
        allsize = allPrograms2.loc[:, 'FILESIZE'].sum() / 1024 / 1024 / 1024
        mmmsize = plResult.loc[:, 'FILESIZE'].sum() / 1024 / 1024 / 1024
        zhanbi2 = 100 * mmmsize / allsize
        print('去除三个月内上线节目，节目总量%d，连续三个月零点播总量%d，占比%.2f%%;节目占用总存储容量：%.1fT，连续三个月零点播占用存储容量：%.1fT，占比%.2f%%' % (
            all, mmm, zhanbi1, allsize, mmmsize, zhanbi2))


if __name__ == '__main__':
    main()
