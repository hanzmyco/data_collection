#!/usr/bin/env python
# encoding: utf-8
import sys
import requests
import ijson
import rules

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
    for item in content:
        for k in item:
            content = item[k]
        #print(content)
        for ite in content:
            if not rules.filter_rules(ite):
                data_block.append(ite+'\n')
                data_block_len+=1
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




def main():
    read_tianya_data(sys.argv[1],sys.argv[2])
    #token_access='24.cdd63c7d0e512d06be4fedcc47314b24.2592000.1544150400.282335-14620368'
    #print(get_review_result(token_access,'一起吃鸡吧'))


if __name__ == '__main__':
    main()
