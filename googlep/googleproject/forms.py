from django import  forms

SEARCH=[('all','All Courses'),
    ('datascience','Data Science'),
('artificial intelligence','Artificial Intelligence'),
('programming','Programming'),
('autonomous system','Autonomous System'),
('cloud computing','Cloud Computing'),
        ]
DURATION=[ ('0','Select Duration'),
          ('1',' 1 month'),
          ('2','2-3 month'),
          ('3', '3-6 month'),
          ('6', 'more than 6 month'),
]
class search_form(forms.Form):
    search2lower=forms.CharField(widget=forms.Select(choices=SEARCH))
    duration=forms.CharField(widget=forms.Select(choices=DURATION))
  #  return render(request,'googleproject/index.html',{'forms':search})


class scraper:
    listt = ["course", "artificialintelligence", "machinemearning", "softskills", "hardware", "blockchain",
             "webdevelopment"]
    Title=[]
    Detail=[]
    link=[]
    image=[]
    duration=[]
    rating=[]
    level=[]

class obj_list:
    OBJ=scraper()
