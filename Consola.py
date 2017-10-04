import twitter
from Documentacion.config import *

tw = Twitter(auth = OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

world_trends = tw.trends.place(_id = WORLD_WOE_ID)
argentina_trends = tw.trends.place(_id = ARGENTINA_WOE_ID)
print('Tendencias Mundiales en formato JSON')
print(world_trends)
for tendencia in world_trends[0]['trends']:
    print(tendencia['name'])

print("\n\n\n")
print('Tendencias Argentinas en formato JSON: ')
print(argentina_trends)
for tendencia in argentina_trends[0]['trends']:
    print(tendencia['name'])