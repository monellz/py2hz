from interface import AbstractSmooth

class Adddelta(AbstractSmooth):
    def __init__(self):
        AbstractSmooth.__init__(self)
        self.delta = self.config['adddelta_delta']

    def smooth2(self,s1,s2):
        '''
            prob = \frac{count(s1s2) + delta}{count(s1) + delta * V}
        '''
        gram = s1 + s2
        if gram not in self.c2.keys():
            self.c2[gram] = 0
        if s1 not in self.c1.keys():
            self.c1[s1] = 0
        prob = (self.c2[gram] + self.delta) / (self.c1[s1] + self.delta * self.config['1sum'])
        return prob
    def smooth3(self,s1,s2,s3):
        '''
            prob(s3|s1s2) = \frac{count(s1s2s3) + delta}{count(s1s2} + delta * V-2order}
        '''
        gram = s1 + s2 + s3
        if gram not in self.c3.keys():
            self.c3[gram] = 0
        if s1 + s2 not in self.c2.keys():
            self.c2[s1 + s2] = 0
        prob = (self.c3[gram] + self.delta) / (self.c2[s1 + s2] + self.delta * self.config['2sum'])
        return prob


class Linear(AbstractSmooth):
    def __init__(self):
        AbstractSmooth.__init__(self)
        self.linear2_lambda = self.config['linear2_lambda']
        self.linear3_3order = self.config['linear3_3order']
        self.linear3_2order = self.config['linear3_2order']
    def smooth2(self,s1,s2):
        '''
            prob(s2|s1) = lamda * \frac{count(s1s2) / count(s2)} + (1 - lambda) * \frac{count(s2) / V}

        '''
        if s2 not in self.c1.keys():
            self.c1[s2] = 0
        if s1 + s2 not in self.c2.keys():
            self.c2[s1 + s2] = 0
        prob = self.linear2_lambda * (self.c2[s1 + s2] / max(self.c1[s2],1)) + (1 - self.linear2_lambda) * (self.c1[s2] / self.config['1sum'])
        return max(prob,1e-200)
    def smooth3(self,s1,s2,s3):
        '''
            prob(s3|s1s2) = l1 * 3-order + l2 * 2-order + l1 * 1-order
        '''
        if s1 + s2 + s3 not in self.c3.keys():
            self.c3[s1 + s2 + s3] = 0
        if s1 + s2 not in self.c2.keys():
            self.c2[s1 + s2] = 0
        if s2 + s3 not in self.c2.keys():
            self.c2[s2 + s3] = 0
        if s2 not in self.c1.keys():
            self.c1[s2] = 0
        if s3 not in self.c1.keys():
            self.c1[s3] = 0
        prob = self.linear3_3order * (self.c3[s1 + s2 + s3] / max(self.c2[s1 + s2],1)) + \
                self.linear3_2order * (self.c2[s2 + s3] / max(self.c1[s2],1)) + \
                    (1 - self.linear3_2order - self.linear3_3order) * self.c1[s3] 
        #print(prob)
        return max(prob,1e-200)

        
