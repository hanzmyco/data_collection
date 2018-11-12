#!/usr/bin/env python
# encoding: utf-8
import sys
import requests
import json

def read_tianya_labels(file_name,thresh_hold,out_data_file_name=None):
    label = [[],[],[],[],[]]
    num_0 =[0,0,0,0,0]
    num_1 = [0,0,0,0,0]

    for line in open(file_name,encoding = 'utf-8'):
        line = line.strip()
        d = json.loads(line)


        for index in range(0,len(d['result']['pass'])):
            print(d['result']['pass'][index])
            target = d['result']['pass'][index]
            if target['score'] > thresh_hold[index]:
                label[index].append(1)
                num_1[index]+=1
            else:
                label[index].append(0)
                num_0[index]+=1


    for index in range(0,5):
        with open(out_data_file_name+'_'+str(index)+'.label','w+') as label_out:
            for ite in label[index]:
                label_out.write(str(ite))
                label_out.write('\n')
            label_out.close()
    print(num_0)
    print(num_1)






def main():
    thresh_hold=[0.5,0.5,0.5,0.5,0.5]
    read_tianya_labels(sys.argv[1],thresh_hold,sys.argv[2])



if __name__ == '__main__':
    main()
