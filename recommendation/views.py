from django.shortcuts import render
from django.http import HttpResponse
import os
import numpy as np
# Create your views here.
def display(request):
    return render(request,'home.html',{'name':'nitin'})
from scipy.sparse import csr_matrix
import pandas as pd
def get_recommendations(request):
    try:
        bname=str(request.GET['bname'])
        combined=pd.read_csv('assets/final_data.csv')
        books=pd.read_csv('assets/BX-Books.csv',sep=';',error_bad_lines=False,encoding='latin-1')
        books.columns=['ISBN','bookTitle','bookAuthor','yearOfPublication','publisher','imageUrlS','imageUrlM','imageUrlL']
        user_rating=combined.drop_duplicates(['userID','bookTitle'])
        user_rating_pivot=user_rating.pivot(index='bookTitle',columns='userID',values='bookRating').fillna(0)
        user_rating_matrix=csr_matrix(user_rating_pivot.values)


        from sklearn.neighbors import NearestNeighbors
        model_knn=NearestNeighbors(metric='cosine',algorithm='brute')
        model_knn.fit(user_rating_matrix)

        a=user_rating_pivot.index==bname
        query_index, = np.where(a == True) # integers
        query_index=int(query_index)

        distances,indices=model_knn.kneighbors(user_rating_pivot.iloc[query_index,:].values.reshape(1,-1),n_neighbors=6)

        
        x=[]
        for i in range(0,len(distances.flatten())):
            if i==0:
                #print("Recommendations for {0}:\n".format(user_rating_pivot.index[query_index]))
                pass
            else:
                #print('{0}: {1},with distance of {2}:'.format(i,user_rating_pivot.index[indices.flatten()[i]],distances.flatten()[i]))
                x.append(user_rating_pivot.index[indices.flatten()[i]])

        y=pd.DataFrame(x,index=np.arange(5),columns=['bookTitle'])
        y1=pd.merge(y,books,on='bookTitle')
        y2=y1.drop_duplicates(['bookTitle'])
        y2.drop(columns=['imageUrlM','imageUrlL'],inplace=True)
        y2.set_index('bookTitle',inplace=True)
        isbn=[]
        bookauthor=[]
        yearofpublication=[]
        publisher=[]
        imageurl=[]
        for j in x:
            isbn.append(y2.loc[j]['ISBN'])
            bookauthor.append(y2.loc[j]['bookAuthor'])
            yearofpublication.append(y2.loc[j]['yearOfPublication'])
            publisher.append(y2.loc[j]['publisher'])
            imageurl.append(y2.loc[j]['imageUrlS'])

        

        
        return render(request,"result.html",{'bname':bname,'name0':x[0],'name1':x[1],'name2':x[2],'name3':x[3],'name4':x[4],'isbn0':isbn[0],'isbn1':isbn[1],'isbn2':isbn[2],'isbn3':isbn[3],'isbn4':isbn[4],'bookauthor0':bookauthor[0],'bookauthor1':bookauthor[1],'bookauthor2':bookauthor[2],'bookauthor3':bookauthor[3],'bookauthor4':bookauthor[4],'yearofpublication0':yearofpublication[0],'yearofpublication1':yearofpublication[1],'yearofpublication2':yearofpublication[2],'yearofpublication3':yearofpublication[3],'yearofpublication4':yearofpublication[4],'publisher0':publisher[0],'publisher1':publisher[1],'publisher2':publisher[2],'publisher3':publisher[3],'publisher4':publisher[4],'imageurl0':imageurl[0],'imageurl1':imageurl[1],'imageurl2':imageurl[2],'imageurl3':imageurl[3],'imageurl4':imageurl[4]})
    except:
        return render(request,"home.html",{'msg':'Select a valid Book Name'})
