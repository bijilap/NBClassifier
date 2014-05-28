import sys
import string
import operator
from math import log

class nbclassify:
	log_word_prob={} # log of probability of word/label
	log_prior={} #log of prior probabilities
	default_log_prob={}
	
	def test_number(self,num): #check if token is a number
		try:
			float(num)
			return True
		except:
			return False
		return False	

	def constructor(self):
		f=open(sys.argv[1],'r')
		labels=f.readline().split()
		#print labels
		for l in labels:
			m=l.split(':')
			#if len(m)>1:
			self.log_prior[m[0]]=float(m[1])
		
		default_val=f.readline().split()
		
		for v in default_val:
			m=v.split(':')
			self.default_log_prob[m[0]]=float(m[1])
			#print m
		
		for w in f:
			w=w.replace('\n','')
			words=w.split('\t')
			#print words
			self.log_word_prob[words[0]]=float(words[1])	

	def assign_label(self,pA):
		return max(pA.iteritems(),key=operator.itemgetter(1))[0]
		
	def classify_text(self,txt):
		#txt=txt.lower()
		#print txt
		txt=txt.replace('\n','')
		words=txt.split(' ')
		pA={}

		for k in self.log_prior:
			pA[k]=self.log_prior[k]

		for w in words:
			for k in self.log_prior:
				feature=k+' '+w
				#print feature+' '+str(self.log_word_prob[feature])
				if self.log_word_prob.has_key(feature):
					pA[k]+=self.log_word_prob[feature]
				else:
					pA[k]+=self.default_log_prob[k]

				

		assigned_label=self.assign_label(pA)
		#if assigned_label=='POS':
		#	print txt
		return assigned_label

nbl=nbclassify()
nbl.constructor()

#test spam filter
f=open(sys.argv[2],'r')
#f2=open('dumpfile.txt','w')
for l in f:
	print (str(nbl.classify_text(l)))
f.close()
#f2.close()
