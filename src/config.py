'''
	config
'''
class Config:
	#file
	fnames = ['2016-02','2016-04','2016-05','2016-06','2016-07','2016-08','2016-09','2016-10','2016-11']
	pyaddr = 'pyList.json'
	hzaddr = 'hzList.json'
	trans_name = 'trans-prob.pickle'
	emit_name = 'emit-prob.pickle'
	py2hz_name = 'py2hz-prob.pickle'
	

	#hyper parameters
	py_num = 413
	hz_num = 9116
	maxlen = 20 #maxlen of sentence
	emb_size = 500
	bank_num = 18
	highway_num = 8
	dropout_rate = 0.2
	
	#for train
	batch_num = 32 
	epoch_num = 5
	validation_split = 0.2
