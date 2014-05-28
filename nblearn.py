import sys
import string
from math import log
class nblearn:

	word_freq={} #feature:frequency -> format of word freq-> LABEL#word:freq
	N={} #total number of words per label (N)
	total_mail_count={} #label: no of mails per label
	log_prior={} #log of prior probabilities
	log_word_prob={} #log probability---> LABEL#word:log of probability
	vocab={} #all the words learned, minus their lable

	def add_to_vocab(self,word):
		if self.vocab.has_key(word)==False:
			self.vocab[word]=True	

	def populate_features(self):
		f=open(str(sys.argv[1]),'r')
		prev_label=''
		for line in f:
			line=line.replace('\n','');
			features=line.split()
			label=features[0]
			features.pop(0)
			if prev_label!=label:
				prev_label=label
				if self.total_mail_count.has_key(label):
					self.total_mail_count[label]+=1
				else:
					self.N[label]=0
					self.total_mail_count[label]=1
			else:
				self.total_mail_count[label]+=1
			for w in features:
				#w=w.lower()
				self.add_to_vocab(w)
				word=label+' '+w
				self.N[label]+=1
				if self.word_freq.has_key(word):
					self.word_freq[word]+=1
				else:
					self.word_freq[word]=2
					#if self.vocab_size.has_key(label)==False:
						#self.vocab_size[label]=0
		f.close()

	
	def calc_probabilities(self):
		total_docs=0 #total number of docs

		#calculation of log of prior probabilities
		for key in self.total_mail_count:
			total_docs+=self.total_mail_count[key]

		for key in self.total_mail_count:
			self.log_prior[key]=log(self.total_mail_count[key])-log(total_docs)
			

		for key in self.total_mail_count:
			#total_docs+=self.total_mail_count[key]
			print key+' '+str(self.N[key])
		print len(self.vocab)

		for key in self.word_freq:
                        word=key.split(' ')

			self.log_word_prob[key]=log(self.word_freq[key])-log(self.N[word[0]]+len(self.vocab))	

	#output the model file	
	def output_file(self):
		f=open(str(sys.argv[2]),'w')
		for key in self.log_prior:
			f.write(key+':'+str(self.log_prior[key])+'\t')
		f.write('\n')
		#default value when a word is not found
                for key in self.N:
                        f.write(key+':'+str(0-log(self.N[key]+len(self.vocab)))+'\t')
                f.write('\n')

		for key in self.log_word_prob:
			f.write(key+'\t'+str(self.log_word_prob[key])+'\n')
		f.close()

nbl=nblearn()
nbl.populate_features()
nbl.calc_probabilities()
nbl.output_file()
#nbl.create_modfile()
