import requests
import json
import time
list_cities =['Delhi','Mumbai','Bangalore','Kolkata','Chennai']

for j in range(0,5):
     for i in range(0,1):
         choice = list_cities[j]
         url1 = "https://developers.zomato.com/api/v2.1/locations?query="
         url1 = url1 + str(choice)
         r1 = requests.get(url1, headers=headers)
         r1 = r1.content
         r1 = json.loads(r1.decode())
         id_city = r1['location_suggestions'][0]['city_id']
         url2 = 'https://developers.zomato.com/api/v2.1/search?entity_id='
         url2 = url2 + str(id_city) + '&entity_type=city'
         r2 = requests.get(url2, headers=headers)
         r2 = r2.content
         r2 = json.loads(r2.decode())
         for k in range(0,20):
             res_id = r2['restaurants'][k]['restaurant']['R']['res_id']
             avg_cost = r2['restaurants'][k]['restaurant']['average_cost_for_two']
             name = r2['restaurants'][k]['restaurant']['name']
             address = r2['restaurants'][k]['restaurant']['location']['address']
             menu = r2['restaurants'][k]['restaurant']['menu_url']
             photos = r2['restaurants'][k]['restaurant']['photos_url']
             thumbnail = r2['restaurants'][k]['restaurant']['featured_image']
             thumbnail = thumbnail.split('?')[0]
             rest_obj = Restaurant.objects.create(City_ID = id_city,name=name,address=address,average_cost_for_two=avg_cost,menu_link=menu,photo_link=photos,thumbnail=thumbnail)
             url3 = 'https://developers.zomato.com/api/v2.1/reviews?res_id=' + str(res_id )
             r3 = requests.get(url3, headers=headers)
             r3 = r3.content
             r3 = json.loads(r3.decode())
             for l in range(0,5):
                 rating = r3['user_reviews'][l]['review']['rating']
                 title = r3['user_reviews'][l]['review']['rating_text']
                 content = r3['user_reviews'][l]['review']['review_text']
                 author = r3['user_reviews'][l]['review']['user']['name']
                 author_photo = r3['user_reviews'][l]['review']['user']['profile_image']
                 Review.objects.create(restaurant=rest_obj,author = author,title = title,content = content,rating = rating,display_pic = author_photo)





