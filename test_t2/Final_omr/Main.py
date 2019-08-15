import json

import Crop_segments
import Question_recog
import Name_recog
import Mobile_recog
import Roll_no
import Center_code
import Category

In_path ="Input/"
Out_path ="Aligned/"
Score_path = "Score/"

Crop_segments.crop(In_path,Out_path,Score_path)
answer=Question_recog.question()
name = Name_recog.name()
mobile = Mobile_recog.mobile()
rollno = Roll_no.roll_no()
code=Center_code.code()
cate = Category.category()

data={'centerCode':code,
         'rollNo':rollno,
         'name':name,
         'category':cate,
         'mobileNo':mobile,
         'answers':answer}
         
data_json = json.dumps(data)

f= open("data.txt","w+")
f.write(data_json)
f.close()
