# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 12:06:40 2018

@author: ppareek1
"""

# -*- coding: utf-8 -*-
"""
Assignment Project #
"""

import math
from operator import itemgetter


# recommender class for user-based filtering which recommends the songs
class UserBasedFilteringRecommender:
    
   

    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      }
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    # m:
    # the number of recommedations to return
    # defaults to 10
    #
    def __init__(self, usersItemRatings, metric='pearson', k=1, m=10):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (FYI - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
         
        # set self.m
        if m > 0:   
            self.m = m
        else:
            print ("    (FYI - invalid value of m (must be > 0) - defaulting to 10)")
            self.m = 10
            

   
    # pearson correlation similarity

    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        
        n = len(userXItemRatings.keys() & userYItemRatings.keys())
        
        for item in userXItemRatings.keys() & userYItemRatings.keys():
            x = userXItemRatings[item]
            y = userYItemRatings[item]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
       
        if n == 0:
            print ("    (FYI - personFn n==0; returning -2)")
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            print ("    (FYI - personFn denominator==0; returning -2)")
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            

  
    # make recommendations for user X from the (best similarity) k nearest neigibors (KNNs)
    def recommendKNN(self, userX):
        
       
        pc_lst = []
        pc_lst_topk = []
        sum_pc_topk = 0
      
        for userY in self.usersItemRatings.keys():
            if userY != userX:

                pcY_withX_initial = self.pearsonFn(self.usersItemRatings[userX],self.usersItemRatings[userY])
                pcY_withX = (pcY_withX_initial + 1) / 2
                user_tup_pc = (userY, pcY_withX)
                
                pc_lst.append(user_tup_pc)
        sortedpc_lst = sorted(pc_lst, key=itemgetter(1), reverse=True)
        #print("sorted List", sortedpc_lst)
        

        pc_lst_topk = sortedpc_lst[:self.k]
        #print('topk list', pc_lst_topk)
        
        j=0

        for i in pc_lst_topk:
            
            sum_pc_topk = sum_pc_topk +  pc_lst_topk[j][1]
            j=j+1
            #print('sum is', sum_pc_topk)
        
              
                
                
    #ties and pc +1 fundae    
            
        lst_reco = []
        lst_influence = []
        dict_inf = {}
        list_of_songs = []
        sum_for_reco = 0
        songs_not_inX = []

        #loop to calculate wts/ influence
        j = 0
        for i in pc_lst_topk:
            influence_user = pc_lst_topk[j][1]/ sum_pc_topk
            tup_influence_user = (pc_lst_topk[j][0], influence_user) 
            lst_influence.append(tup_influence_user)
            j = j+1
        #print("list of calculated weight", lst_influence)

            
# differentiating the songs from the two lists            
        i = 0         
        for value in lst_influence:
            x = self.usersItemRatings[userX]
            
            
            userY = lst_influence[i][0]
            y = self.usersItemRatings[userY]
            for songs in y.keys():
                if songs not in x.keys():
                    songs_not_inX.append(songs)
            i = i + 1
        
               
        
                
            
        songs_not_inX = set(songs_not_inX)
        #print('songs not in x', songs_not_inX)
            
        
        for song in songs_not_inX:
                i = 0
                sum_for_reco = 0
        
                for value in lst_influence:
                    
                    infl_val_user = lst_influence[i][1]
                    usertemp = lst_influence[i][0]
                    z = self.usersItemRatings[usertemp]
                    if song in z.keys():
                        rate_val_song_user = z[song]
                        acc_rating_of_song = infl_val_user * rate_val_song_user
                        sum_for_reco = sum_for_reco + acc_rating_of_song
                        #print("sum of rating", song, usertemp, acc_rating_of_song, sum_for_reco)
                    i = i+1
                        
#                
                tup_reco = (song, round(sum_for_reco, 2))
#                

                lst_reco.append(tup_reco)
##        
        sortedlst_reco = sorted(lst_reco, key=itemgetter(1), reverse=True)
#return the first m items
        return(sortedlst_reco[:self.m])
#
#            
#                    
#                
                    
    