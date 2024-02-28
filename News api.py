import requests as rq

world_news = rq.get("https://api.nytimes.com/svc/topstories/v2/world.json?api-key=OcxS60gEJGK534n3jLYRKqb4OPyfo3SY")
sport_news = rq.get("https://api.nytimes.com/svc/topstories/v2/sports.json?api-key=OcxS60gEJGK534n3jLYRKqb4OPyfo3SY")
business = rq.get("https://api.nytimes.com/svc/topstories/v2/business.json?api-key=OcxS60gEJGK534n3jLYRKqb4OPyfo3SY")
home_news = rq.get("https://api.nytimes.com/svc/topstories/v2/home.json?api-key=OcxS60gEJGK534n3jLYRKqb4OPyfo3SY")

news = []
world_json = world_news.json()
sport_json = sport_news.json()
business_json = business.json()
home_json = home_news.json()
for i in range(2):
    news.append(world_json["results"][i])
    news.append(sport_json["results"][i])
    news.append(business_json["results"][i])
    news.append(home_json["results"][i])
new_text = ""
for new in news:
    new_text += (str(new["title"]) + "\n")
    new_text += (str(new["abstract"]) + "\n")
    new_text += (str(new["url"]) + "\n")

print(new_text)
