#!/usr/bin/env python
# encoding: utf-8
import sys
import requests
import ijson
import rules
import time

def get_review_result(access_token,text):
    request_url='https://aip.baidubce.com/rest/2.0/antispam/v2/spam?access_token='+access_token
    response = requests.post(request_url, data={'content': text})
    return response.text

def read_tianya_data(file_name,out_data_file_name=None):
    f = open(file_name)
    data_block=[]
    content = ijson.items(f,'item')
    output_index=0
    data_block_len = 0
    labels_block=[]
    token_access = '24.cdd63c7d0e512d06be4fedcc47314b24.2592000.1544150400.282335-14620368'

    for item in content:
        for k in item:
            content = item[k]
        #print(content)
        for ite in content:
            if not rules.filter_rules(ite):
                data_block.append(ite+'\n')
                data_block_len+=1

                labels_block.append(str(get_review_result(token_access, ite))+'\n')

                if data_block_len==10000:
                    with open(out_data_file_name+str(output_index)+'.txt','w+',encoding='utf-8') as f_out:
                        try:
                            f_out.writelines(data_block)
                            data_block = []
                            data_block_len = 0
                            output_index += 1
                            print(output_index)

                        except:
                            data_block = []
                            data_block_len = 0
                            output_index += 1
                            print(output_index)
                            continue
                    with open(out_data_file_name+str(output_index-1)+'_labels.txt','w+',encoding='utf-8') as label_out:
                        try:
                            label_out.writelines(labels_block)
                            labels_block_block = []

                        except:
                            labels_block = []
                            #print(output_index)
                            continue

def readTianyaByLine(file_tianya,label_tianya,file_index,access_token):
     num=0
     with open(label_tianya[:30]+str(file_index)+label_tianya[30:],'a',encoding = 'utf-8') as label_out:
         with  open(file_tianya[:32]+str(file_index)+file_tianya[32:],'r',encoding = 'utf-8') as f:
            while True:
                try:
                    line = f.readline()
                    if line =='' or line == None:
                        print(num)
                        break

                    result = get_review_result(access_token,line.strip())
                    #print(str(result))
                    while 'error_msg' in str(result):
                        print('error')
                        result = get_review_result(access_token, line.strip())

                    label_out.write(result)
                    #time.sleep(1)
                    label_out.write('\n')
                except:
                    print('some thing wrong')
                    print(num)
                    continue
                num+=1



def main():
    #read_tianya_data(sys.argv[1],sys.argv[2])
    token_access='24.254dee64f67b7ce9ba030e752b4afc13.2592000.1544426178.282335-14620368'
    #print(get_review_result(token_access,'交易所问询不少， 嘴硬，  实力也硬，罗牛山封涨停真不含糊，'))

    readTianyaByLine(sys.argv[1],sys.argv[2],sys.argv[3],token_access)



if __name__ == '__main__':
    main()
